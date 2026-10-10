"""Static site generator for CalcHub.
Run:  python build.py
Edit DOMAIN/SITE below, add calculators in specs_*.py, rebuild.
"""
import html, json, os, glob
from specs_finance import SPECS as F
from specs_health_math import SPECS as HM
from specs_other import SPECS as O
from specs_f2 import SPECS as F2
from specs_h2 import SPECS as H2
from specs_m2 import SPECS as M2
from specs_c2 import SPECS as C2
from specs_k2 import SPECS as K2

DOMAIN = "https://YOURDOMAIN.com"
SITE = "CalcHub"
OUT = os.path.dirname(os.path.abspath(__file__))

CATS = [
    ("finance", "Finance", "Mortgage, loan, savings, investing and everyday money calculators."),
    ("health", "Health", "BMI, calories, body fat, heart rate and fitness calculators."),
    ("math", "Math", "Percentages, statistics, algebra and geometry calculators."),
    ("conversion", "Unit Converters", "Convert length, weight, temperature, volume, speed and more."),
    ("everyday", "Everyday", "Dates, ages, GPA, fuel cost, electricity and shopping calculators."),
    ("construction", "Construction", "Paint, concrete, flooring, tile, gravel and lumber estimators."),
    ("science", "Science", "Physics and science calculators: Ohm's law, energy, density and more."),
]
CAT = {c[0]: c for c in CATS}
SPECS = F + HM + O + F2 + H2 + M2 + C2 + K2
e = html.escape


def nav():
    return "".join(f'<a href="{s}.html">{n}</a>' for s, n, _ in CATS)


def head(title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{DOMAIN}/{path}">
<link rel="stylesheet" href="style.css">
{extra}<!-- ADSENSE: after approval, uncomment and add your publisher id
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>-->
</head><body>
<header><div class="wrap"><a class="logo" href="index.html">{SITE}</a><nav>{nav()}</nav></div></header>
<main class="wrap">
"""


def foot():
    return f"""</main>
<footer><div class="wrap">&copy; {SITE} · <a href="privacy.html">Privacy</a> · Results are estimates for information only, not financial, medical or professional advice.</div></footer>
"""


def field(i):
    id_, label, default = i[0], i[1], i[2]
    extra = i[3] if len(i) > 3 else None
    if isinstance(extra, list):
        opts = "".join(
            f'<option value="{e(str(v))}"{" selected" if str(v) == str(default) else ""}>{e(l)}</option>' for v, l in extra)
        ctl = f'<select id="{id_}">{opts}</select>'
    elif extra in ("date", "time"):
        today = ' data-today="1"' if default == "today" else ""
        val = "" if default == "today" else default
        ctl = f'<input id="{id_}" type="{extra}" value="{val}"{today}>'
    elif extra == "textarea":
        ctl = f'<textarea id="{id_}" rows="5">{e(str(default))}</textarea>'
    elif extra == "text":
        ctl = f'<input id="{id_}" type="text" value="{e(str(default))}">'
    else:
        ctl = f'<input id="{id_}" type="number" step="any" value="{default}">'
    return f'<label for="{id_}">{e(label)}</label>{ctl}'


def calc_page(s):
    cat = CAT[s["cat"]]
    related = [x for x in SPECS if x["cat"] == s["cat"] and x["slug"] != s["slug"]]
    idx = [x["slug"] for x in SPECS if x["cat"] == s["cat"]].index(s["slug"])
    related = (related[idx:] + related[:idx])[:6]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]}
    ld = f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>\n'
    ids = ",".join(i[0] for i in s["inputs"])
    p = head(f'{s["title"]} | {SITE}', s["desc"], s["slug"] + ".html", ld)
    p += f'<p class="muted"><a href="index.html">Home</a> › <a href="{cat[0]}.html">{cat[1]}</a></p>\n'
    p += f'<h1>{e(s["title"])}</h1>\n<p class="muted">{e(s["desc"])}</p>\n'
    p += '<form class="card" data-calc="1">\n' + "\n".join(field(i) for i in s["inputs"])
    p += '\n<button type="submit">Calculate</button>\n<div class="result" id="out" aria-live="polite"></div>\n</form>\n'
    p += '<div class="ad"><!-- ad slot --></div>\n'
    p += f'<h2>How it works</h2>\n<p>{e(s["about"])}</p>\n'
    p += "<h2>Frequently asked questions</h2>\n" + "".join(
        f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>\n" for q, a in s["faqs"])
    p += "<h2>Related calculators</h2>\n<div class=\"grid\">" + "".join(
        f'<a href="{r["slug"]}.html"><b>{e(r["title"])}</b></a>' for r in related) + "</div>\n"
    p += foot()
    p += f'<script src="calc.js"></script>\n<script>CalcPage(function({{{ids}}}){{\n{s["body"]}\n}});</script>\n</body></html>\n'
    return p


def card(s):
    return f'<a href="{s["slug"]}.html" data-t="{e((s["title"] + " " + s["desc"]).lower())}"><b>{e(s["title"])}</b>{e(s["desc"])}</a>'


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def main():
    seen = set()
    for s in SPECS:
        assert s["slug"] not in seen, "duplicate slug " + s["slug"]
        seen.add(s["slug"])
    for old in glob.glob(os.path.join(OUT, "*.html")):
        if os.path.basename(old) != "privacy.html":
            os.remove(old)
    for s in SPECS:
        write(s["slug"] + ".html", calc_page(s))
    # category pages
    for slug, name, blurb in CATS:
        items = [s for s in SPECS if s["cat"] == slug]
        p = head(f"{name} Calculators – Free Online | {SITE}", blurb, slug + ".html")
        p += f'<p class="muted"><a href="index.html">Home</a></p>\n<h1>{name} Calculators</h1>\n<p class="muted">{blurb}</p>\n'
        p += '<div class="grid">' + "".join(card(s) for s in items) + "</div>\n<div class=\"ad\"></div>\n" + foot() + "</body></html>\n"
        write(slug + ".html", p)
    # home
    p = head(f"{SITE} – Free Online Calculators for Money, Health, Math & More",
             f"{len(SPECS)} free online calculators: mortgage, loan, BMI, percentage, unit converters, dates and more. Instant results, no sign-up.",
             "")
    p += f'<h1>Free Online Calculators</h1>\n<p class="muted">{len(SPECS)} calculators. Instant results, no sign-up, nothing stored.</p>\n'
    p += '<input class="search" id="q" type="search" placeholder="Search calculators (e.g. mortgage, BMI, percentage)…" aria-label="Search calculators">\n'
    for slug, name, blurb in CATS:
        items = [s for s in SPECS if s["cat"] == slug]
        p += f'<section class="cat"><h2><a href="{slug}.html">{name}</a></h2><div class="grid">' + "".join(card(s) for s in items[:12]) + "</div>" + (f'<p><a href="{slug}.html">View all {len(items)} {name.lower()} calculators →</a></p>' if len(items) > 12 else "") + "</section>\n"
    p += '<div class="ad"></div>\n' + foot()
    p += """<script>
const q=document.getElementById('q');
q.addEventListener('input',()=>{const t=q.value.trim().toLowerCase();
document.querySelectorAll('.grid a').forEach(a=>{a.style.display=!t||a.dataset.t.includes(t)?'':'none';});
document.querySelectorAll('.cat').forEach(c=>{c.style.display=[...c.querySelectorAll('a[data-t]')].some(a=>a.style.display!=='none')?'':'none';});});
</script>
</body></html>
"""
    write("index.html", p)
    # sitemap + robots
    urls = [""] + [c[0] + ".html" for c in CATS] + [s["slug"] + ".html" for s in SPECS] + ["privacy.html"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"<url><loc>{DOMAIN}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    print(f"Built {len(SPECS)} calculators, {len(CATS)} category pages.")


if __name__ == "__main__":
    main()
