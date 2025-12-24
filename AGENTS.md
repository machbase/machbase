# Repository Guidelines

## Project Structure & Module Organization
- Source markdown sits in `content/`; Korean Machbase Neo docs live in `content/kr/neo/`, with each landing page using `_index.md` and topic details using `index.md` leaf bundles.
- Shared visual assets reside in `assets/`, fingerprinted static files go in `static/`, and reusable layouts/shortcodes live in `layouts/partials/`; adjust theme modules through `go.mod` from the repo root so Hugo resolves `github.com/imfing/hextra`.
- Keep locale folders structurally parallel, staging new English references under `content/en/` before coordinating translations.

## Build, Test, and Development Commands
- `hugo server -D` launches a hot-reload preview (including drafts) at `http://localhost:1313/neo/`; watch the console for 404s or shortcode warnings.
- `hugo --gc --minify` creates the publishable site in `public/`, removing unused resources.
- `hugo mod tidy` refreshes theme dependencies after upgrading modules or pulling upstream changes.

## Coding Style & Naming Conventions
- Author Markdown in UTF-8, keeping lines near 100 chars; indent nested lists with two spaces and prefer imperative headings consistent with “Machbase Neo” and “TQL”.
- Front matter must include `title`, `weight`, and `toc`; add optional keys like `description` only when required.
- Store screenshots beneath `static/images/` and reference them via site-relative paths like `/images/neo-dashboard.png`.

## Testing Guidelines
- Run `hugo --printUnusedTemplates --printI18nWarnings` before pushing to surface unresolved partials or translation misses.
- Validate new links in the `hugo server` console; add quick-start `bash` blocks for lengthy tutorials so reviewers can reproduce steps quickly.

## Commit & Pull Request Guidelines
- Follow the short, scoped commit format seen in history (example: `api-http: clarify payload limits`) and group related locale edits together.
- Reference issue IDs in the commit body when available and list touched sections such as `content/kr/neo/api-grpc/index.md`.
- PRs should summarize scope, mention new media, and attach screenshots or terminal captures when UX or CLI output changes.

## Localization & Terminology Coordination
- Align Korean wording with glossary entries under `i18n/`; add new terminology there before publishing.
- Keep English and Korean structures synchronized by staging source material under `content/en/` and mirroring section bundles in `content/kr/neo/`.
