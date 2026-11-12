# Layout-aware smoke QA for any showcase page generated from the template family.
# Usage: python qa_smoke.py <absolute-path-to-html>
# Auto-detects layout: cardwall (article.card) vs report (.rpt-h).
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

if len(sys.argv) < 2:
    print('usage: python qa_smoke.py <absolute-path-to-html>')
    sys.exit(2)
HTML = sys.argv[1].replace('\\', '/')
URL = 'file:///' + HTML.lstrip('/')
failures = []

def check(name, cond, extra=''):
    ok = bool(cond)
    if not ok:
        failures.append(name)
    print(('PASS' if ok else 'FAIL') + ' | ' + name + ((' | ' + str(extra)) if extra else ''))

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox', '--disable-gpu'])
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    console_errors = []
    page.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: console_errors.append(str(e)))

    page.goto(URL, wait_until='load')
    page.wait_for_timeout(600)

    title = page.title()
    check('title rendered', '加载中' not in title, title)
    layout = 'cardwall' if page.locator('article.card').count() > 0 else ('report' if page.locator('.rpt-h').count() > 0 else 'unknown')
    check('layout detected', layout in ('cardwall', 'report'), layout)

    # ── 公共：字号 / 工具条 / 主题 ──
    fs = page.evaluate('getComputedStyle(document.documentElement).fontSize')
    check('default font-size 17px', fs == '17px', fs)
    page.locator('#fsPlus').click(); page.wait_for_timeout(120)
    fs = page.evaluate('getComputedStyle(document.documentElement).fontSize')
    check('A+ steps up', fs == '19px', fs)
    page.locator('#fsMinus').click(); page.wait_for_timeout(120)
    fs = page.evaluate('getComputedStyle(document.documentElement).fontSize')
    check('A- back to 17px', fs == '17px', fs)
    check('edge rail visible', page.locator('.edge-rail').is_visible())
    check('back-top always visible', page.locator('#backTop').is_visible())

    # ── 主题：默认浅色 + 右下按钮切换 + 持久化（v1.4 F5）──
    page.evaluate('localStorage.removeItem("aos-showcase-theme")')
    page.reload(wait_until='load'); page.wait_for_timeout(500)
    bg = page.evaluate('getComputedStyle(document.body).backgroundColor')
    check('light theme default (bg #F3F4F6)', bg == 'rgb(243, 244, 246)', bg)
    page.locator('#themeBtn').click(); page.wait_for_timeout(250)
    bgt = page.evaluate('getComputedStyle(document.body).backgroundColor')
    check('theme button flips to dark', bgt == 'rgb(2, 6, 23)', bgt)
    check('theme persists to localStorage', page.evaluate('localStorage.getItem("aos-showcase-theme")') == 'dark')
    n_after_dark = page.locator('article.card').count() if layout == 'cardwall' else page.locator('.rpt-h').count()
    check('content survives theme flip', n_after_dark >= 1, 'got %s' % n_after_dark)
    page.locator('#themeBtn').click(); page.wait_for_timeout(250)
    bgl = page.evaluate('getComputedStyle(document.body).backgroundColor')
    check('theme toggles back to light', bgl == 'rgb(243, 244, 246)', bgl)
    page.evaluate('localStorage.removeItem("aos-showcase-theme")')

    if layout == 'cardwall':
        cards = page.locator('article.card').count()
        check('cards rendered >= 1', cards >= 1, 'got %d' % cards)
        check('stats band exists', page.locator('#statsBand').count() == 1)
        pos = page.evaluate('getComputedStyle(document.querySelector(".toolbar-wrap")).position')
        check('toolbar NOT sticky (v1.3)', pos == 'static', pos)
        chips = page.locator('#statusChips .chip:not(.reset):not(.more-chip)').count()
        sdefs = page.evaluate('JSON.parse(document.getElementById("aos-data").textContent).status_def.length')
        cap_ok = chips <= max(6, 0) or sdefs <= 6 or page.locator('#statusChips .more-chip').count() == 1
        check('status chips capped at 6 when over', cap_ok, '%d defs, %d chips' % (sdefs, chips))
        tags_total = page.evaluate("""
        (() => { const d = JSON.parse(document.getElementById('aos-data').textContent);
          const t = {}; (d.items||[]).forEach(i => (i.tags||[]).forEach(x => t[x]=1)); return Object.keys(t).length; })()
        """)
        tag_chips = page.locator('#tagChips .chip.tagchip').count()
        if tags_total > 8:
            check('tag chips capped at 8 when over', tag_chips <= 8 and page.locator('#tagChips .more-chip').count() == 1, '%d tags -> %d chips' % (tags_total, tag_chips))
        page.locator('[data-status]').first.click(); page.wait_for_timeout(250)
        n = page.locator('article.card').count()
        check('status filter works', n >= 1, 'got %d' % n)
        page.locator('#resetBtn').click(); page.wait_for_timeout(250)
        check('reset restores', page.locator('article.card').count() == cards)
        page.fill('#q', 'zzzzz-no-match-qa'); page.wait_for_timeout(300)
        check('empty state visible', page.locator('.empty').is_visible())
        page.locator('#resetBtn2').click(); page.wait_for_timeout(250)
        check('empty reset restores', page.locator('article.card').count() == cards)
        if page.locator('.more-btn').count() > 0:
            page.locator('.more-btn').first.click(); page.wait_for_timeout(150)
            check('expand panel opens', page.locator('article.card.open .more-panel').first.is_visible())
        page.evaluate('document.body.focus()')
        page.keyboard.press('/')
        check('/ focuses search', page.evaluate('document.activeElement.id') == 'q')
        page.keyboard.press('Escape')
        if page.locator('.grp-head').count() > 0:
            page.locator('.grp-head').first.click(); page.wait_for_timeout(150)
            check('section collapses', page.locator('section.grp.collapsed').count() == 1)
            page.locator('.grp-head').first.click(); page.wait_for_timeout(150)
    else:
        hs = page.locator('.rpt-h').count()
        check('headings rendered', hs >= 1, 'got %d' % hs)
        toc_links = page.locator('#toc a').count() if page.locator('#toc').count() else 0
        check('toc links == headings', toc_links == hs, '%d vs %d' % (toc_links, hs))
        # anchors resolve
        bad = page.evaluate("""
        [...document.querySelectorAll('#toc a')].filter(a => {
          const id = a.getAttribute('href').slice(1);
          return !document.getElementById(id);
        }).length
        """)
        check('toc anchors all resolve', bad == 0, '%d broken' % bad)
        check('stat tiles present', page.locator('.rpt-stats .tile').count() >= 1)
        check('table present', page.locator('.rpt-table').count() >= 1)
        check('callout present', page.locator('.callout').count() >= 1)
        check('md-lite bold works', page.locator('.rpt-p strong').count() >= 1)
        check('md-lite code works', page.locator('.rpt-p code, .rpt-li code').count() >= 1)
        _sample = bool(page.evaluate("JSON.parse(document.getElementById('aos-data').textContent).meta.sample"))
        check('sample badge iff meta.sample', ('SAMPLE' in page.locator('#metaBadges').text_content()) == _sample, 'meta.sample=%s' % _sample)
        # v1.4：目录粘滞 / 图表 / 排序 / 筛选
        postoc = page.evaluate('getComputedStyle(document.querySelector(".toc")).position')
        check('toc is sticky sidebar', postoc == 'sticky', postoc)
        check('chart svg rendered', page.locator('.rpt-chart svg').count() >= 1)
        has_donut = page.evaluate('(JSON.parse(document.getElementById("aos-data").textContent).blocks||[]).some(b => b.t === "chart" && b.kind === "donut")')
        if has_donut:
            legend_txt = page.evaluate("[...document.querySelectorAll('.rpt-chart svg')].map(s => s.textContent).join(' ')") if page.locator('.rpt-chart svg').count() else ''
            check('donut legend in-svg with percent+base', '%' in legend_txt and '共' in legend_txt, legend_txt[:40])
        else:
            print('SKIP | donut legend (no donut chart in data)')
        fc_before = page.locator('.rpt-table tbody tr td').first.inner_text()
        page.evaluate('document.querySelector(".rpt-table th.sortable").scrollIntoView({block:"center",behavior:"instant"})')
        page.wait_for_timeout(700)
        page.locator('.rpt-table th.sortable').first.click(position={'x': 24, 'y': 21}); page.wait_for_timeout(200)
        aria = page.locator('.rpt-table th.sortable').first.get_attribute('aria-sort')
        check('table sort sets aria-sort', aria in ('ascending', 'descending'), aria)
        fc_after = page.locator('.rpt-table tbody tr td').first.inner_text()
        check('table sort reorders rows', fc_before != fc_after, '%s -> %s' % (fc_before, fc_after))
        outer = page.locator('.tbl-outer', has=page.locator('.tbl-filter'))
        if outer.count():
            o = outer.first
            tblf = o.locator('.rpt-table')
            kw = tblf.locator('tbody tr td').first.inner_text()[:4].strip()
            total = tblf.locator('tbody tr').count()
            o.locator('.tbl-filter input').fill(kw); page.wait_for_timeout(250)
            nrows = tblf.locator('tbody tr').count()
            check('table filter narrows rows', 1 <= nrows <= total, 'kw=%s %d -> %d' % (kw, total, nrows))
            o.locator('.reset-btn').click(); page.wait_for_timeout(250)
            check('table reset restores rows+order', tblf.locator('tbody tr').count() == total)
            check('table reset restores order', tblf.locator('tbody tr td').first.inner_text() == fc_before)
        # ── v1.5：设置面板 / 目录树 / 章节折叠 / 图表悬浮+排序 / 列筛选 ──
        page.locator('#setBtn').click(); page.wait_for_timeout(200)
        check('settings panel opens', page.locator('#settingsPop.open').count() == 1)
        page.locator('#setSec').select_option('collapse'); page.wait_for_timeout(250)
        check('secdef collapse applies live', page.locator('.sec.collapsed').count() >= 1, page.locator('.sec.collapsed').count())
        page.locator('#setSec').select_option('expand'); page.wait_for_timeout(250)
        check('secdef expand restores', page.locator('.sec.collapsed').count() == 0)
        page.keyboard.press('Escape'); page.wait_for_timeout(150)
        check('Esc closes settings', page.locator('#settingsPop.open').count() == 0)
        has_lv2 = page.evaluate('(JSON.parse(document.getElementById("aos-data").textContent).blocks||[]).some(b => b.t === "h" && b.level === 2)')
        if has_lv2:
            check('toc tree has lv2 entries', page.locator('.toc a.lv2').count() >= 1)
        else:
            print('SKIP | toc tree lv2 (no level:2 headings in data)')
        sec1 = page.locator('.sec').first
        sec1.locator('.rpt-h').first.click(); page.wait_for_timeout(200)
        check('section collapses on heading click', sec1.get_attribute('class').find('collapsed') >= 0)
        sec1.locator('.rpt-h').first.click(); page.wait_for_timeout(200)
        check('section expands again', sec1.get_attribute('class').find('collapsed') < 0)
        page.locator('.rpt-chart [data-t1]').first.hover(); page.wait_for_timeout(250)
        tipvis = page.locator('#chartTip').is_visible()
        check('chart hover tooltip appears', tipvis)
        if tipvis:
            tip_txt = (page.locator('#chartTip').text_content() or '').strip()
            check('chart tooltip has detail', len(tip_txt) > 8, tip_txt[:30])
        if page.locator('.csort').count():
            page.locator('.csort').first.click(); page.wait_for_timeout(200)
            check('chart sort toggles', '降序' in page.locator('.csort').first.text_content())
        tbl1 = page.locator('.rpt-table').first
        th_cf = tbl1.locator('th .cf-btn').first
        th_cf.click(); page.wait_for_timeout(250)
        check('column filter popup opens', page.locator('#cfPop.open').count() == 1)
        total_all = tbl1.locator('tbody tr').count()
        page.locator('#cfPop input[type=checkbox]').first.click(); page.wait_for_timeout(250)
        n_col = tbl1.locator('tbody tr').count()
        check('column filter narrows rows', n_col < total_all, '%d -> %d' % (total_all, n_col))
        page.locator('#cfPop [data-cf=all]').click(); page.wait_for_timeout(250)
        check('column filter select-all restores', tbl1.locator('tbody tr').count() == total_all)
        page.locator('body').click(position={'x': 40, 'y': 300}); page.wait_for_timeout(200)
        check('column popup closes on outside click', page.locator('#cfPop.open').count() == 0)
        # ── v1.6：布局/宽度设置 + timeline/flow/mindmap ──
        has_tl = page.evaluate('(JSON.parse(document.getElementById("aos-data").textContent).blocks||[]).some(b => ["timeline","flow","mindmap"].indexOf(b.t) >= 0)')
        if has_tl:
            _svg_count = page.locator('.rpt-chart .scrollx svg').count()
            _mm_count = page.locator('.mm-wrap').count()
            _tl_types = page.evaluate('(JSON.parse(document.getElementById("aos-data").textContent).blocks||[]).filter(b => ["timeline","flow","mindmap"].indexOf(b.t) >= 0).length')
            check('timeline/flow/mindmap rendered', _svg_count + _mm_count >= _tl_types, 'svg=%d mm=%d expected=%d' % (_svg_count, _mm_count, _tl_types))
        page.locator('#setBtn').click(); page.wait_for_timeout(200)
        page.locator('#setLayout').select_option('side'); page.wait_for_timeout(200)
        check('layout side mode applies', page.evaluate('document.body.classList.contains("lay-side")'))
        page.evaluate('document.getElementById("setWidth").value = 800; document.getElementById("setWidth").dispatchEvent(new Event("input"));'); page.wait_for_timeout(200)
        _wv = page.evaluate('document.getElementById("setWidth").value')
        _ls = page.evaluate('localStorage.getItem("aos-showcase-width-px")')
        _actual = page.evaluate('document.querySelector(".rpt-main").getBoundingClientRect().width')
        check('width slider px applies', _wv == '800' and _ls == '800' and _actual < 900, 'input=%s ls=%s actual=%.0fpx' % (_wv, _ls, _actual))
        page.locator('#setLayout').select_option('center')
        page.evaluate('document.getElementById("setWidth").value = 1100; document.getElementById("setWidth").dispatchEvent(new Event("input"));')
        page.wait_for_timeout(200)
        check('layout prefs revert', not page.evaluate('document.body.classList.contains("lay-side")') and not page.evaluate('document.body.classList.contains("w-wide")'))
        page.evaluate('localStorage.removeItem("aos-showcase-layout"); localStorage.removeItem("aos-showcase-width")')

    # ── 移动端 ──
    page.set_viewport_size({'width': 375, 'height': 800}); page.wait_for_timeout(300)
    delta = page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
    check('375px no horizontal overflow', delta <= 1, 'delta %spx' % delta)

    check('no console errors', len(console_errors) == 0, ' ;; '.join(console_errors)[:400])
    browser.close()

print('ALL PASS' if not failures else '%d FAILURES: %s' % (len(failures), ', '.join(failures)))
sys.exit(0 if not failures else 1)
