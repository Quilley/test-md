import importlib.util
from pathlib import Path
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
        self.faces.write_text('/* Test with system fallback faces. */')

    def tearDown(self):
        self.directory.cleanup()

    def test_preserves_text_and_inlines_shared_assets(self):
        result = INLINE.assemble(SOURCE, ROOT / 'assets/fonts.css')
        self.assertIn('<h1>Keep this writing.</h1>', result)
        self.assertIn('data:font/ttf;base64,', result)
        self.assertIn("'IHD Source Serif 4'", result)
        self.assertIn("'IHD Libre Franklin'", result)
        self.assertNotIn('<!-- ihd:', result)
        self.assertNotIn('url(\'fonts/', result)

    def test_missing_and_repeated_markers_fail(self):
        for source in [SOURCE.replace('<!-- ihd:styles -->', ''), SOURCE.replace('<!-- ihd:reader -->', '<!-- ihd:reader --><!-- ihd:reader -->')]:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'exactly one'):
                INLINE.assemble(source, self.faces)

    def test_rendering_dependencies_rejected_but_citations_allowed(self):
        for fragment in ['<img src="missing.png">', '<script src="https://example.com/app.js"></script>', '<svg><image href="remote.svg"/></svg>', '<style>p{background:url(../secret.png)}</style>']:
            with self.subTest(fragment=fragment), self.assertRaisesRegex(ValueError, 'dependency'):
                INLINE.assemble(SOURCE.replace('</body>', fragment + '</body>'), self.faces)
        INLINE.assemble(SOURCE.replace('</body>', '<a href="https://example.com/source">Source</a></body>'), self.faces)

    def test_font_path_cannot_escape_its_directory(self):
        self.faces.write_text('@font-face {src: url(../outside.ttf)}')
        with self.assertRaisesRegex(ValueError, 'beneath'):
            INLINE.font_css(self.faces)

    def test_cli_requires_font_mode_and_preserves_existing_output(self):
        source = self.root / 'source.html'
        output = self.root / 'output.html'
        source.write_text(SOURCE)
        command = [sys.executable, str(ROOT / 'scripts/inline.py'), str(source), str(output)]
        self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertFalse(output.exists())
        output.write_text('Existing work')
        result = subprocess.run(command + ['--font-css', str(self.faces)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_text(), 'Existing work')
        self.assertEqual(source.read_text(), SOURCE)


if __name__ == '__main__':
    unittest.main()
