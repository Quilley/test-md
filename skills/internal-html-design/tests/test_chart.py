import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


chart = load('chart')
inline = load('inline')
SPRITE = '<svg class="ihd-sprite" width="0" height="0" aria-hidden="true"></svg>'

BASE = {'title': 'T', 'caption': 'What to notice.'}
SPECS = {
    'bar': dict(BASE, type='bar', items=[{'label': 'A', 'value': 30}, {'label': 'B', 'value': 60}]),
    'grouped': dict(BASE, type='grouped', categories=['A', 'B'], series=[{'name': 'x', 'values': [30, 60]}, {'name': 'y', 'values': [10, 20]}]),
    'stacked': dict(BASE, type='stacked', categories=['A', 'B'], series=[{'name': 'x', 'values': [3, 6]}, {'name': 'y', 'values': [1, 2]}]),
    'line': dict(BASE, type='line', x=[1, 2, 3], series=[{'name': 'a', 'values': [1, 2, 3]}, {'name': 'b', 'values': [2, 3, 5]}]),
    'range': dict(BASE, type='range', items=[{'label': 'A', 'low': 1, 'base': 2, 'high': 4}]),
    'tornado': dict(BASE, type='tornado', base=10, items=[{'label': 'Small', 'low': 9, 'high': 11}, {'label': 'Big', 'low': 4, 'high': 18, 'low_case': 'at 1', 'high_case': 'at 9'}]),
    'waterfall': dict(BASE, type='waterfall', steps=[{'label': 'Start', 'value': 50}, {'label': 'Cut', 'value': -10}, {'label': 'End', 'value': 40, 'kind': 'total'}]),
    'slope': dict(BASE, type='slope', items=[{'label': 'A', 'before': 1, 'after': 5}, {'label': 'B', 'before': 3, 'after': 2}]),
    'scatter': dict(BASE, type='scatter', points=[{'label': 'P', 'x': 1, 'y': 2}, {'label': 'Q', 'x': 5, 'y': 9}]),
    'matrix': dict(BASE, type='matrix', quadrants={'tl': 'One', 'tr': 'Two', 'bl': 'Three', 'br': 'Four'}, points=[{'label': 'P', 'x': 1, 'y': 2}, {'label': 'Q', 'x': 5, 'y': 9}]),
}


def rects(markup):
    return [(float(x), float(w)) for x, w in re.findall(r'<rect class="ihd-s\d[^"]*" x="([\d.]+)" y="[\d.]+" width="([\d.]+)"', markup)]


class MathTests(unittest.TestCase):
    def test_ticks_are_round_and_cover_the_data(self):
        ticks, low, high = chart.ticks_for(0, 64, 5)
        self.assertEqual(ticks, [0, 20, 40, 60, 80])
        self.assertEqual((low, high), (0, 80))
        ticks, low, high = chart.ticks_for(2, 8, 5, zero=False)
        self.assertLessEqual(low, 2)
        self.assertGreaterEqual(high, 8)

    def test_number_format_is_plain(self):
        self.assertEqual(chart.num(0), '0')
        self.assertEqual(chart.num(12.50), '12.5')
        self.assertEqual(chart.num(10000), '10,000')
        self.assertEqual(chart.num(-0.001), '0')
        self.assertEqual(chart.num(-3), '−3')

    def test_spread_keeps_order_and_gap(self):
        out = chart.spread([100, 101, 102], 24, 0, 300)
        self.assertEqual(sorted(out), out)
        self.assertTrue(all(b - a >= 24 for a, b in zip(out, out[1:])))
        with self.assertRaises(chart.ChartError):
            chart.spread([1, 2, 3], 24, 0, 30)


class RenderTests(unittest.TestCase):
    def test_every_type_renders_with_caption_and_unique_ids(self):
        markup = ''.join(chart.render(spec, n) for n, spec in enumerate(SPECS.values(), 1))
        self.assertEqual(markup.count('<figure'), len(SPECS))
        self.assertEqual(markup.count('<figcaption'), len(SPECS))
        ids = re.findall(r'\bid="([^"]+)"', markup)
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_svg_chart_has_a_table_with_every_value(self):
        for name, spec in SPECS.items():
            if name == 'bar':
                continue
            markup = chart.render(spec, 1)
            self.assertIn('ihd-diagram-wide', markup, name)
            self.assertIn('<div class="ihd-diagram-small"><table>', markup, name)
            cells = re.findall(r'<td class="ihd-number">([^<]*)</td>', markup)
            self.assertTrue(cells, name)

    def test_table_holds_inputs(self):
        markup = chart.render(SPECS['range'], 1)
        for value in ('1', '2', '4'):
            self.assertIn(f'<td class="ihd-number">{value}</td>', markup)

    def test_bar_widths_follow_values(self):
        widths = [float(w) for w in re.findall(r'style="width:([\d.]+)%"', chart.render(SPECS['bar'], 1))]
        self.assertEqual(widths, [50.0, 100.0])

    def test_svg_bar_geometry_is_proportional(self):
        grouped = dict(SPECS['grouped'], max=80)
        widths = [w for _, w in rects(chart.render(grouped, 1)) if w > 20]
        # values 30, 10, 60, 20 on one scale; the key swatches are 16 wide and are skipped
        self.assertAlmostEqual(widths[2] / widths[0], 2.0, places=2)
        self.assertAlmostEqual(widths[0] / widths[1], 3.0, places=2)

    def test_series_differ_by_dash_and_marker_not_tone_alone(self):
        spec = dict(SPECS['line'], series=SPECS['line']['series'] + [{'name': 'c', 'values': [3, 4, 6]}])
        markup = chart.render(spec, 1)
        lines = re.findall(r'<polyline class="([^"]+)"', markup)
        self.assertEqual(len(set(lines)), 3)
        self.assertEqual({m for m in re.findall(r'href="#(ihd-m-\w+)"', markup)}, {'ihd-m-circle', 'ihd-m-square', 'ihd-m-triangle'})

    def test_tornado_sorts_by_swing(self):
        markup = chart.render(SPECS['tornado'], 1)
        self.assertLess(markup.index('>Big<'), markup.index('>Small<'))

    def test_waterfall_totals_must_add_up(self):
        bad = dict(SPECS['waterfall'], steps=[{'label': 'Start', 'value': 50}, {'label': 'Cut', 'value': -10}, {'label': 'End', 'value': 45, 'kind': 'total'}])
        with self.assertRaises(chart.ChartError):
            chart.render(bad, 1)

    def test_output_stays_inside_the_ink_kit(self):
        for name, spec in SPECS.items():
            markup = chart.render(spec, 1)
            self.assertNotRegex(markup, r'(fill|stroke)="#', name)
            self.assertNotRegex(markup, r'(fill|stroke|color):\s*#', name)
            self.assertNotIn('<script', markup)

    def test_text_is_escaped(self):
        spec = dict(SPECS['bar'], title='<b>x</b>', items=[{'label': 'A & B', 'value': 1}])
        markup = chart.render(spec, 1)
        self.assertNotIn('<b>', markup)
        self.assertIn('A &amp; B', markup)


class ErrorTests(unittest.TestCase):
    def check(self, spec):
        with self.assertRaises(chart.ChartError):
            chart.render(spec, 1)

    def test_rejects_bad_specs(self):
        self.check(dict(SPECS['bar'], caption=''))
        self.check(dict(SPECS['bar'], title=''))
        self.check(dict(SPECS['bar'], type='pie'))
        self.check(dict(SPECS['bar'], items=[{'label': 'A', 'value': 'ten'}]))
        self.check(dict(SPECS['bar'], items=[{'label': 'A', 'value': float('nan')}]))
        self.check(dict(SPECS['bar'], items=[{'label': 'A', 'value': -1}]))
        self.check(dict(SPECS['line'], series=[{'name': str(i), 'values': [1, 2, 3]} for i in range(4)]))
        self.check(dict(SPECS['range'], items=[{'label': 'A', 'low': 5, 'base': 2, 'high': 4}]))
        self.check(dict(SPECS['grouped'], series=[{'name': 'x', 'values': [1]}]))

    def test_colliding_scatter_labels_are_an_error(self):
        points = [{'label': 'A long label here', 'x': 1 + i * .001, 'y': 1} for i in range(8)]
        self.check(dict(SPECS['scatter'], points=points + [{'label': 'Far', 'x': 9, 'y': 9}]))


class ExpandTests(unittest.TestCase):
    def doc(self, spec, sprite=True):
        return '<html><body>%s<div data-ihd-chart><script type="application/json">%s</script></div></body></html>' % (SPRITE if sprite else '', json.dumps(spec))

    def test_expand_replaces_placeholders_and_numbers_ids(self):
        out = chart.expand(self.doc(SPECS['range']) + self.doc(SPECS['line']))
        self.assertNotIn('data-ihd-chart', out)
        self.assertIn('ihd-chart-1-title', out)
        self.assertIn('ihd-chart-2-title', out)

    def test_expand_needs_the_sprite(self):
        with self.assertRaises(chart.ChartError):
            chart.expand(self.doc(SPECS['range'], sprite=False))

    def test_expand_rejects_bad_json_and_malformed_placeholders(self):
        with self.assertRaises(chart.ChartError):
            chart.expand('<div data-ihd-chart><script type="application/json">{nope</script></div>')
        with self.assertRaises(chart.ChartError):
            chart.expand('<div data-ihd-chart class="x"></div>')

    def test_errors_name_the_chart(self):
        with self.assertRaises(chart.ChartError) as caught:
            chart.expand(self.doc(dict(SPECS['bar'], caption='')))
        self.assertIn('Chart 1', str(caught.exception))

    def test_assemble_expands_before_inlining(self):
        source = '<!doctype html><html><head><!-- ihd:styles --></head><body>%s<!-- ihd:reader --></body></html>' % self.doc(SPECS['waterfall'])
        out = inline.assemble(source)
        self.assertIn('<figure class="ihd-figure"', out)
        self.assertNotIn('data-ihd-chart', out)

    def test_shipped_example_builds(self):
        source = (ROOT / 'examples/source/data-charts.html').read_text()
        out = inline.assemble(source)
        self.assertEqual(out.count('<figure class="ihd-figure"'), 9)


if __name__ == '__main__':
    unittest.main()
