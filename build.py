#!/usr/bin/env python3
"""problems.json + python/php/go/ + topics/*.md  ->  site/ (statik HTML)."""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "site"
LANGS = [("python", "Python", "py"), ("php", "PHP", "php"), ("go", "Go", "go")]
E = html.escape
SCALE = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"]
ALIAS = {"O(N)": 2, "O(S)": 2, "O(N^2)": 4, "O(N*N)": 4, "O(2^N)": 5, "O(N LOG N)": 3, "O(LOG N)": 1}


def level(v):
    v = v.strip()
    if v in SCALE:
        return SCALE.index(v)
    if v.upper() in ALIAS:
        return ALIAS[v.upper()]
    up = v.upper()
    if "²" in up or "^2" in up or "2^" in up:
        return 4
    if "LOG" in up:
        return 3
    if "N" in up or "S" in up or "M" in up:
        return 2
    if "1" in up:
        return 0
    return 2


def meter(label, value):
    lv = level(value)
    if lv < 0:
        print("OGOHLANTIRISH: noma'lum murakkablik %r" % value)
    tone = "lo" if lv <= 1 else "mid" if lv <= 3 else "hi"
    return '<div class="meter %s"><div class="meter-top"><span>%s</span><b>%s</b></div></div>' % (tone, label, E(value))


ASSETS = ROOT / "assets"


def inline(s):
    s = E(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


TAB_LANGS = {"python": "Python", "php": "PHP", "go": "Go"}


def code_tabs(group):
    tabs = "".join(
        '<button type="button" role="tab" data-lang="%s" aria-selected="false">%s</button>' % (l, TAB_LANGS[l]) for l, _ in group
    )
    panels = "".join(
        '<div class="panel" data-lang="%s" hidden><pre><code>%s</code></pre></div>' % (l, E(src)) for l, src in group
    )
    return ('<section class="editor ctabs" data-tabs><div class="ed-bar" role="tablist">%s'
            '<button type="button" class="copy">%s<span>Nusxalash</span></button></div>%s</section>' % (tabs, ICONS["copy"], panels))


def md(text):
    out, para, items, group, code, lang = [], [], [], [], None, ""

    def flush_text():
        nonlocal para, items
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            para = []
        if items:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(i) for i in items))
            items = []

    def flush_group():
        nonlocal group
        if group:
            out.append(code_tabs(group))
            group = []

    def flush():
        flush_text()
        flush_group()

    def cells(row):
        return [c.strip() for c in row.strip().strip("|").split("|")]

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if code is not None:
            if line.startswith("```"):
                src = "\n".join(code)
                if lang in TAB_LANGS:
                    group.append((lang, src))
                else:
                    flush_group()
                    out.append("<pre><code>%s</code></pre>" % E(src))
                code = None
            else:
                code.append(line)
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            if lang in TAB_LANGS:
                flush_text()
            else:
                flush()
            code = []
        elif line.lstrip().startswith("|") and i < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i]):
            flush()
            head = cells(line)
            i += 1
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            out.append("<div class=\"tbl\"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (
                "".join("<th>%s</th>" % inline(c) for c in head),
                "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows)))
        elif m := re.match(r"(#{1,4})\s+(.*)", line):
            flush()
            n = max(len(m.group(1)), 2)
            out.append("<h%d>%s</h%d>" % (n, inline(m.group(2)), n))
        elif line.startswith("> "):
            flush()
            out.append('<blockquote>%s</blockquote>' % inline(line[2:]))
        elif m := re.match(r"[-*]\s+(.*)", line):
            flush_group()
            if para:
                flush_text()
            items.append(m.group(1))
        elif not line.strip():
            flush_text()
        else:
            flush_group()
            if items:
                flush_text()
            para.append(line.strip())
    flush()
    return "\n".join(out)


def add_toc(html_):
    toc = []

    def sub(m):
        n = len(toc) + 1
        toc.append((n, re.sub(r"<[^>]+>", "", m.group(1))))
        return '<h2 id="s%d">%s</h2>' % (n, m.group(1))

    return re.sub(r"<h2>(.*?)</h2>", sub, html_), toc


def front_matter(text):
    meta = {}
    if text.startswith("---"):
        _, fm, text = text.split("---", 2)
        for line in fm.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, text.strip()


ICONS = {
    "list": '<svg viewBox="0 0 24 24"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></svg>',
    "book": '<svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/></svg>',
    "hash": '<svg viewBox="0 0 24 24"><path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/></svg>',
    "search": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>',
    "theme": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 3v18" /><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>',
    "copy": '<svg viewBox="0 0 24 24"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>',
    "out": '<svg viewBox="0 0 24 24"><path d="M7 17 17 7M8 7h9v9"/></svg>',
}
SIDE_TOPICS = []  # (slug, title, count) — main() to'ldiradi


def page(title, body, base, active="", wide=False):
    def cur(n):
        return ' aria-current="page"' if n == active else ""

    return f"""<!doctype html>
<html lang="uz"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} — LeetNote</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{base}style.css"></head>
<body>
<div class="shell">
<aside class="side">
<a class="brand" href="{base}index.html"><span class="logo">&gt;_</span>leetnote</a>
<nav class="nav" aria-label="Asosiy"><span class="nav-label">Bo'limlar</span>
<a href="{base}index.html"{cur("problems")}>{ICONS["list"]}Masalalar</a>
<a href="{base}topics.html"{cur("topics")}>{ICONS["book"]}Topiclar</a></nav>
<div class="side-foot"><span>Python · PHP · Go</span>
<button id="theme" class="icon-btn" type="button" aria-label="Mavzuni almashtirish">{ICONS["theme"]}</button></div>
</aside>
<main class="content"><div class="inner{" narrow" if not wide else ""}">
{body}
</div></main>
</div>
<script src="{base}app.js"></script>
</body></html>"""


def chips(slugs, topics, base, link=True):
    tag = "a" if link else "span"
    return "".join(
        '<%s class="chip"%s>%s</%s>'
        % (tag, ' href="%stopics/%s.html"' % (base, s) if link else "", E(topics.get(s, {}).get("title", s)), tag)
        for s in slugs
    )


def badge(d):
    return '<span class="badge %s">%s</span>' % (d, d)


def main():
    problems = sorted(json.loads((ROOT / "problems.json").read_text("utf-8")), key=lambda p: p["id"])
    topics = {}
    for f in sorted((ROOT / "topics").glob("*.md")):
        meta, text = front_matter(f.read_text("utf-8"))
        topics[f.stem] = {"title": meta.get("title", f.stem), "summary": meta.get("summary", ""), "html": md(text)}

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "problems").mkdir(parents=True)
    (OUT / "topics").mkdir()
    shutil.copy(ASSETS / "style.css", OUT / "style.css")
    shutil.copy(ASSETS / "app.js", OUT / "app.js")

    used = {}
    for p in problems:
        for t in p["topics"]:
            used.setdefault(t, []).append(p)
            if t not in topics:
                print("OGOHLANTIRISH: topics/%s.md yo'q (masala %d)" % (t, p["id"]))
    SIDE_TOPICS[:] = [(k, v["title"], len(used.get(k, []))) for k, v in sorted(topics.items(), key=lambda kv: kv[1]["title"])]
    count = lambda d: sum(1 for p in problems if p["difficulty"] == d)
    total = max(len(problems), 1)

    def has(p, d, ext):
        return (ROOT / d / ("%04d-%s.%s" % (p["id"], p["slug"], ext))).exists()

    # index
    rows = ""
    for p in problems:
        langs = "".join('<span class="lg%s">%s</span>' % (" on" if has(p, d, ext) else "", ext.upper()) for d, _, ext in LANGS)
        rows += (
            '<a class="row" href="problems/%04d-%s.html" data-s="%s" data-d="%s" data-t="%s">'
            '<span class="n">%04d</span><span class="main"><span class="t">%s</span><span class="tags">%s</span></span>'
            '<span class="langs">%s</span><span class="diff">%s</span></a>'
            % (p["id"], p["slug"], E((p["title"] + " " + str(p["id"])).lower()), p["difficulty"], " ".join(p["topics"]),
               p["id"], E(p["title"]), chips(p["topics"], topics, "", link=False), langs, badge(p["difficulty"]))
        )
    tf = "".join('<button type="button" data-t="%s" aria-pressed="false">%s</button>' % (s, E(t)) for s, t, _ in SIDE_TOPICS)
    seg = "".join(
        '<button type="button" data-d="%s" aria-pressed="%s">%s</button>' % (v, "true" if not v else "false", l)
        for v, l in [("", "Barchasi"), ("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")]
    )
    body = f"""<h1>Masalalar</h1>
<p class="sub">Yechimlar va ularning g'oyasi. Topic bo'yicha filtrlang yoki qidiring.</p>
<div class="summary"><span><b id="count">{len(problems)}</b> / {len(problems)} masala</span>
<span class="dist" aria-hidden="true"><i class="e" style="width:{count("Easy") * 100 / total}%"></i><i class="m" style="width:{count("Medium") * 100 / total}%"></i><i class="h" style="width:{count("Hard") * 100 / total}%"></i></span>
<span>{count("Easy")} easy · {count("Medium")} medium · {count("Hard")} hard</span></div>
<div class="bar"><label class="search">{ICONS["search"]}<input id="q" type="search" placeholder="Nom yoki raqam" aria-label="Qidirish"></label>
<div class="seg" role="group" aria-label="Daraja">{seg}</div></div>
<div class="tf" role="group" aria-label="Topic">{tf}</div>
<div class="list">{rows}<div id="none" class="none" hidden>Hech narsa topilmadi.</div></div>"""
    (OUT / "index.html").write_text(page("Masalalar", body, "", "problems"), "utf-8")

    # topics index
    cards = "".join(
        '<a class="card" href="topics/%s.html" data-s="%s"><span class="k">Topic</span><strong>%s</strong><p>%s</p><span class="count">%d ta masala</span></a>'
        % (k, E((v["title"] + " " + v["summary"]).lower()), E(v["title"]), E(v["summary"]), len(used.get(k, [])))
        for k, v in sorted(topics.items(), key=lambda kv: kv[1]["title"])
    )
    body = f"""<h1>Topiclar</h1><p class="sub">Masalalarda ishlatiladigan g'oyalar va shablonlar.</p>
<div class="bar"><label class="search">{ICONS["search"]}<input id="tq" type="search" placeholder="Topic qidirish" aria-label="Topic qidirish"></label></div>
<div class="grid">{cards}</div><div id="tnone" class="none" hidden>Hech narsa topilmadi.</div>"""
    (OUT / "topics.html").write_text(page("Topiclar", body, "", "topics"), "utf-8")

    # topic pages
    for k, v in topics.items():
        content, toc = add_toc(v["html"])
        nav = "".join('<a href="#s%d">%s</a>' % (n, t) for n, t in toc)
        lst = "".join(
            '<a class="row" href="../problems/%04d-%s.html"><span class="n">%04d</span><span class="t">%s</span><span></span>%s</a>'
            % (p["id"], p["slug"], p["id"], E(p["title"]), badge(p["difficulty"]))
            for p in used.get(k, [])
        )
        related = ('<h2>Shu topicdagi masalalar</h2><div class="list">%s</div>' % lst) if lst else ""
        body = (f'<div class="crumbs"><a href="../topics.html">Topiclar</a><i>/</i><span>{E(v["title"])}</span></div>'
                f'<div class="doc"><article class="article"><span class="eyebrow">Topic</span><h1>{E(v["title"])}</h1>'
                f'<p class="sub">{E(v["summary"])}</p><div class="prose">{content}</div>{related}</article>'
                f'<aside class="toc"><span class="label">Mundarija</span>{nav}</aside></div>')
        (OUT / "topics" / (k + ".html")).write_text(page(v["title"], body, "../", "topics", wide=True), "utf-8")

    # problem pages
    for i, p in enumerate(problems):
        stem = "%04d-%s" % (p["id"], p["slug"])
        methods = p.get("methods")

        link = ('<a class="ext" href="%s" target="_blank" rel="noopener">LeetCode%s</a>' % (E(p["url"]), ICONS["out"])) if p.get("url") else ""
        prev = problems[i - 1] if i > 0 else None
        nxt = problems[i + 1] if i + 1 < len(problems) else None
        pager = ""
        if prev:
            pager += '<a class="prev" href="%04d-%s.html"><small>← Oldingi</small>%s</a>' % (prev["id"], prev["slug"], E(prev["title"]))
        if nxt:
            pager += '<a class="next" href="%04d-%s.html"><small>Keyingi →</small>%s</a>' % (nxt["id"], nxt["slug"], E(nxt["title"]))

        if methods:
            # 1. Methods selector box in brief
            m_items = []
            for m_idx, m_obj in enumerate(methods):
                active_attr = ' aria-selected="true"' if m_idx == 0 else ' aria-selected="false"'
                tag_badge = ('<span class="badge Easy" style="font-size:.65rem;padding:1px 6px;margin-left:6px">%s</span>' % E(m_obj["tag"])) if m_obj.get("tag") else ""
                m_items.append(
                    '<button type="button" class="m-item" role="tab" data-m="%d"%s>'
                    '<span class="m-num">%d</span>'
                    '<span class="m-info"><span class="m-title">%s%s</span>'
                    '<span class="m-meta">Vaqt: %s · Xotira: %s</span></span>'
                    '</button>' % (m_idx, active_attr, m_idx + 1, E(m_obj["name"]), tag_badge, E(m_obj.get("time", "")), E(m_obj.get("space", "")))
                )
            methods_card = (
                '<div class="panel-card methods-box"><span class="label">Usullar (ustiga boring yoki bosing)</span>'
                '<div class="methods-list" role="tablist" aria-label="Yechim usullari">%s</div></div>' % "".join(m_items)
            )

            # 2. Views (Meters + Idea for each method)
            m_views = []
            for m_idx, m_obj in enumerate(methods):
                hidden_attr = "" if m_idx == 0 else " hidden"
                m_cx = ""
                if m_obj.get("time") or m_obj.get("space"):
                    m_cx = '<div class="meters">%s%s</div>' % (
                        meter("Vaqt", m_obj["time"]) if m_obj.get("time") else "",
                        meter("Xotira", m_obj["space"]) if m_obj.get("space") else "",
                    )
                m_idea = ('<div class="panel-card idea"><span class="label">G\'oya: %s</span><div class="prose"><p>%s</p></div></div>' % (E(m_obj["name"]), inline(m_obj["desc"]))) if m_obj.get("desc") else ""
                m_views.append('<div class="m-view" data-m="%d"%s>%s%s</div>' % (m_idx, hidden_attr, m_cx, m_idea))
            views_html = "".join(m_views)

            # 3. Note box if problem has general notes (e.g. S definition)
            note_box = ('<div class="panel-card note-box"><span class="label">Izoh: S nima va nega O(S)?</span><div class="prose">%s</div></div>' % md(p["notes"])) if p.get("notes") else ""

            # 4. Language tabs
            lang_tabs = "".join('<button type="button" role="tab" data-lang="%s" aria-selected="%s">%s.%s</button>' % (d, "true" if d == "python" else "false", "solution", ext) for d, _, ext in LANGS)

            # 5. Panels for each method and language
            panels = ""
            for m_idx, m_obj in enumerate(methods):
                code_map = m_obj.get("code", {})
                for d, label, ext in LANGS:
                    src = code_map.get(d)
                    if not src:
                        f = ROOT / d / (stem + "." + ext)
                        if f.exists():
                            src = f.read_text("utf-8").strip()
                    if src:
                        src = src.strip()
                        is_initial = (m_idx == 0 and d == "python")
                        hidden_str = "" if is_initial else " hidden"
                        panels += (
                            '<div class="panel" data-method="%d" data-lang="%s"%s><pre><code>%s</code></pre>'
                            '<div class="status"><span>%s · %s</span><span>%d qator · UTF-8</span></div></div>'
                            % (m_idx, d, hidden_str, E(src), E(label), E(m_obj["name"]), src.count("\n") + 1)
                        )

            editor = (
                '<section class="editor" data-tabs aria-label="Yechim">'
                '<div class="ed-bar" role="tablist">%s<button type="button" class="copy">%s<span>Nusxalash</span></button></div>'
                '%s</section>' % (lang_tabs, ICONS["copy"], panels)
            )

            body = (f'<div class="crumbs"><a href="../index.html">Masalalar</a><i>/</i><span>{p["id"]:04d}</span></div>'
                    f'<div class="split"><div class="brief"><div><h1>{E(p["title"])}</h1>'
                    f'<div class="meta">{badge(p["difficulty"])}{link}</div></div>'
                    f'<div class="panel-card topics-box"><span class="label">Topics</span>{chips(p["topics"], topics, "../")}</div>'
                    f'{methods_card}{views_html}{note_box}{"<div class=pager>" + pager + "</div>" if pager else ""}</div>{editor}</div>')

        else:
            tabs, panels = "", ""
            for d, label, ext in LANGS:
                f = ROOT / d / (stem + "." + ext)
                if f.exists():
                    src = f.read_text("utf-8").rstrip()
                    tabs += '<button type="button" role="tab" data-lang="%s" aria-selected="false">%s.%s</button>' % (d, "solution", ext)
                    panels += ('<div class="panel" data-lang="%s" hidden><pre><code>%s</code></pre>'
                               '<div class="status"><span>%s</span><span>%d qator · UTF-8</span></div></div>'
                               % (d, E(src), E(label), src.count("\n") + 1))
            editor = (
                '<section class="editor" data-tabs aria-label="Yechim"><div class="ed-bar" role="tablist">%s'
                '<button type="button" class="copy">%s<span>Nusxalash</span></button></div>%s</section>' % (tabs, ICONS["copy"], panels)
                if tabs else '<section class="editor"><p class="empty" style="padding:20px">Hali kod yo\'q.</p></section>'
            )
            cx = ""
            if p.get("time") or p.get("space"):
                cx = '<div class="meters">%s%s</div>' % (
                    meter("Vaqt", p["time"]) if p.get("time") else "",
                    meter("Xotira", p["space"]) if p.get("space") else "",
                )
            idea = ('<div class="panel-card idea"><span class="label">G\'oya</span><div class="prose">%s</div></div>' % md(p["notes"])) if p.get("notes") else ""
            body = (f'<div class="crumbs"><a href="../index.html">Masalalar</a><i>/</i><span>{p["id"]:04d}</span></div>'
                    f'<div class="split"><div class="brief"><div><h1>{E(p["title"])}</h1>'
                    f'<div class="meta">{badge(p["difficulty"])}{link}</div></div>'
                    f'<div class="panel-card topics-box"><span class="label">Topics</span>{chips(p["topics"], topics, "../")}</div>'
                    f'{cx}{idea}{"<div class=pager>" + pager + "</div>" if pager else ""}</div>{editor}</div>')

        (OUT / "problems" / (stem + ".html")).write_text(page(p["title"], body, "../", "problems", wide=True), "utf-8")

    print("Tayyor: %s (%d masala, %d topic)" % (OUT / "index.html", len(problems), len(topics)))


main()
