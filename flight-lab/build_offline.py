"""Update viewer code in the existing offline bundle; preserve safe source exports."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import os


ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'downloads/MH370_Flight_Dynamics_Lab_v1.zip'
START = '/* Saved-state navigation: numbered records and a separate terminal scale. */'
END = '/* The Atlas desktop rack occupies 214px.'
NOTE_START = '<!-- PLAYBACK_CONTEXT_REPAIR -->'
NOTE_END = '<!-- END_PLAYBACK_CONTEXT_REPAIR -->'


def build():
    with ZipFile(ARCHIVE) as old:
        entries = [(entry, old.read(entry.filename)) for entry in old.infolist()]
    original = {entry.filename: data for entry, data in entries}
    css = (ROOT / 'assets/win98.css').read_text()
    controls = css[css.index(START):css.index(END)].replace('#flight-lab-app ', '')
    controls = ':root { --fl-raised: inset 1px 1px #fff, inset -1px -1px #404040, inset 2px 2px #dfdfdf, inset -2px -2px #808080; --fl-sunken: inset 1px 1px #808080, inset -1px -1px #fff, inset 2px 2px #404040, inset -2px -2px #dfdfdf; }\n.lab { container-type: inline-size; container-name: flightlab; }\n' + controls
    html = original['dist/index.html'].decode()
    if 'assets/playback.css' not in html:
        html = html.replace('</head>', '  <link rel="stylesheet" href="assets/playback.css">\n</head>')
    replacements = {
        'dist/assets/app.js': (ROOT / 'assets/app.js').read_bytes(),
        'dist/assets/scene3d.js': (ROOT / 'assets/scene3d.js').read_bytes(),
        'dist/assets/playback.css': controls.encode(),
        'dist/index.html': html.encode(),
    }
    validation = ROOT / 'playback_context_validation.json'
    if validation.exists():
        replacements['source/playback_context_validation.json'] = validation.read_bytes()
    readme = original['README.md'].decode()
    if NOTE_START in readme:
        a, rest = readme.split(NOTE_START, 1)
        _, b = rest.split(NOTE_END, 1)
        readme = a + b.lstrip('\n')
    note = '''<!-- PLAYBACK_CONTEXT_REPAIR -->
# Playback selection update — 12 November 2026

The route and recorded-force views now preserve the selected flight, response and checkpoint. Missing force data is shown explicitly. A terminal close-up and height/time plot display the three retained final states; numbered checkpoint cards expose unequal time gaps. Overlapping marker clicks offer a timestamp choice. The bank command and recorded bank are labelled separately. Full-route markers have no invented connecting trajectory.

This update changes presentation and selection only. The dataset, safe input exports, compiler and scientific assumptions remain as packaged. The lower-speed experiment is still outside this frozen catalogue snapshot. No flight integration is performed by this viewer.

The application and renderer match the published Atlas edition; supplemental CSS supports the same new controls in this standalone layout.
<!-- END_PLAYBACK_CONTEXT_REPAIR -->

'''
    replacements['README.md'] = (note + readme).encode()
    temporary = ARCHIVE.with_suffix('.tmp.zip')
    with ZipFile(temporary, 'w', compression=ZIP_DEFLATED, compresslevel=9) as out:
        for entry, data in entries:
            out.writestr(entry, replacements.pop(entry.filename, data))
        for name, data in replacements.items():
            out.writestr(name, data)
    with ZipFile(temporary) as updated:
        assert updated.testzip() is None
        for name, data in original.items():
            if name.startswith('source/safe_exports/') or name in ('dist/assets/data.js', 'source/compile_data.py', 'source/source_manifest.json', 'source/validation_report.json'):
                assert updated.read(name) == data, name
        assert updated.read('dist/assets/app.js') == (ROOT / 'assets/app.js').read_bytes()
        assert updated.read('dist/assets/scene3d.js') == (ROOT / 'assets/scene3d.js').read_bytes()
    os.replace(temporary, ARCHIVE)
    print('Offline bundle updated; dataset, safe exports and scientific provenance preserved.')


if __name__ == '__main__':
    build()
