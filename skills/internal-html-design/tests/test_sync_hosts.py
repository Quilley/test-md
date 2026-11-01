import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('ihd_sync', ROOT / 'scripts/sync_hosts.py')
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


class HostInstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.source = self.base / 'source/internal-html-design'
        self.source.mkdir(parents=True)
        (self.source / 'SKILL.md').write_text('---\nname: internal-html-design\ndescription: Test local package\n---\nRead references/local.md.\n')
        for directory in ('scripts', 'references', 'assets'):
            (self.source / directory).mkdir()
        (self.source / 'scripts/inline.py').write_text('# local packager')
        (self.source / 'references/local.md').write_text('Local resource')
        self.target = self.base / 'claude/internal-html-design'
        self.backups = self.base / 'backups'

    def tearDown(self):
        self.temp.cleanup()

    def test_hosts_have_same_common_content_and_distinct_invocation_metadata(self):
        SYNC.sync(self.source, self.target, 'claude', backup_root=self.backups)
        self.assertIn('disable-model-invocation: true', (self.target / 'SKILL.md').read_text())
        codex = self.base / 'codex/internal-html-design'
        SYNC.sync(self.target, codex, 'codex', backup_root=self.backups)
        self.assertNotIn('disable-model-invocation:', (codex / 'SKILL.md').read_text())
        a = json.loads((self.target / SYNC.MANIFEST).read_text())
        b = json.loads((codex / SYNC.MANIFEST).read_text())
        self.assertEqual(a['files'], b['files'])
        self.assertEqual(SYNC.sync(self.source, self.target, 'claude', check=True)['status'], 'match')

    def test_check_is_read_only_and_replacement_preserves_backup(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_text('old wrapper')
        result = SYNC.sync(self.source, self.target, 'claude', check=True)
        self.assertEqual(result['status'], 'drift')
        self.assertEqual((self.target / 'SKILL.md').read_text(), 'old wrapper')
        result = SYNC.sync(self.source, self.target, 'claude', backup_root=self.backups)
        self.assertEqual((Path(result['backup']) / 'SKILL.md').read_text(), 'old wrapper')
        (self.target / 'references/local.md').write_text('unexpected edit')
        self.assertIn('references/local.md', SYNC.sync(self.source, self.target, 'claude', check=True)['files'])
        (self.target / 'unexpected-link').symlink_to(self.source / 'assets')
        self.assertIn('unexpected-link', SYNC.sync(self.source, self.target, 'claude', check=True)['files'])

    def test_unsafe_destinations_and_source_symlinks_are_rejected(self):
        for target in (self.source, self.base, self.source / 'nested/internal-html-design'):
            with self.subTest(target=target), self.assertRaises(ValueError):
                SYNC.sync(self.source, target, 'claude')
        (self.source / 'assets/link').symlink_to(self.source / 'references/local.md')
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            SYNC.payload(self.source, 'claude')

    def test_relocated_installation_packages_using_only_its_local_assets(self):
        complete = self.base / 'complete/internal-html-design'
        shutil.copytree(ROOT, complete, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        SYNC.sync(complete, self.target, 'claude', backup_root=self.backups)
        complete.rename(self.base / 'source-not-installed')
        source = self.base / 'authored.html'
        source.write_text('<!doctype html><html lang="en"><head><!-- ihd:styles --></head><body><main><h1>Standalone</h1><p>Preserve this exact supplied sentence.</p></main><!-- ihd:reader --></body></html>')
        output = self.base / 'standalone.html'
        result = subprocess.run([sys.executable, str(self.target / 'scripts/inline.py'), str(source), str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Preserve this exact supplied sentence.', output.read_text())
        self.assertIn('data:font/woff2;base64,', output.read_text())
        self.assertNotIn(str(ROOT), (self.target / 'SKILL.md').read_text())


if __name__ == '__main__':
    unittest.main()
