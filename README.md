# adriano-229

A lightweight site for notes on CS topics. Write HTML posts, push to GitHub, and the site builds and deploys itself.

## How it works

- You write posts as `.html` files in `/posts`
- `build.py` reads their `<article>` elements and glues them into `docs/index.html`
- A GitHub Actions workflow (`.github/workflows/deploy.yml`) runs the build automatically on every push and publishes `/docs` to the `gh-pages` branch

## Writing a new post

Create a new file in `/posts`.

Each post is a regular HTML document containing one article. The article must include a
`post-meta-row` with a date and an `h1` title:

```html
<article class="post">
  <div class="post-meta-row"><span>Oct 23, 2026</span></div>
  <h1>My talk on B-trees</h1>
  <div class="content">
    <p>Optional write-up goes here.</p>
  </div>
</article>
```

The builder does not convert Markdown or generate individual post pages. It only combines
the articles into the home page, so write the HTML you want displayed directly in each file.
Tables are automatically placed in horizontal scroll containers when they are wider than a post.

## Previewing locally

```bash
python3 build.py
```

Regenerates `docs/index.html` and `docs/style.css`. Open `docs/index.html` in a browser, or serve it locally:

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

- **Font** — change `--body-font` and `--body-font-size` in the `:root` section of the
  `BASE_CSS` string in `build.py`.
- **Background** — change `--paper` for the page color, or edit `body::before` in the
  same `BASE_CSS` block to replace the decorative background gradients.
- **Post width** — change `--max-w` in `:root`; it controls the centered site and post width.
- **Colors, spacing, borders, and tables** — edit the other variables and selectors in
  `BASE_CSS`. The build copies this CSS to `docs/style.css`.
- **Profile image** — add your image as `docs/images/avatar.jpg`; it is displayed as a
  circular image in the centered header.
- **Site name / tagline** — in `HEADER_TEMPLATE` and `SITE_TAGLINE`, same file

## Project structure

```
.
├── posts/                   ← write your .html posts here
├── docs/                    ← generated site (do not edit by hand)
├── build.py                 ← the whole site generator
├── .github/workflows/
│   └── deploy.yml             ← auto-build + deploy on push
└── README.md
```
