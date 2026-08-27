#!/usr/bin/env python3
"""
Static site builder for adriano-229.
Reads Markdown files from /posts, builds a styled HTML site into /docs.

Each post is a .md file with frontmatter like:

---
title: Why I stopped using inheritance
date: 2026-07-12
video_url: https://youtube.com/watch?v=xxxx   # optional
excerpt: A short one-liner shown on the index page.
---

Body in markdown goes here.
"""

import html
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Installing 'markdown' package...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "markdown"], check=True)
    import markdown

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
OUT_DIR = ROOT / "docs"
SITE_NAME = "adriano-229"
SITE_TAGLINE = "notes on topics"


def _unquote(val: str) -> str:
    """Strip one layer of matching outer quotes only (not stray internal quotes)."""
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
        return val[1:-1]
    return val


def parse_frontmatter(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("Missing frontmatter block (---...---) at top of file")
    raw_fm, body = m.group(1), m.group(2)
    meta = {}
    for line in raw_fm.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        meta[key] = _unquote(val)
    return meta, body


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def load_posts():
    posts = []
    if not POSTS_DIR.exists():
        return posts
    for f in sorted(POSTS_DIR.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        required = ["title", "date"]
        missing = [r for r in required if r not in meta]
        if missing:
            print(f"WARNING: {f.name} missing fields {missing}, skipping")
            continue
        meta["slug"] = meta.get("slug") or slugify(meta["title"])
        meta["html"] = markdown.markdown(
            body, extensions=["fenced_code", "codehilite", "tables"]
        )
        try:
            meta["_date_obj"] = datetime.strptime(meta["date"], "%Y-%m-%d")
        except ValueError:
            meta["_date_obj"] = datetime.min
        posts.append(meta)
    posts.sort(key=lambda p: p["_date_obj"], reverse=True)
    return posts


def fmt_date(date_str: str) -> str:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%b %-d, %Y")
    except ValueError:
        return date_str


BASE_CSS = """
:root {
  --paper: #FAFAFA;
  --paper-raised: #FFFFFF;
  --ink: #212223;
  --ink-soft: #5B5D61;
  --ink-faint: #8B8D92;
  --rust: #6C6FE0;
  --rust-soft: #EFEFFC;
  --rule: #E4E4E7;
  --rule-soft: #EEEEF0;
  --code-bg: #F1F1F3;
  --max-w: 680px;
  --serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
  --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
}

* { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; }

body {
  margin: 0;
  background: var(--paper);
  background-image: radial-gradient(circle at 12% 8%, rgba(108, 111, 224, 0.05), transparent 45%);
  background-attachment: fixed;
  color: var(--ink);
  font-family: var(--sans);
  font-size: 17px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a { color: var(--rust); text-decoration: none; transition: color 0.15s var(--ease); }
a:hover { text-decoration: underline; }
a:focus-visible, button:focus-visible { outline: 2px solid var(--rust); outline-offset: 3px; border-radius: 2px; }

.wrap {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 24px;
}

/* Header */
header.site-header {
  padding: 72px 0 36px;
  border-bottom: 1px solid var(--rule);
}

header.site-header .handle {
  display: flex;
  align-items: baseline;
  gap: 10px;
  font-family: var(--serif);
  font-size: 2.2rem;
  font-weight: 600;
  letter-spacing: -0.015em;
  margin: 0 0 10px;
}

header.site-header .handle a { color: var(--ink); transition: color 0.15s var(--ease); }
header.site-header .handle a:hover { color: var(--rust); text-decoration: none; }

header.site-header .dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--rust);
  box-shadow: 0 0 0 4px var(--rust-soft);
}

header.site-header .tagline {
  color: var(--ink-soft);
  font-family: var(--mono);
  font-size: 0.86rem;
  margin: 0;
}

header.site-header .tagline .prompt { color: var(--ink-faint); }

/* Post list */
main { padding: 8px 0 100px; }

.post-item {
  display: block;
  padding: 30px 20px;
  margin: 0 -20px;
  border-bottom: 1px solid var(--rule-soft);
  border-radius: 12px;
  color: var(--ink);
  transition: background-color 0.18s var(--ease), transform 0.18s var(--ease);
}

.post-item:hover {
  text-decoration: none;
  background: var(--paper-raised);
  transform: translateX(2px);
}

.post-item:hover .post-title { color: var(--rust); }
.post-item:last-child { border-bottom: none; }

.post-meta-row {
  margin-bottom: 12px;
  font-family: var(--mono);
  font-size: 0.76rem;
  color: var(--ink-faint);
}

.post-title {
  font-family: var(--serif);
  font-size: 1.48rem;
  font-weight: 600;
  margin: 0 0 9px;
  line-height: 1.32;
  letter-spacing: -0.008em;
  transition: color 0.15s var(--ease);
}

.post-excerpt {
  color: var(--ink-soft);
  font-size: 0.97rem;
  margin: 0;
  max-width: 56ch;
}

/* Single post */
article.post {
  padding: 16px 0 60px;
}

article.post .post-meta-row { margin-bottom: 20px; }

article.post h1 {
  font-family: var(--serif);
  font-size: 2.15rem;
  font-weight: 600;
  line-height: 1.22;
  letter-spacing: -0.015em;
  margin: 0 0 22px;
}

article.post .content {
  font-size: 1.06rem;
}

article.post .content h2 {
  font-family: var(--serif);
  font-size: 1.42rem;
  font-weight: 600;
  margin: 2em 0 0.6em;
  letter-spacing: -0.01em;
}

article.post .content h3 {
  font-family: var(--serif);
  font-size: 1.16rem;
  font-weight: 600;
  margin: 1.8em 0 0.5em;
}

article.post .content p { margin: 0 0 1.25em; }

article.post .content a {
  text-decoration: underline;
  text-decoration-color: var(--rule);
  text-underline-offset: 3px;
  transition: text-decoration-color 0.15s var(--ease);
}
article.post .content a:hover { text-decoration-color: var(--rust); }

article.post .content code {
  font-family: var(--mono);
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.87em;
}

article.post .content pre {
  background: var(--code-bg);
  padding: 20px 22px;
  border-radius: 10px;
  overflow-x: auto;
  margin: 0 0 1.5em;
  border: 1px solid var(--rule-soft);
}

article.post .content pre code {
  background: none;
  padding: 0;
  font-size: 0.87rem;
  line-height: 1.6;
}

article.post .content blockquote {
  margin: 0 0 1.5em;
  padding: 4px 0 4px 20px;
  border-left: 3px solid var(--rust);
  color: var(--ink-soft);
  font-style: italic;
}

article.post .content ul, article.post .content ol {
  margin: 0 0 1.25em;
  padding-left: 1.4em;
}

article.post .content li { margin-bottom: 0.45em; }

article.post .content table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 1.5em;
  font-size: 0.95rem;
}

article.post .content th,
article.post .content td {
  padding: 10px 14px;
  border: 1px solid var(--rule);
  text-align: left;
}

article.post .content th {
  background: var(--rule-soft);
  font-weight: 600;
  font-family: var(--mono);
  font-size: 0.82rem;
  letter-spacing: 0.01em;
}

article.post .content tr:nth-child(even) td {
  background: var(--paper-raised);
}

article.post .content img {
  max-width: 100%;
  border-radius: 10px;
  margin: 1.2em 0;
  border: 1px solid var(--rule-soft);
}

.video-embed {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  margin: 0 0 1.8em;
  border-radius: 10px;
  overflow: hidden;
  background: var(--code-bg);
  border: 1px solid var(--rule-soft);
}

.video-embed iframe {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  border: 0;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 32px;
  font-family: var(--mono);
  font-size: 0.84rem;
  color: var(--ink-faint);
  transition: color 0.15s var(--ease), transform 0.15s var(--ease);
}

.back-link:hover { color: var(--rust); transform: translateX(-2px); }

/* Footer */
footer.site-footer {
  padding: 36px 0 60px;
  border-top: 1px solid var(--rule);
  font-family: var(--mono);
  font-size: 0.78rem;
  color: var(--ink-faint);
}

footer.site-footer a { color: var(--ink-faint); }
footer.site-footer a:hover { color: var(--rust); }

.empty-state {
  padding: 48px 0;
  color: var(--ink-soft);
  font-family: var(--mono);
  font-size: 0.9rem;
  text-align: center;
  border: 1px dashed var(--rule);
  border-radius: 12px;
}

::selection { background: var(--rust-soft); color: var(--ink); }

@media (max-width: 600px) {
  header.site-header { padding: 44px 0 28px; }
  header.site-header .handle { font-size: 1.75rem; }
  .post-item { margin: 0 -16px; padding: 26px 16px; }
  article.post h1 { font-size: 1.65rem; }
  .post-title { font-size: 1.28rem; }
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
"""

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>&#128220;</text></svg>">
</head>
<body>
"""

HEADER_TEMPLATE = """
<div class="wrap">
  <header class="site-header">
    <p class="handle"><a href="{root}index.html">adriano-229</a><span class="dot" aria-hidden="true"></span></p>
    <p class="tagline"><span class="prompt">$</span> notes on topics</p>
  </header>
"""

FOOTER_TEMPLATE = """
  <footer class="site-footer">
    <p>&copy; {year} adriano-229 &mdash; built with claude</p>
  </footer>
</div>
</body>
</html>
"""


def render_index(posts):
    items_html = []

    if not posts:
        items_html.append(
            '<div class="empty-state">no posts yet &mdash; drop a .md file in /posts and rebuild</div>'
        )

    for p in posts:
        items_html.append(f"""
    <a class="post-item" href="posts/{p['slug']}.html">
      <div class="post-meta-row">
        <span>{fmt_date(p['date'])}</span>
      </div>
      <h2 class="post-title">{html.escape(p['title'])}</h2>
      <p class="post-excerpt">{html.escape(p.get('excerpt', ''))}</p>
    </a>""")

    html_out = HEAD_TEMPLATE.format(
        title="adriano-229 — notes on topics",
        description=html.escape(SITE_TAGLINE),
        root="",
    )
    html_out += HEADER_TEMPLATE.format(root="")
    html_out += f'<main>{"".join(items_html)}</main>'
    html_out += FOOTER_TEMPLATE.format(year=datetime.now().year)
    return html_out


def render_post(post):
    video_html = ""
    if post.get("video_url"):
        m = re.search(r"(?:v=|youtu\.be/|embed/)([\w-]+)", post["video_url"])
        if m:
            video_html = f"""
      <div class="video-embed">
        <iframe src="https://www.youtube.com/embed/{m.group(1)}" title="{html.escape(post['title'])}" allowfullscreen loading="lazy"></iframe>
      </div>"""

    html_out = HEAD_TEMPLATE.format(
        title=html.escape(f"{post['title']} — adriano-229"),
        description=html.escape(post.get("excerpt", SITE_TAGLINE)),
        root="../",
    )
    html_out += HEADER_TEMPLATE.format(root="../")
    html_out += f"""
  <main>
    <article class="post">
      <a class="back-link" href="../index.html">&larr; all posts</a>

      <div class="post-meta-row">
        <span>{fmt_date(post['date'])}</span>
      </div>

      <h1>{html.escape(post['title'])}</h1>
      {video_html}
      <div class="content">
        {post['html']}
      </div>
    </article>
  </main>"""

    html_out += FOOTER_TEMPLATE.format(year=datetime.now().year)
    return html_out


def build():
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "posts").mkdir(exist_ok=True)

    (OUT_DIR / "style.css").write_text(BASE_CSS, encoding="utf-8")

    posts = load_posts()

    (OUT_DIR / "index.html").write_text(render_index(posts), encoding="utf-8")

    for p in posts:
        out_path = OUT_DIR / "posts" / f"{p['slug']}.html"
        out_path.write_text(render_post(p), encoding="utf-8")

    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Built {len(posts)} post(s) into {OUT_DIR}")


if __name__ == "__main__":
    build()
