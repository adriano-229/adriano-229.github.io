import html
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS_DIR = ROOT / "posts"
OUT_DIR = ROOT / "docs"
ASSETS_DIR = OUT_DIR / "assets"
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
            r'<div\b[^>]*class=["\'][^"\']*\bcontent\b[^"\']*["\'][^>]*>(.*)</div>',
            article_body,
            re.DOTALL | re.IGNORECASE,
        )
        if not content_match:
            print(f"WARNING: {f.name} is missing a content div, skipping")
            continue
        content = content_match.group(1).strip()
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


HEAD_TEMPLATE = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{title}</title>\n<meta name="description" content="{description}">\n<link rel="stylesheet" href="{root}style.css">\n<script src="{root}script.js" defer></script>\n</head>\n<body>\n'

HEADER_TEMPLATE = '\n<div class="wrap">\n  <header class="site-header">\n    <img class="profile-image" src="{root}images/avatar.jpg" alt="Foto de perfil" onerror="this.style.display=\'none\'">\n    <p class="handle"><a href="{root}index.html">adriano-229</a><span class="dot" aria-hidden="true"></span></p>\n    <p class="tagline"><span class="prompt">$</span> notes on topics</p>\n  </header>\n'

FOOTER_TEMPLATE = '\n  <footer class="site-footer">\n    <p>&copy; {year} adriano-229 &mdash; built with claude</p>\n  </footer>\n</div>\n</body>\n</html>\n'


def render_post(post):
    article = f"""
<article class="post">
  <div class="post-meta-row">
    <span>{html.escape(post['date'])}</span>
  </div>
  <h1>{html.escape(post['title'])}</h1>
  <div class="content">
{post['html']}
  </div>
</article>"""

    html_out = HEAD_TEMPLATE.format(
        title=f"{post['title']} — {SITE_NAME}",
        description=html.escape(SITE_TAGLINE),
        root="../",
    )
    html_out += HEADER_TEMPLATE.format(root="../")
    html_out += f"<main>{article}</main>"
    html_out += FOOTER_TEMPLATE.format(year=datetime.now().year)
    return html_out


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
    html_out += FOOTER_TEMPLATE.format(year=datetime.now().year)
    return html_out


def copy_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for source in ROOT.glob("posts/**/assets/**/*"):
        if not source.is_file():
            continue
        relative = source.relative_to(POSTS_DIR)
        parts = relative.parts
        if len(parts) > 2 and parts[1] == "assets":
            destination = ASSETS_DIR / Path(*parts[2:])
        elif parts and parts[0] == "assets":
            destination = ASSETS_DIR / Path(*parts[1:])
        else:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build():
    OUT_DIR.mkdir(exist_ok=True)
    copy_assets()

    posts = load_posts()

    (OUT_DIR / "index.html").write_text(render_index(posts), encoding="utf-8")

    generated_posts = OUT_DIR / "posts"
    if generated_posts.exists():
        shutil.rmtree(generated_posts)
    generated_posts.mkdir()
    for post in posts:
        page = generated_posts / f"{post['filename']}.html"
        page.write_text(render_post(post), encoding="utf-8")

    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Built {len(posts)} post(s) into {OUT_DIR}")


if __name__ == "__main__":
    build()
