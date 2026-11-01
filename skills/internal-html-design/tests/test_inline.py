import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('ihd_inline', ROOT / 'scripts/inline.py')
INLINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INLINE)
SOURCE = '<!doctype html><html><head><!-- ihd:styles --></head><body><h1>Keep this writing.</h1><!-- ihd:reader --></body></html>'


class InliningTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.faces = self.root / 'faces.css'
        self.font = self.root / 'fixture.woff2'
        self.font.write_bytes(b'fake font payload')
        (self.root / 'fixture.svg').write_text('<svg/>')
        self.faces.write_text('@font-face { font-family: Fixture; src: url("fixture.woff2") format("woff2"); }')

    def tearDown(self):
        self.directory.cleanup()

    def test_default_inliner_embeds_platform_faces_and_license_comments(self):
        result = INLINE.assemble(SOURCE)
        self.assertIn('<h1>Keep this writing.</h1>', result)
        self.assertNotIn('<!-- ihd:', result)
        self.assertGreaterEqual(result.count('data:font/woff2;base64,'), 4)
        self.assertNotRegex(result, r'url\([\'"]?(?:https?:|fonts/)')
        for alias in ('IHD Serif', 'IHD Sans', 'IHD Mono'):
            self.assertIn(alias, result)
        default_faces = (ROOT / 'assets/fonts.css').read_text()
        self.assertIn('newsreader-', default_faces)
        self.assertIn('manrope-', default_faces)
        self.assertIn('geist-mono-', default_faces)
        # Font provenance is carried with the embedded CSS for a saved HTML file.
        comments = re.findall(r'/\*.*?\*/', result, re.S)
        self.assertTrue(any(re.search(r'licen[cs]', comment, re.I) for comment in comments))
        self.assertNotIn('private-mockup', result)

    def test_custom_face_css_is_preserved_by_assemble(self):
        result = INLINE.assemble(SOURCE, self.faces)
        self.assertIn('font-family: Fixture', result)
        self.assertIn('data:font/woff2;base64,', result)
        self.assertIn('Keep this writing.', result)

    def test_missing_or_repeated_markers_fail(self):
        cases = [
            SOURCE.replace('<!-- ihd:styles -->', ''),
            SOURCE.replace('<!-- ihd:reader -->', '<!-- ihd:reader --><!-- ihd:reader -->'),
        ]
        for source in cases:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'exactly one'):
                INLINE.assemble(source)

    def test_all_external_rendering_dependencies_are_rejected(self):
        fragments = [
            '<img src="missing.png">',
            '<img srcset="small.png 1x, large.png 2x">',
            '<script src="https://example.com/app.js"></script>',
            '<svg><image href="remote.svg"/></svg>',
            '<style>p{background:url(../secret.png)}</style>',
            '<style>@import url(https://example.com/theme.css);</style>',
            '<link rel="stylesheet" href="theme.css">',
        ]
        for fragment in fragments:
            with self.subTest(fragment=fragment), self.assertRaisesRegex(ValueError, 'dependency|import|srcset'):
                INLINE.assemble(SOURCE.replace('</body>', fragment + '</body>'))
        INLINE.assemble(SOURCE.replace('</body>', '<a href="https://example.com/source">Source</a></body>'))

    def test_font_paths_formats_and_size_are_constrained(self):
        cases = [
            ('@font-face {src:url(../outside.woff2)}', 'beneath'),
            ('@font-face {src:url(missing.woff2)}', 'beneath'),
            ('@font-face {src:url(fixture.svg)}', 'Unsupported'),
            ('@import url(https://example.com/font.css);', 'import'),
        ]
        for css, error in cases:
            self.faces.write_text(css)
            with self.subTest(css=css), self.assertRaisesRegex(ValueError, error):
                INLINE.font_css(self.faces)
        large = self.root / 'large.woff2'
        with large.open('wb') as target:
            target.truncate(5_000_001)
        self.faces.write_text('@font-face {src:url(large.woff2)}')
        with self.assertRaisesRegex(ValueError, '5 MB'):
            INLINE.font_css(self.faces)

    def test_cli_default_override_preview_alias_and_exclusive_output(self):
        source = self.root / 'source.html'
        output = self.root / 'output.html'
        source.write_text(SOURCE)
        command = [sys.executable, str(ROOT / 'scripts/inline.py'), str(source), str(output)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Newsreader', output.read_text())
        output.unlink()
        result = subprocess.run(command + ['--font-css', str(self.faces)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Fixture', output.read_text())
        self.assertNotIn('private-mockup', output.read_text())

        output.unlink()
        result = subprocess.run(command + ['--preview-fonts'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('private-mockup', output.read_text())
        existing = output.read_text()
        result = subprocess.run(command + ['--preview-fonts'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_text(), existing)
        self.assertEqual(source.read_text(), SOURCE)


if __name__ == '__main__':
    unittest.main()
