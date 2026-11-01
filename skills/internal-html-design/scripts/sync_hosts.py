#!/usr/bin/env python3
"""Install an independent host package, or compare it without writing."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import uuid

NAME = 'internal-html-design'
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'package-manifest.json'
DIRECTORIES = {'assets', 'references', 'scripts', 'examples', 'tests', 'agents'}


def host_entrypoint(data, host):
    text = data.decode('utf-8')
    parts = text.split('---', 2)
    if len(parts) != 3 or parts[0] or not parts[1].startswith('\n'):
        raise ValueError('The source SKILL.md needs YAML frontmatter.')
    lines = [line for line in parts[1].strip('\n').splitlines()
             if not line.startswith('disable-model-invocation:')]
    if host == 'claude':
        lines.append('disable-model-invocation: true')
    return ('---\n' + '\n'.join(lines) + '\n---' + parts[2]).encode('utf-8')


def payload(source, host):
    files = {}
    for path in sorted(source.rglob('*')):
        relative = path.relative_to(source)
        if relative.parts[0] not in DIRECTORIES and relative.as_posix() != 'SKILL.md':
            continue
        if any(part in {'__pycache__', '.DS_Store', 'node_modules'} for part in relative.parts) or path.suffix == '.pyc':
            continue
        if path.is_symlink():
            raise ValueError(f'Package resources must be local files, not symlinks: {relative}')
        if path.is_file():
            files[relative.as_posix()] = path.read_bytes()
    if 'SKILL.md' not in files or 'scripts/inline.py' not in files:
        raise ValueError('The source is not a complete skill package.')
    files['SKILL.md'] = host_entrypoint(files['SKILL.md'], host)
    hashes = {name: hashlib.sha256(host_entrypoint(data, 'codex') if name == 'SKILL.md' else data).hexdigest()
              for name, data in files.items()}
    files[MANIFEST] = (json.dumps({'format_version': 1, 'host': host, 'files': hashes}, indent=2, sort_keys=True) + '\n').encode()
    return files


def validate_destination(source, target):
    if target.name != NAME:
        raise ValueError(f'Destination must be named {NAME}.')
    if target.is_symlink() or source.is_symlink():
        raise ValueError('Installation roots must not be symlinks.')
    a, b = source.resolve(), target.resolve()
    if a == b or a in b.parents or b in a.parents:
        raise ValueError('Source and destination must not overlap.')


def sync(source, target, host, check=False, backup_root=None):
    source, target = Path(source), Path(target).expanduser().absolute()
    validate_destination(source, target)
    expected = payload(source, host)
    actual = {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob('*')
              if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts and p.suffix != '.pyc'} if target.is_dir() else {}
    if target.is_dir():
        for path in target.rglob('*'):
            if path.is_symlink():
                actual[path.relative_to(target).as_posix()] = b'__symlink__:' + os.readlink(path).encode()
    drift = sorted(name for name in set(expected) | set(actual) if expected.get(name) != actual.get(name))
    if check:
        return {'status': 'drift' if drift else 'match', 'files': drift, 'destination': str(target)}
    if not drift:
        return {'status': 'match', 'files': [], 'destination': str(target)}
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.ihd-stage-', dir=target.parent))
    staged = staging / NAME
    staged.mkdir()
    backup = None
    rollback = staging / 'previous'
    try:
        for name, data in expected.items():
            destination = staged / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        # Verify staged bytes before changing an installed directory.
        if any((staged / name).read_bytes() != data for name, data in expected.items()):
            raise ValueError('Staged package verification failed.')
        if target.exists():
            base = Path(backup_root) if backup_root else Path.home() / '.local/share/internal-html-design/backups'
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
            backup = base / stamp / host / NAME
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(target, backup, symlinks=True)
            os.replace(target, rollback)
        try:
            os.replace(staged, target)
        except Exception:
            if rollback.exists():
                os.replace(rollback, target)
            raise
    finally:
        shutil.rmtree(staging)
    return {'status': 'installed', 'destination': str(target), 'backup': str(backup) if backup else None,
            'common_files': len(expected) - 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['codex', 'claude'], required=True)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = args.destination or Path.home() / f'.{args.target}' / 'skills' / NAME
    try:
        result = sync(ROOT, target, args.target, args.check)
        print(json.dumps(result, indent=2))
        return 1 if result['status'] == 'drift' else 0
    except (OSError, ValueError) as error:
        print(json.dumps({'status': 'error', 'reason': str(error)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
