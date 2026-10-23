import html
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS_DIR = ROOT / "posts"
OUT_DIR = ROOT / "docs"
SITE_NAME = "adriano-229"
SITE_TAGLINE = "notes on topics"


def load_posts():
    posts = []
    if not POSTS_DIR.exists():
        return posts
    for f in sorted(POSTS_DIR.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        article_match = re.search(r"<article\b([^>]*)>(.*?)</article>", raw, re.DOTALL | re.IGNORECASE)
        if not article_match:
            print(f"WARNING: {f.name} has no article element, skipping")
            continue
        _, article_body = article_match.groups()
        title_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", article_body, re.DOTALL | re.IGNORECASE)
        date_match = re.search(
            r'<div class="post-meta-row">\s*<span>(.*?)</span>',
            article_body,
            re.DOTALL | re.IGNORECASE,
        )
        if not title_match or not date_match:
            print(f"WARNING: {f.name} is missing an h1 or post-meta-row, skipping")
            continue
        title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
        date = date_match.group(1).strip()
        content_match = re.search(
            r'<div class="content">(.*)</div>',
            article_body,
            re.DOTALL | re.IGNORECASE,
        )
        if not content_match:
            print(f"WARNING: {f.name} is missing a content div, skipping")
            continue
        content = content_match.group(1).strip()
        content = re.sub(
            rf'(?<=["\(])\.\./assets/{re.escape(f.stem)}/assets/',
            'assets/',
            content,
        )
        content = re.sub(r'(?<=["\(])\.\./assets/', 'assets/', content)
        content = re.sub(
            r"(<table\b[^>]*>.*?</table>)",
            r'<div class="table-scroll">\1</div>',
            content,
            flags=re.DOTALL | re.IGNORECASE,
        )
        meta = {
            "title": title,
            "date": date,
            "filename": f.stem,
            "html": content,
        }
        try:
            meta["_date_obj"] = datetime.strptime(date, "%b %d, %Y")
        except ValueError:
            meta["_date_obj"] = datetime.min
        posts.append(meta)
    posts.sort(key=lambda p: p["_date_obj"], reverse=True)
    return posts


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
  --max-w: 1000px;
  --body-font: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --body-font-size: 16px;
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
}

* { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; }

body {
  margin: 0;
  background: var(--paper);
  background-attachment: fixed;
  color: var(--ink);
  font-family: var(--body-font);
  font-size: var(--body-font-size);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body::before {
  content: "";
  position: fixed;
  z-index: 0;
  inset: -18%;
  pointer-events: none;
  background:
    radial-gradient(ellipse at 18% 22%, rgba(93, 166, 255, 0.16), transparent 36%),
    radial-gradient(ellipse at 82% 72%, rgba(108, 111, 224, 0.12), transparent 40%),
    radial-gradient(ellipse at 55% 12%, rgba(174, 219, 255, 0.1), transparent 32%);
  filter: blur(28px);
  animation: blue-drift 28s ease-in-out infinite alternate;
}

@keyframes blue-drift {
  0% { transform: translate3d(-2%, -1%, 0) scale(1); }
  50% { transform: translate3d(2%, 1.5%, 0) scale(1.04); }
  100% { transform: translate3d(-1%, 2%, 0) scale(1.02); }
}

a { color: var(--rust); text-decoration: none; transition: color 0.15s var(--ease); }
a:hover { text-decoration: underline; }
a:focus-visible, button:focus-visible { outline: 2px solid var(--rust); outline-offset: 3px; border-radius: 2px; }

.wrap {
  position: relative;
  z-index: 1;
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 24px;
}

/* Header */
header.site-header {
  padding: 56px 0 36px;
  border-bottom: 1px solid var(--rule);
  text-align: center;
}

.profile-image {
  display: block;
  width: 92px;
  height: 92px;
  margin: 0 auto 18px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--paper-raised);
  box-shadow: 0 0 0 1px var(--rule), 0 8px 20px rgba(33, 34, 35, 0.1);
}

header.site-header .handle {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 10px;
  font-family: var(--body-font);
  font-size: 2rem;
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
  font-family: var(--body-font);
  font-size: 0.86rem;
  margin: 0;
}

header.site-header .tagline .prompt { color: var(--ink-faint); }

/* Post list */
main { padding: 8px 0 100px; }

.post-item {
  display: block;
  padding: 32px 34px;
  margin: 0 0 28px;
  background: var(--paper-raised);
  border-bottom: 1px solid var(--rule-soft);
  border-radius: 12px;
  color: var(--ink);
  border: 1px solid var(--rule);
  box-shadow: 0 8px 24px rgba(33, 34, 35, 0.05);
}

.post-item:last-child { border-bottom: none; }

.post-content-preview {
  position: relative;
  max-height: 18rem;
  overflow: hidden;
}

.post-content-preview.is-truncated:not(.is-expanded)::after {
  content: "";
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  height: 5rem;
  pointer-events: none;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0), var(--paper-raised));
}

.post-content-preview.is-expanded {
  max-height: none;
}

.expand-button {
  display: block;
  width: 100%;
  margin: 18px 0 0;
  padding: 10px 0 0;
  border: 0;
  border-top: 1px solid var(--rule-soft);
  background: transparent;
  color: var(--rust);
  font: inherit;
  font-weight: 600;
  text-align: center;
  cursor: pointer;
}

.expand-button:hover { color: var(--ink); }
.expand-button[hidden] { display: none; }

.post-meta-row {
  margin-bottom: 12px;
  font-family: var(--body-font);
  font-size: 0.76rem;
  color: var(--ink-faint);
}

.post-title {
  font-family: var(--body-font);
  font-size: 1.55rem;
  font-weight: 600;
  margin: 0 0 9px;
  line-height: 1.32;
  letter-spacing: -0.008em;
  transition: color 0.15s var(--ease);
}

/* Single post */
article.post {
  padding: 16px 0 60px;
}

article.post .post-meta-row { margin-bottom: 20px; }

article.post h1 {
  font-family: var(--body-font);
  font-size: 2.15rem;
  font-weight: 600;
  line-height: 1.22;
  letter-spacing: -0.015em;
  margin: 0 0 22px;
}

.content {
  font-size: 1.06rem;
}

.content h2 {
  font-family: var(--body-font);
  font-size: 1.42rem;
  font-weight: 600;
  margin: 2em 0 0.6em;
  letter-spacing: -0.01em;
}

.content h3 {
  font-family: var(--body-font);
  font-size: 1.16rem;
  font-weight: 600;
  margin: 1.8em 0 0.5em;
}

.content p { margin: 0 0 1.25em; }

.content a {
  text-decoration: underline;
  text-decoration-color: var(--rule);
  text-underline-offset: 3px;
  transition: text-decoration-color 0.15s var(--ease);
}
.content a:hover { text-decoration-color: var(--rust); }

.content code {
  font-family: var(--body-font);
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.87em;
}

.content pre {
  background: var(--code-bg);
  padding: 20px 22px;
  border-radius: 10px;
  overflow-x: auto;
  margin: 0 0 1.5em;
  border: 1px solid var(--rule-soft);
}

.content pre code {
  background: none;
  padding: 0;
  font-size: 0.87rem;
  line-height: 1.6;
}

.content blockquote {
  margin: 0 0 1.5em;
  padding: 4px 0 4px 20px;
  border-left: 3px solid var(--rust);
  color: var(--ink-soft);
  font-style: italic;
}

.content ul, .content ol {
  margin: 0 0 1.25em;
  padding-left: 1.4em;
}

.content li { margin-bottom: 0.45em; }

.content table {
  width: max-content;
  min-width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.table-scroll {
  max-width: 100%;
  overflow-x: auto;
  margin: 0 0 1.5em;
  -webkit-overflow-scrolling: touch;
}

.content th,
.content td {
  padding: 10px 14px;
  border: 1px solid var(--rule);
  text-align: left;
}

.content th {
  background: var(--rule-soft);
  font-weight: 600;
  font-family: var(--body-font);
  font-size: 0.82rem;
  letter-spacing: 0.01em;
}

.content tr:nth-child(even) td {
  background: var(--paper-raised);
}

.content img {
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
  font-family: var(--body-font);
  font-size: 0.84rem;
  color: var(--ink-faint);
  transition: color 0.15s var(--ease), transform 0.15s var(--ease);
}

.back-link:hover { color: var(--rust); transform: translateX(-2px); }

/* Footer */
footer.site-footer {
  padding: 36px 0 60px;
  border-top: 1px solid var(--rule);
  font-family: var(--body-font);
  font-size: 0.78rem;
  color: var(--ink-faint);
}

footer.site-footer a { color: var(--ink-faint); }
footer.site-footer a:hover { color: var(--rust); }

.empty-state {
  padding: 48px 0;
  color: var(--ink-soft);
  font-family: var(--body-font);
  font-size: 0.9rem;
  text-align: center;
  border: 1px dashed var(--rule);
  border-radius: 12px;
}

::selection { background: var(--rust-soft); color: var(--ink); }

@media (max-width: 600px) {
  header.site-header { padding: 44px 0 28px; }
  header.site-header .handle { font-size: 1.75rem; }
  .post-item { margin: 0 0 20px; padding: 26px 20px; }
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
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
"""

HEADER_TEMPLATE = """
<div class="wrap">
  <header class="site-header">
    <img class="profile-image" src="{root}images/avatar.jpg" alt="Foto de perfil" onerror="this.style.display='none'">
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
            '<div class="empty-state">no posts yet &mdash; add an .html file to /posts and rebuild</div>'
        )

    for p in posts:
        items_html.append(f"""
    <article class="post-item">
      <div class="post-meta-row">
        <span>{html.escape(p['date'])}</span>
      </div>
      <h2 class="post-title">{html.escape(p['title'])}</h2>
      <div class="post-content-preview">
        <div class="content">
        {p['html']}
        </div>
      </div>
      <button class="expand-button" type="button" aria-expanded="false" hidden>↓ Show more</button>
    </article>""")

    html_out = HEAD_TEMPLATE.format(
        title="adriano-229 — notes on topics",
        description=html.escape(SITE_TAGLINE),
        root="",
    )
    html_out += HEADER_TEMPLATE.format(root="")
    html_out += f'<main>{"".join(items_html)}</main>'
    html_out += """
<script>
  const updateExpandButtons = () => {
    document.querySelectorAll(".expand-button").forEach((button) => {
      const preview = button.previousElementSibling;
      if (!preview.classList.contains("is-expanded")) {
        const isTruncated = preview.scrollHeight > preview.clientHeight;
        preview.classList.toggle("is-truncated", isTruncated);
        button.hidden = !isTruncated;
      }
    });
  };

  document.querySelectorAll(".expand-button").forEach((button) => {
    button.addEventListener("click", () => {
      const preview = button.previousElementSibling;
      const expanded = preview.classList.toggle("is-expanded");
      button.hidden = false;
      button.setAttribute("aria-expanded", String(expanded));
      button.textContent = expanded ? "↑ Show less" : "↓ Show more";
    });
  });

  updateExpandButtons();
  window.addEventListener("resize", updateExpandButtons);
</script>
"""
    html_out += FOOTER_TEMPLATE.format(year=datetime.now().year)
    return html_out


def build():
    OUT_DIR.mkdir(exist_ok=True)

    (OUT_DIR / "style.css").write_text(BASE_CSS, encoding="utf-8")

    posts = load_posts()

    (OUT_DIR / "index.html").write_text(render_index(posts), encoding="utf-8")
    generated_posts = OUT_DIR / "posts"
    if generated_posts.exists():
        for generated_page in generated_posts.iterdir():
            if generated_page.is_file():
                generated_page.unlink()
        generated_posts.rmdir()

    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Built {len(posts)} post(s) into {OUT_DIR}")


if __name__ == "__main__":
    build()
