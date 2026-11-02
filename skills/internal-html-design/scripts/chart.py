#!/usr/bin/env python3
"""Turn data into accessible figures: SVG, a text table and a caption, in the skill's ink-only kit.

Source documents hold a placeholder; inline.py expands it. The author supplies data and a chart type,
never coordinates:

    <div data-ihd-chart><script type="application/json">{"type": "range", ...}</script></div>

`python3 chart.py spec.json` prints one figure fragment, for pasting and hand editing.
"""
import html
import json
import math
import re
import sys
from pathlib import Path

W = 640
MONO = 9.6      # px per character, Geist Mono at 16px
SANS = 10.0     # px per character, Manrope at 16px, rounded up so labels never overrun
MINUS = '−'
SERIES = (
    ('ihd-s1', '', 'ihd-m-circle'),
    ('ihd-s2', 'ihd-dash', 'ihd-m-square'),
    ('ihd-s3', 'ihd-dot', 'ihd-m-triangle'),
)
TYPES = ('bar', 'grouped', 'stacked', 'line', 'range', 'tornado', 'waterfall', 'slope', 'scatter', 'matrix')
PLACEHOLDER = re.compile(r'<div\s+data-ihd-chart\s*>\s*<script\s+type="application/json"\s*>(.*?)</script>\s*</div>', re.S)


class ChartError(ValueError):
    pass


# ---- small helpers ---------------------------------------------------------

def esc(value):
    return html.escape(str(value), quote=True)


def isnum(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def need_num(value, where):
    if not isnum(value):
        raise ChartError(f'{where} must be a finite number, got {value!r}')
    return value


def need_list(spec, key, low=1, high=None):
    value = spec.get(key)
    if not isinstance(value, list) or len(value) < low or (high is not None and len(value) > high):
        bound = f'{low} to {high}' if high else f'at least {low}'
        raise ChartError(f'"{key}" must be a list of {bound} entries')
    return value


def num(value):
    value = 0.0 if value == 0 else float(value)
    if abs(value) >= 1000:
        text = f'{abs(value):,.0f}' if abs(value) >= 10000 or value.is_integer() else f'{abs(value):,.1f}'
    else:
        text = ('%.2f' % abs(value)).rstrip('0').rstrip('.')
    if text == '0':
        return '0'
    return (MINUS if value < 0 else '') + text


def fmt(spec, value, signed=False):
    sign = MINUS if value < 0 else ('+' if signed and value > 0 else '')
    return sign + spec.get('prefix', '') + num(abs(value)).replace(MINUS, '') + spec.get('suffix', '')


def tw(text, mono=False):
    return len(str(text)) * (MONO if mono else SANS)


def wrap(text, width):
    lines, current = [], ''
    for word in str(text).split():
        trial = (current + ' ' + word).strip()
        if current and tw(trial) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    return lines + [current] if current else ['']


def ticks_for(low, high, count=5, zero=True):
    if zero:
        low, high = min(low, 0), max(high, 0)
    if low == high:
        high = low + 1
    raw = (high - low) / max(count, 1)
    magnitude = 10 ** math.floor(math.log10(raw))
    fraction = raw / magnitude
    step = (1 if fraction <= 1 else 2 if fraction <= 2 else 5 if fraction <= 5 else 10) * magnitude
    start = math.floor(low / step + 1e-9) * step
    stop = math.ceil(high / step - 1e-9) * step
    ticks, k = [], 0
    while start + k * step <= stop + step * 1e-9:
        ticks.append(round(start + k * step, 10))
        k += 1
    return ticks, ticks[0], ticks[-1]


def axis_ticks(low, high, room, spec, zero=True):
    """Ticks that fit `room` px without their labels touching."""
    for count in (5, 4, 3, 2):
        ticks, lo, hi = ticks_for(low, high, count, zero)
        widest = max(tw(fmt(spec, t), True) for t in ticks)
        if (room / max(len(ticks) - 1, 1)) >= widest + 14:
            return ticks, lo, hi
    return ticks, lo, hi


def spread(centres, gap, low, high):
    """Move label centres apart, keeping order, so none are closer than `gap`."""
    if len(centres) > 1 and (high - low) < gap * (len(centres) - 1):
        raise ChartError('Labels do not fit the height available; use fewer series or points')
    order = sorted(range(len(centres)), key=lambda i: centres[i])
    out, previous = list(centres), None
    for i in order:
        out[i] = max(centres[i], low if previous is None else previous + gap)
        previous = out[i]
    following = None
    for i in reversed(order):
        out[i] = min(out[i], high if following is None else following - gap)
        following = out[i]
    return out


def lin(value, d0, d1, r0, r1):
    return r0 + (value - d0) * (r1 - r0) / (d1 - d0)


def text(x, y, content, cls='ihd-chart-label', anchor='start', extra=''):
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}{extra}>{esc(content)}</text>'


def lines_text(x, y, content, width, cls='ihd-chart-label', anchor='start', lead=20):
    parts = wrap(content, width)
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    spans = ''.join(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else lead}">{esc(part)}</tspan>' for i, part in enumerate(parts))
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}>{spans}</text>', len(parts)


def marker(kind, cx, cy, cls, size=12):
    return f'<use class="{cls}" href="#{kind}" x="{cx - size / 2:.1f}" y="{cy - size / 2:.1f}" width="{size}" height="{size}"/>'


def table(_title, head, rows):
    heads = ''.join(f'<th scope="col">{esc(c)}</th>' for c in head)
    body = ''.join(
        '<tr><th scope="row">{}</th>{}</tr>'.format(esc(r[0]), ''.join(f'<td class="ihd-number">{esc(c)}</td>' for c in r[1:]))
        for r in rows)
    return f'<div class="ihd-diagram-small"><table><caption>The same data, as a table</caption><thead><tr>{heads}</tr></thead><tbody>{body}</tbody></table></div>'


def unit_note(spec, x, y):
    if spec.get('unit'):
        return text(x, y, spec['unit'], 'ihd-chart-label ihd-svg-muted', 'end')
    return ''


# ---- charts ----------------------------------------------------------------
# Each returns (svg_inner, height, table_html, description).

def label_column(labels, cap=190):
    wide = max(tw(label) for label in labels) + 10
    return min(max(wide, 60), cap)


def h_frame(spec, labels, right=70):
    column = label_column(labels)
    x0 = column + 24
    return column, x0, W - right


def r_grouped(spec, stacked=False):
    cats = need_list(spec, 'categories')
    series = need_list(spec, 'series', 1, 3)
    for s in series:
        if len(s.get('values', [])) != len(cats):
            raise ChartError(f'Series "{s.get("name")}" needs {len(cats)} values')
        for v in s['values']:
            need_num(v, f'"{s.get("name")}" value')
            if v < 0:
                raise ChartError('Bars start at zero; use a range or waterfall for negative values')
    totals = [sum(s['values'][i] for s in series) for i in range(len(cats))]
    top = max(totals) if stacked else max(v for s in series for v in s['values'])
    column, x0, x1 = h_frame(spec, cats, right=84)
    ticks, lo, hi = axis_ticks(0, spec.get('max', top), x1 - x0, spec)
    sx = lambda v: lin(v, lo, hi, x0, x1)
    g, y = [], 52
    # key: the series named once, in the same order as the bars
    kx = 0
    for i, s in enumerate(series):
        cls = SERIES[i][0] + (' ihd-hatch' if i == 2 else '')
        g.append(f'<rect class="{cls}" x="{kx}" y="14" width="16" height="16"/>')
        g.append(text(kx + 24, 28, s['name']))
        kx += 24 + tw(s['name']) + 28
    for ci, cat in enumerate(cats):
        label, lines = lines_text(column, y + 16, cat, column, anchor='end')
        g.append(label)
        if stacked:
            cursor = 0
            for i, s in enumerate(series):
                v = s['values'][ci]
                if v > 0:
                    cls = SERIES[i][0] + (' ihd-hatch' if i == 2 else '')
                    g.append(f'<rect class="{cls}" x="{sx(cursor):.1f}" y="{y}" width="{sx(cursor + v) - sx(cursor):.1f}" height="22"/>')
                    width = sx(cursor + v) - sx(cursor)
                    if width >= tw(fmt(spec, v), True) + 6:
                        g.append(text((sx(cursor) + sx(cursor + v)) / 2, y + 42, fmt(spec, v), 'ihd-chart-value', 'middle'))
                cursor += v
            g.append(text(sx(totals[ci]) + 10, y + 17, fmt(spec, totals[ci]), 'ihd-chart-value'))
            y += 66
        else:
            for i, s in enumerate(series):
                v = s['values'][ci]
                cls = SERIES[i][0] + (' ihd-hatch' if i == 2 else '')
                g.append(f'<rect class="{cls}" x="{x0}" y="{y + i * 26}" width="{max(sx(v) - x0, 0):.1f}" height="18"/>')
                g.append(text(sx(v) + 8, y + i * 26 + 15, fmt(spec, v), 'ihd-chart-value'))
            y += len(series) * 26 + 18
    g.append(f'<path class="ihd-axis" d="M{x0} 42V{y - 8}"/>')
    axis_y = y
    g.append(f'<path class="ihd-axis" d="M{x0} {axis_y}H{x1}"/>')
    for t in ticks:
        g.append(f'<path class="ihd-axis" d="M{sx(t):.1f} {axis_y}v6"/>')
        g.append(text(sx(t), axis_y + 26, fmt(spec, t), 'ihd-chart-value', 'middle'))
    g.append(unit_note(spec, x1, axis_y + 52))
    head = [spec.get('category_label', 'Category')] + [s['name'] for s in series] + (['Total'] if stacked else [])
    rows = [[cat] + [fmt(spec, s['values'][i]) for s in series] + ([fmt(spec, totals[i])] if stacked else []) for i, cat in enumerate(cats)]
    desc = '; '.join(f'{cat}: ' + ', '.join(f'{s["name"]} {fmt(spec, s["values"][i])}' for s in series) for i, cat in enumerate(cats))
    return ''.join(g), axis_y + (62 if spec.get('unit') else 40), table(spec['title'], head, rows), desc


def r_line(spec):
    series = need_list(spec, 'series', 1, 3)
    xs = need_list(spec, 'x', 2)
    for s in series:
        if len(s.get('values', [])) != len(xs):
            raise ChartError(f'Series "{s.get("name")}" needs {len(xs)} values')
        for v in s['values']:
            need_num(v, f'"{s.get("name")}" value')
    numeric = all(isnum(x) for x in xs)
    allv = [v for s in series for v in s['values']]
    right = min(max(tw(s['name']) for s in series), 140) + 30
    top, bottom = 52, 64
    height = spec.get('height', 300)
    x0, x1 = 78, W - right
    ph = height - top - bottom
    ticks, lo, hi = axis_ticks(min(allv), max(allv), ph * 1.6, spec, zero=spec.get('zero', True))
    sy = lambda v: lin(v, lo, hi, top + ph, top)
    if numeric:
        sxv = lambda v: lin(v, xs[0], xs[-1], x0 + 10, x1 - 10)
    else:
        sxv = lambda v: lin(xs.index(v), 0, len(xs) - 1, x0 + 10, x1 - 10)
    g = [text(x0, 24, spec.get('y_label', spec['title']))]
    g.append(f'<path class="ihd-axis" d="M{x0} {top}V{top + ph}H{x1}"/>')
    for t in ticks:
        g.append(f'<path class="ihd-axis" d="M{x0 - 6} {sy(t):.1f}h6"/>')
        g.append(text(x0 - 12, sy(t) + 5, fmt(spec, t), 'ihd-chart-value', 'end'))
    xpos = [sxv(x) for x in xs]
    for i, x in enumerate(xs):
        label = fmt({}, x) if numeric else str(x)
        if i and xpos[i] - xpos[i - 1] < tw(label, numeric) + 10:
            raise ChartError('x labels touch; use fewer points or shorter labels')
        g.append(f'<path class="ihd-axis" d="M{xpos[i]:.1f} {top + ph}v6"/>')
        g.append(text(xpos[i], top + ph + 28, label, 'ihd-chart-value', 'middle'))
    if spec.get('x_label'):
        g.append(text(x1, top + ph + 54, spec['x_label'], 'ihd-chart-label ihd-svg-muted', 'end'))
    ends = []
    for i, s in enumerate(series):
        tone, dash, mark = SERIES[i]
        heavy = ' ihd-emph' if spec.get('emph') == s['name'] else ''
        pts = ' '.join(f'{xpos[j]:.1f},{sy(v):.1f}' for j, v in enumerate(s['values']))
        g.append(f'<polyline class="ihd-line {dash} {tone}{heavy}" points="{pts}"/>'.replace('  ', ' '))
        g.append(f'<g class="{tone}">' + ''.join(marker(mark, xpos[j], sy(v), tone) for j, v in enumerate(s['values'])) + '</g>')
        ends.append(sy(s['values'][-1]))
    placed = spread(ends, 24, top + 6, top + ph)
    for i, s in enumerate(series):
        label, _ = lines_text(x1 + 10, placed[i] + 5, s['name'], right - 20)
        g.append(label)
    head = [spec.get('x_label', 'x')] + [s['name'] for s in series]
    rows = [[fmt({}, x) if numeric else x] + [fmt(spec, s['values'][j]) for s in series] for j, x in enumerate(xs)]
    desc = '; '.join(f'{s["name"]} runs from {fmt(spec, s["values"][0])} to {fmt(spec, s["values"][-1])}' for s in series)
    return ''.join(g), height, table(spec['title'], head, rows), desc


def r_range(spec):
    items = need_list(spec, 'items')
    for it in items:
        for key in ('low', 'base', 'high'):
            need_num(it.get(key), f'"{it.get("label")}" {key}')
        if not it['low'] <= it['base'] <= it['high']:
            raise ChartError(f'"{it["label"]}" needs low <= base <= high')
    column = label_column([i['label'] for i in items])
    x0, x1 = column + 70, W - 70
    ticks, lo, hi = axis_ticks(min(i['low'] for i in items), max(i['high'] for i in items), x1 - x0, spec, zero=spec.get('zero', True))
    sx = lambda v: lin(v, lo, hi, x0, x1)
    g, y = [], 20
    for it in items:
        cy = y + 30
        heavy = spec.get('emph') == it['label']
        tone = 'ihd-s1' if heavy or not spec.get('emph') else 'ihd-s2'
        label, _ = lines_text(column, cy + 5, it['label'], column, anchor='end')
        g.append(label)
        g.append(f'<path class="ihd-line {tone}{" ihd-emph" if heavy else ""}" d="M{sx(it["low"]):.1f} {cy}H{sx(it["high"]):.1f}"/>')
        for v in (it['low'], it['high']):
            g.append(f'<path class="ihd-axis" d="M{sx(v):.1f} {cy - 9}v18"/>')
        g.append(marker('ihd-m-diamond', sx(it['base']), cy, 'ihd-s1', 18))
        g.append(text(sx(it['low']) - 12, cy + 5, fmt(spec, it['low']), 'ihd-chart-value', 'end'))
        g.append(text(sx(it['high']) + 12, cy + 5, fmt(spec, it['high']), 'ihd-chart-value'))
        g.append(text(sx(it['base']), cy - 16, fmt(spec, it['base']), 'ihd-chart-value', 'middle', ' style="font-weight:650"'))
        y += 64
    axis_y = y + 4
    g.append(f'<path class="ihd-axis" d="M{x0} {axis_y}H{x1}"/>')
    for t in ticks:
        g.append(f'<path class="ihd-axis" d="M{sx(t):.1f} {axis_y}v6"/>')
        g.append(text(sx(t), axis_y + 26, fmt(spec, t), 'ihd-chart-value', 'middle'))
    g.append(unit_note(spec, x1, axis_y + 52))
    rows = [[i['label'], fmt(spec, i['low']), fmt(spec, i['base']), fmt(spec, i['high'])] for i in items]
    desc = '; '.join(f'{i["label"]}: {fmt(spec, i["low"])} to {fmt(spec, i["high"])}, base {fmt(spec, i["base"])}' for i in items)
    return ''.join(g), axis_y + (62 if spec.get('unit') else 40), table(spec['title'], [spec.get('item_label', 'Item'), 'Low', 'Base', 'High'], rows), desc


def r_tornado(spec):
    base = need_num(spec.get('base'), '"base"')
    items = need_list(spec, 'items')
    for it in items:
        for key in ('low', 'high'):
            need_num(it.get(key), f'"{it.get("label")}" {key}')
    items = sorted(items, key=lambda i: -abs(i['high'] - i['low']))
    left, right = 150, 150
    x0, x1 = left, W - right
    lows = [min(i['low'], i['high'], base) for i in items]
    highs = [max(i['low'], i['high'], base) for i in items]
    ticks, lo, hi = axis_ticks(min(lows), max(highs), x1 - x0, spec, zero=False)
    sx = lambda v: lin(v, lo, hi, x0, x1)
    g, y = [], 44
    top_y = y - 8
    for rank, it in enumerate(items):
        tone = 'ihd-s1' if rank == 0 else 'ihd-s2'
        g.append(text(0, y + 16, it['label'], 'ihd-chart-label'))
        by = y + 30
        for key, anchor_start in (('low', True), ('high', False)):
            v = it[key]
            a, b = sorted((sx(base), sx(v)))
            g.append(f'<rect class="{tone}" x="{a:.1f}" y="{by}" width="{max(b - a, 1):.1f}" height="18"/>')
        # each end: the outcome, then the input that produced it
        for key in ('low', 'high'):
            v = it[key]
            outward_left = v < base
            ex = sx(v) + (-10 if outward_left else 10)
            anchor = 'end' if outward_left else 'start'
            g.append(text(ex, by + 14, fmt(spec, v), 'ihd-chart-value', anchor))
            case = it.get(f'{key}_case')
            if case:
                lbl, _ = lines_text(ex, by + 34, case, 140, 'ihd-chart-label ihd-svg-muted', anchor, 18)
                g.append(lbl)
        y += 76
    g.append(f'<path class="ihd-axis" d="M{sx(base):.1f} {top_y}V{y - 12}"/>')
    g.append(text(sx(base), top_y - 8, f'Base {fmt(spec, base)}', 'ihd-chart-label', 'middle', ' style="font-weight:650"'))
    axis_y = y
    g.append(f'<path class="ihd-axis" d="M{x0} {axis_y}H{x1}"/>')
    for t in ticks:
        g.append(f'<path class="ihd-axis" d="M{sx(t):.1f} {axis_y}v6"/>')
        g.append(text(sx(t), axis_y + 26, fmt(spec, t), 'ihd-chart-value', 'middle'))
    g.append(unit_note(spec, x1, axis_y + 52))
    rows = []
    for it in items:
        cell = lambda key: fmt(spec, it[key]) + (f' ({it[key + "_case"]})' if it.get(key + '_case') else '')
        rows.append([it['label'], cell('low'), cell('high')])
    desc = f'Base {fmt(spec, base)}. ' + '; '.join(f'{i["label"]} moves it from {fmt(spec, i["low"])} to {fmt(spec, i["high"])}' for i in items)
    return ''.join(g), axis_y + (62 if spec.get('unit') else 40) + 14, table(spec['title'], [spec.get('item_label', 'Assumption'), 'Outcome at low case', 'Outcome at high case'], rows), desc


def r_waterfall(spec):
    steps = need_list(spec, 'steps', 2)
    running, bars = 0.0, []
    for k, st in enumerate(steps):
        v = need_num(st.get('value'), f'"{st.get("label")}" value')
        if st.get('kind', 'total' if k == 0 else 'delta') == 'total':
            if k and abs(running - v) > 1e-9:
                raise ChartError(f'Total "{st["label"]}" is {num(v)} but the steps before it add to {num(running)}')
            bars.append(('total', 0.0, v))
            running = v
        else:
            bars.append(('up' if v >= 0 else 'down', running, running + v))
            running += v
    column = label_column([s['label'] for s in steps])
    x0, x1 = column + 24, W - 90
    ends = [b[1] for b in bars] + [b[2] for b in bars]
    ticks, lo, hi = axis_ticks(min(ends), max(ends), x1 - x0, spec)
    sx = lambda v: lin(v, lo, hi, x0, x1)
    g, y = [], 18
    prev = None
    for st, (kind, a, b) in zip(steps, bars):
        cy = y + 14
        label, _ = lines_text(column, cy + 5, st['label'], column, anchor='end')
        g.append(label)
        left, right_ = sorted((sx(a), sx(b)))
        cls = {'total': 'ihd-shape', 'up': 'ihd-s2', 'down': 'ihd-hatch'}[kind]
        g.append(f'<rect class="{cls}" x="{left:.1f}" y="{y}" width="{max(right_ - left, 1):.1f}" height="28"/>')
        if prev is not None:
            g.append(f'<path class="ihd-connector" d="M{sx(prev):.1f} {y - 14}V{y}"/>')
        label_text = fmt(spec, b, False) if kind == 'total' else fmt(spec, b - a, True)
        if b >= a:
            g.append(text(right_ + 10, cy + 5, label_text, 'ihd-chart-value'))
        else:
            g.append(text(left - 10, cy + 5, label_text, 'ihd-chart-value', 'end'))
        prev = b
        y += 52
    axis_y = y
    g.append(f'<path class="ihd-axis" d="M{x0} {axis_y}H{x1}"/>')
    g.append(f'<path class="ihd-axis" d="M{sx(0):.1f} 8V{axis_y}"/>')
    for t in ticks:
        g.append(f'<path class="ihd-axis" d="M{sx(t):.1f} {axis_y}v6"/>')
        g.append(text(sx(t), axis_y + 26, fmt(spec, t), 'ihd-chart-value', 'middle'))
    g.append(unit_note(spec, x1, axis_y + 52))
    rows = []
    for st, (kind, a, b) in zip(steps, bars):
        rows.append([st['label'], fmt(spec, b) if kind == 'total' else fmt(spec, b - a, True), fmt(spec, b)])
    desc = '; '.join(f'{st["label"]} {fmt(spec, bar[2] - bar[1], True) if bar[0] != "total" else fmt(spec, bar[2])}' for st, bar in zip(steps, bars))
    return ''.join(g), axis_y + (62 if spec.get('unit') else 40), table(spec['title'], [spec.get('item_label', 'Step'), 'Change', 'Running total'], rows), desc


def r_slope(spec):
    items = need_list(spec, 'items', 2, 9)
    for it in items:
        need_num(it.get('before'), f'"{it.get("label")}" before')
        need_num(it.get('after'), f'"{it.get("label")}" after')
    vals = [v for it in items for v in (it['before'], it['after'])]
    top, ph = 56, 60 + 44 * len(items)
    lo, hi = min(vals), max(vals)
    if lo == hi:
        hi = lo + 1
    pad = (hi - lo) * .05
    sy = lambda v: lin(v, lo - pad, hi + pad, top + ph, top)
    xa, xb = 130, 330
    g = [text(xa, 28, spec.get('before_label', 'Before'), anchor='middle'), text(xb, 28, spec.get('after_label', 'After'), anchor='middle')]
    g.append(f'<path class="ihd-axis" d="M{xa} {top - 8}V{top + ph + 8}M{xb} {top - 8}V{top + ph + 8}"/>')
    placed_r = spread([sy(it['after']) for it in items], 24, top, top + ph)
    placed_l = spread([sy(it['before']) for it in items], 24, top, top + ph)
    for it, yl, yr in zip(items, placed_l, placed_r):
        heavy = spec.get('emph') == it['label']
        tone = 'ihd-s1' if heavy or not spec.get('emph') else 'ihd-s3'
        g.append(f'<path class="ihd-line {tone}{" ihd-emph" if heavy else ""}" d="M{xa} {sy(it["before"]):.1f}L{xb} {sy(it["after"]):.1f}"/>')
        g.append(marker('ihd-m-circle', xa, sy(it['before']), tone, 12))
        g.append(marker('ihd-m-circle', xb, sy(it['after']), tone, 12))
        g.append(text(xa - 14, yl + 5, fmt(spec, it['before']), 'ihd-chart-value', 'end'))
        lbl, _ = lines_text(xb + 14, yr + 5, f'{fmt(spec, it["after"])}  {it["label"]}', W - xb - 24)
        g.append(lbl)
    g.append(unit_note(spec, W - 10, top + ph + 40))
    rows = [[it['label'], fmt(spec, it['before']), fmt(spec, it['after']), fmt(spec, it['after'] - it['before'], True)] for it in items]
    desc = '; '.join(f'{it["label"]} goes from {fmt(spec, it["before"])} to {fmt(spec, it["after"])}' for it in items)
    return ''.join(g), top + ph + (56 if spec.get('unit') else 24), table(spec['title'], [spec.get('item_label', 'Item'), spec.get('before_label', 'Before'), spec.get('after_label', 'After'), 'Change'], rows), desc


def overlaps(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def r_scatter(spec, quadrants=False):
    pts = need_list(spec, 'points', 1, 12)
    for p in pts:
        need_num(p.get('x'), f'"{p.get("label")}" x')
        need_num(p.get('y'), f'"{p.get("label")}" y')
    x0, x1, top, ph = 92, W - 34, 44, 330
    def padded(values):
        low, high = min(values), max(values)
        margin = (high - low) * .08 or 1
        return low - margin, high + margin
    xt, xlo, xhi = axis_ticks(*padded([p['x'] for p in pts]), x1 - x0, spec.get('x_format', {}), zero=spec.get('zero_x', False))
    yt, ylo, yhi = axis_ticks(*padded([p['y'] for p in pts]), ph * 1.5, spec.get('y_format', {}), zero=spec.get('zero_y', False))
    xf, yf = spec.get('x_format', {}), spec.get('y_format', {})
    sx = lambda v: lin(v, xlo, xhi, x0, x1)
    sy = lambda v: lin(v, ylo, yhi, top + ph, top)
    g = [text(x0, 24, spec.get('y_label', 'y'))]
    g.append(f'<path class="ihd-axis" d="M{x0} {top}V{top + ph}H{x1}"/>')
    for t in yt:
        g.append(f'<path class="ihd-axis" d="M{x0 - 6} {sy(t):.1f}h6"/>')
        g.append(text(x0 - 12, sy(t) + 5, fmt(yf, t), 'ihd-chart-value', 'end'))
    for t in xt:
        g.append(f'<path class="ihd-axis" d="M{sx(t):.1f} {top + ph}v6"/>')
        g.append(text(sx(t), top + ph + 28, fmt(xf, t), 'ihd-chart-value', 'middle'))
    g.append(text(x1, top + ph + 54, spec.get('x_label', 'x'), 'ihd-chart-label ihd-svg-muted', 'end'))
    obstacles = []
    if quadrants:
        names = spec.get('quadrants') or {}
        mx = spec.get('mid_x', (xlo + xhi) / 2)
        my = spec.get('mid_y', (ylo + yhi) / 2)
        g.append(f'<path class="ihd-connector" d="M{sx(mx):.1f} {top}V{top + ph}M{x0} {sy(my):.1f}H{x1}"/>')
        corners = {'tl': (x0 + 10, top + 22, 'start'), 'tr': (x1 - 10, top + 22, 'end'), 'bl': (x0 + 10, top + ph - 12, 'start'), 'br': (x1 - 10, top + ph - 12, 'end')}
        for key, (qx, qy, anchor) in corners.items():
            if names.get(key):
                width = tw(names[key])
                rect = (qx - width if anchor == 'end' else qx, qy - 16, qx if anchor == 'end' else qx + width, qy + 4)
                obstacles.append(rect)
                g.append(text(qx, qy, names[key], 'ihd-chart-label ihd-svg-muted', anchor))
    for p in pts:
        px, py = sx(p['x']), sy(p['y'])
        obstacles.append((px - 9, py - 9, px + 9, py + 9))
    for p in pts:
        px, py = sx(p['x']), sy(p['y'])
        heavy = spec.get('emph') == p['label']
        tone = 'ihd-s1' if heavy or not spec.get('emph') else 'ihd-s2'
        g.append(marker('ihd-m-diamond' if heavy else 'ihd-m-circle', px, py, tone, 20 if heavy else 14))
        width = tw(p['label'])
        options = [('start', px + 14, py + 5), ('end', px - 14, py + 5), ('middle', px, py - 16), ('middle', px, py + 28)]
        for anchor, lx, ly in options:
            left = lx if anchor == 'start' else lx - width if anchor == 'end' else lx - width / 2
            rect = (left, ly - 15, left + width, ly + 5)
            inside = rect[0] >= 0 and rect[2] <= W and rect[1] >= top - 6 and rect[3] <= top + ph + 4
            own = (px - 9, py - 9, px + 9, py + 9)
            if inside and not any(overlaps(rect, o) for o in obstacles if o != own):
                obstacles.append(rect)
                g.append(text(lx, ly, p['label'], 'ihd-chart-label', anchor))
                break
        else:
            raise ChartError(f'Label "{p["label"]}" collides with others; spread the points, shorten the label or drop a point')
    rows = [[p['label'], fmt(xf, p['x']), fmt(yf, p['y'])] for p in pts]
    desc = '; '.join(f'{p["label"]} at {fmt(xf, p["x"])}, {fmt(yf, p["y"])}' for p in pts)
    return ''.join(g), top + ph + 66, table(spec['title'], [spec.get('item_label', 'Point'), spec.get('x_label', 'x'), spec.get('y_label', 'y')], rows), desc


def r_bar(spec):
    items = need_list(spec, 'items')
    for it in items:
        need_num(it.get('value'), f'"{it.get("label")}" value')
        if it['value'] < 0:
            raise ChartError('Bars start at zero; use a range or waterfall for negative values')
    top = spec.get('max', max(i['value'] for i in items))
    if top <= 0:
        raise ChartError('Bars need a positive maximum')
    emph = spec.get('emph')
    rows = []
    for it in items:
        cls = 'ihd-bar'
        if it.get('assumed'):
            cls += ' ihd-bar--muted'
        elif emph and it['label'] != emph:
            cls += ' ihd-bar--quiet'
        value = fmt(spec, it['value']) + (f' {spec["unit"]}' if spec.get('unit') else '')
        rows.append(f'<div class="ihd-bar-row"><span>{esc(it["label"])}</span><div class="ihd-track"><div class="{cls}" style="width:{min(it["value"] / top * 100, 100):.3f}%"></div></div><span>{esc(value)}</span></div>')
    desc = '; '.join(f'{i["label"]} {fmt(spec, i["value"])}' for i in items)
    return ''.join(rows), None, '', desc


BUILDERS = {
    'grouped': lambda s: r_grouped(s),
    'stacked': lambda s: r_grouped(s, True),
    'line': r_line, 'range': r_range, 'tornado': r_tornado, 'waterfall': r_waterfall, 'slope': r_slope,
    'scatter': lambda s: r_scatter(s), 'matrix': lambda s: r_scatter(s, True),
}


def render(spec, n=1):
    if not isinstance(spec, dict):
        raise ChartError('A chart spec must be a JSON object')
    kind = spec.get('type')
    if kind not in TYPES:
        raise ChartError(f'Unknown chart type {kind!r}; use one of {", ".join(TYPES)}')
    if not str(spec.get('caption', '')).strip():
        raise ChartError('Every chart needs a caption that states what to notice')
    if not str(spec.get('title', '')).strip():
        raise ChartError('Every chart needs a title')
    ident = f'ihd-chart-{n}'
    title = f'<p class="ihd-figure-title">{esc(spec["title"])}</p>'
    caption = f'<figcaption id="{ident}-caption">{esc(spec["caption"])}</figcaption>'
    if kind == 'bar':
        rows, _, _, _ = r_bar(spec)
        return f'<figure class="ihd-figure" aria-labelledby="{ident}-caption">{title}{rows}{caption}</figure>'
    if spec.get('facets'):
        raise ChartError('facets is not supported yet; write one chart per panel on a shared "max"')
    svg, height, tab, desc = BUILDERS[kind](spec)
    description = spec.get('description') or desc
    height = int(math.ceil(height))
    svg = (f'<svg class="ihd-diagram-wide" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-labelledby="{ident}-title {ident}-desc">'
           f'<title id="{ident}-title">{esc(spec["title"])}</title><desc id="{ident}-desc">{esc(description)}</desc>{svg}</svg>')
    return f'<figure class="ihd-figure" aria-labelledby="{ident}-caption">{title}<div class="ihd-visual">{svg}{tab}</div>{caption}</figure>'


def expand(source):
    """Replace every placeholder in `source`. Raises ChartError for a bad spec or a missing sprite."""
    count = [0]

    def one(match):
        count[0] += 1
        try:
            spec = json.loads(match.group(1))
        except json.JSONDecodeError as error:
            raise ChartError(f'Chart {count[0]} is not valid JSON: {error}')
        try:
            return render(spec, count[0])
        except ChartError as error:
            raise ChartError(f'Chart {count[0]} ({spec.get("title", "untitled")}): {error}')

    output = PLACEHOLDER.sub(one, source)
    if 'data-ihd-chart' in output:
        raise ChartError('A data-ihd-chart placeholder is malformed; use <div data-ihd-chart><script type="application/json">...</script></div>')
    if count[0] and 'class="ihd-sprite"' not in output:
        raise ChartError('Charts use markers and hatching: copy the ihd-sprite block from assets/starter.html into the document')
    return output


def main(argv):
    if len(argv) != 2 or argv[1] in ('-h', '--help'):
        print(__doc__)
        return 0 if len(argv) == 2 else 2
    try:
        print(render(json.loads(Path(argv[1]).read_text()), 1))
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
