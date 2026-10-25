#!/usr/bin/env python3
"""Inline the shared presentation assets into an already-authored HTML file."""
import argparse
import base64
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r'url\(\s*[\'"]?([^\'"\)]+)[\'"]?\s*\)', re.I)


def font_css(path):
    path = path.resolve()
    text = path.read_text()
    if re.search(r'@import\b', text, re.I):
        raise ValueError('Font CSS must not import external stylesheets.')

    def embed(match):
        source = match.group(1).strip()
        if source.startswith('data:font/'):
            return match.group(0)
        target = (path.parent / source).resolve()
        if not target.is_relative_to(path.parent) or not target.is_file():
            raise ValueError(f'Font file must exist beneath the font CSS directory: {source}')
        if target.suffix.lower() not in {'.ttf', '.otf', '.woff', '.woff2'}:
            raise ValueError(f'Unsupported font file: {source}')
        if target.stat().st_size > 5_000_000:
            raise ValueError(f'Font file exceeds 5 MB: {source}')
        mime = {'.ttf': 'ttf', '.otf': 'otf', '.woff': 'woff', '.woff2': 'woff2'}[target.suffix.lower()]
        data = base64.b64encode(target.read_bytes()).decode('ascii')
        return f'url("data:font/{mime};base64,{data}")'

    return URL.sub(embed, text)


class OfflineDependencies(HTMLParser):
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        refs = []
        if 'srcset' in attrs:
            raise ValueError('Inline images using src data URLs instead of srcset.')
        for attribute in ('src', 'poster', 'data'):
            if attribute in attrs:
                refs.append(attrs[attribute])
        if tag in {'use', 'image'}:
            refs.extend(attrs[key] for key in ('href', 'xlink:href') if key in attrs)
        if tag == 'link' and set(attrs.get('rel', '').split()) & {'stylesheet', 'preload', 'icon', 'modulepreload'}:
            refs.append(attrs.get('href', ''))
        for ref in refs:
            if not ref.startswith(('data:', '#')):
                raise ValueError(f'Inline the remaining rendering dependency: {ref}')

    handle_startendtag = handle_starttag


def assemble(source, faces):
    for marker in ('<!-- ihd:styles -->', '<!-- ihd:reader -->'):
        if source.count(marker) != 1:
            raise ValueError(f'Input must contain exactly one {marker}')
    css = font_css(faces) + '\n' + (ROOT / 'assets/theme.css').read_text()
    script = (ROOT / 'assets/reader.js').read_text()
    output = source.replace('<!-- ihd:styles -->', '<style>\n' + css + '\n</style>')
    output = output.replace('<!-- ihd:reader -->', '<script>\n' + script + '\n</script>')
    if re.search(r'@import\b', output, re.I):
        raise ValueError('Inline imported CSS before assembly.')
    for match in URL.finditer(output):
        if not match.group(1).strip().startswith(('data:', '#')):
            raise ValueError(f'Inline the remaining CSS dependency: {match.group(1)}')
    OfflineDependencies().feed(output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--bundled-fonts', action='store_true', help='Embed the bundled Source Serif 4 and Libre Franklin faces.')
    mode.add_argument('--font-css', type=Path, help='Font-face CSS for other licensed font files.')
    args = parser.parse_args()
    faces = ROOT / 'assets/fonts.css' if args.bundled_fonts else args.font_css
    try:
        output = assemble(args.input.read_text(), faces)
        with args.output.open('x') as target:
            target.write(output)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
    print(args.output.resolve())


if __name__ == '__main__':
    main()
