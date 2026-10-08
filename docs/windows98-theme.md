# Atlas 98 presentation

Windows 98-inspired presentation for the existing Atlas. This changes the shared `common.css` and `common.js` only; this document records the scope. Scientific content, data, formulas, raw and derived figures, `gen.py`, CNAME, DNS and deployment settings are unchanged.

## Interface

- Teal desktop, gray beveled panels, blue gradient title bar and small original SVG icons.
- Existing section links remain available as tabs; additional desktop and Start-menu shortcuts point to the same pages.
- Working minimize/taskbar restore, maximize/restore, About dialog and print command. No fake destructive Close button.
- Responsive single-column launcher layout on phones, scrollable navigation, locally scrollable wide tables, keyboard focus and Escape/arrow-key support.
- The taskbar clock is explicitly current UTC, not flight/model time.
- The classic light appearance is intentional even on a dark-mode operating system. Original light-theme scientific color tokens are retained. System font fallbacks are used; no new font files, frameworks or runtime network requests are introduced.

## Preservation and build

The new shell is appended after the original 9,842 bytes of `common.js`. No original MH map, range, plotting or data-fetch function is rewritten. It progressively enhances existing DOM nodes after DOMContentLoaded and preserves IDs and event handlers. Table wrappers retain the original tables. The original stylesheet is retained as a prefix, followed by theme overrides.

Existing pages already load both shared files. `gen.py` writes HTML pages but does not overwrite these assets, so regeneration retains the theme without duplicating scientific templates. Standalone embedded documents with their own styles are not separately reskinned.

Baseline: `3227224c705fb69f6db0336da79a3a5d8dc12089`.

Tested final blob identities:
- `common.js`: `dc4e67ed22c1f346788f3cf5cba17d53077b9617`
- `common.css`: `bf49c374aacf1a29488da17508d3181610990c7e`

## Verification performed

76 offline checks passed in Chromium. These cover source blob identity, preservation of the original JS/CSS prefixes, unchanged homepage text/tables/destinations, 390/768/1024/1440-pixel layouts without document overflow, Start open/close and keyboard navigation, minimize/restore, maximize/restore, About dialog, print styling, and no added runtime network requests or JavaScript errors in the tested fixtures.

A synthetic map fixture exercised the unchanged MH.Map renderer, layer toggle, resize and minimize/restore. It is a UI smoke test, not a replay of MH370 scientific results. Screenshots were rendered from the pinned actual homepage with the proposed assets; external fonts were not loaded. Live-domain browsing and a complete real-data end-to-end test of every page were unavailable in this execution environment and are not claimed.

The downloadable review package supplied with the change contains screenshots, the offline preview, the test script, original baseline fixtures and `validation.json`. The PR remains unmerged until publication is authorized.
