"""Build index.html: embed the weekly HHS data into the dashboard template.

Usage:  python scripts/build.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEEP = ["w", "ib", "iu", "ab", "ao", "icb", "ico", "tib", "tiu", "cov", "covicu", "ed", "edc"]

weeks = json.loads((ROOT / "data" / "weeks.json").read_text(encoding="utf-8"))
weeks = [{k: w.get(k) for k in KEEP} for w in weeks]

page = (ROOT / "src" / "dashboard.src.html").read_text(encoding="utf-8")
page = page.replace("/*DATA*/[]", json.dumps(weeks, separators=(",", ":")))

html = (
    "<!doctype html>\n<html lang=\"en\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
    "<style>:root{color-scheme:dark;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
    "body{margin:0;font:14px system-ui,-apple-system,'Segoe UI',sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>\n"
    "</head>\n<body>\n" + page + "\n</body>\n</html>\n"
)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"Wrote index.html ({len(html):,} bytes, {len(weeks)} weeks)")
