# Refresh an old showcase/report to the latest template engine.
# Usage: python refresh_engine.py <html-path> [--no-backup]
# Detects layout from the aos-data island, injects it into the matching
# template asset, backs up the original to 05_CACHE, writes in place.
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ASSETS = 'D:/AOS/.dsh/skills/research-showcase/assets'
BAK_DIR = 'D:/AOS/05_CACHE/quicktasks/20261112_viz-showcase-prototype/backups'
PATTERN = re.compile(r'(<script type="application/json" id="aos-data">)(.*?)(</script>)', re.S)


def main():
    if len(sys.argv) < 2:
        print('usage: python refresh_engine.py <html-path> [--no-backup]')
        sys.exit(2)
    path = sys.argv[1]
    nobackup = '--no-backup' in sys.argv
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    m = PATTERN.search(html)
    if not m:
        print('ERROR: aos-data island not found in', path)
        sys.exit(1)
    island_raw = m.group(2)
    data = json.loads(island_raw)
    layout = (data.get('meta', {}) or {}).get('layout') or ('cardwall' if '_showcase' in path else 'report')
    tpl_name = 'cardwall.template.html' if layout == 'cardwall' else 'report.template.html'
    tpl_path = os.path.join(ASSETS, tpl_name)
    with open(tpl_path, 'r', encoding='utf-8') as f:
        tpl = f.read()
    if not nobackup:
        os.makedirs(BAK_DIR, exist_ok=True)
        base = os.path.splitext(os.path.basename(path))[0]
        bak = os.path.join(BAK_DIR, base + '_pre_v1.6.1_' + str(int(__import__('time').time())) + '.html')
        shutil.copyfile(path, bak)
        print('backup:', bak)
    island = json.dumps(data, ensure_ascii=False, indent=2).replace('</script', '<\\/script')
    new_html, n = PATTERN.subn(lambda mm: mm.group(1) + '\n' + island + '\n  ' + mm.group(3), tpl, count=1)
    assert n == 1
    json.loads(PATTERN.search(new_html).group(2))  # sanity
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_html)
    print('OK: %s refreshed on %s engine (%d bytes)' % (os.path.basename(path), tpl_name, len(new_html.encode('utf-8'))))
    print('next: run qa_smoke.py + impeccable detect on the file, then build_index.py')


if __name__ == '__main__':
    main()
