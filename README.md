# adriano-229

A lightweight site for notes on CS topics. Write Markdown, push to GitHub, and the site builds and deploys itself.

## How it works

- You write posts as `.md` files in `/posts`
- `scripts/build.py` reads them and generates static HTML into `/docs`
- A GitHub Actions workflow (`.github/workflows/deploy.yml`) runs the build automatically on every push and publishes `/docs` to the `gh-pages` branch
- No database, no server, no JS framework — just Python turning Markdown into HTML

## Writing a new post

Create a new file in `/posts`. The date-prefixed naming convention (`YYYY-MM-DD-slug.md`) is just for tidiness in your file browser — the `date` field in the frontmatter is what actually controls sort order.

Every post needs frontmatter like this:

```markdown
---
title: Your post title
date: 2026-08-01
excerpt: One sentence that shows up on the homepage.
---

Write your post in regular Markdown here. Headings, `code`, **bold**,
> blockquotes, lists, images, tables — all supported.
```

**Optional video embed** — add a `video_url` field with a YouTube link:

```markdown
---
title: My talk on B-trees
date: 2026-08-01
video_url: https://www.youtube.com/watch?v=XXXXXXXXXXX
excerpt: A walkthrough of B-tree indexing in databases.
---

Optional write-up goes here below the embedded video.
```

## Previewing locally

```bash
python3 scripts/build.py
```

Regenerates everything in `/docs`. Open `docs/index.html` in a browser, or serve it locally:

```bash
cd docs && python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploying to GitHub Pages

1. Create a repo on GitHub — name it `adriano-229.github.io` if you want the site at the root domain, or anything else if a subpath URL is fine
2. Push this folder to that repo's `main` branch
3. In repo Settings → **Pages**, set the source to the `gh-pages` branch (the Action creates this branch automatically on first run)
4. Push a commit — the site goes live at `https://adriano-229.github.io/` (or `https://adriano-229.github.io/<repo-name>/` if you used a different repo name)

From then on, every push that touches `/posts` rebuilds and republishes automatically.

## Customizing

- **Colors, fonts, spacing** — in `scripts/build.py`, inside the `BASE_CSS` string
- **Site name / tagline** — in `HEADER_TEMPLATE` and `SITE_TAGLINE`, same file

## Project structure

```
.
├── posts/                   ← write your .md posts here
├── docs/                    ← generated site (do not edit by hand)
├── scripts/
│   └── build.py              ← the whole site generator
├── .github/workflows/
│   └── deploy.yml             ← auto-build + deploy on push
└── README.md
```
