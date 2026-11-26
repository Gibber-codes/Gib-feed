# GibberFeed

My own swipe feed for AI and cool science, to scroll instead of YouTube reels.

- `index.html` is the whole app: full-screen cards, topics, saves (stored on the phone).
- `feed.json` holds the cards. `tools/seed.py` writes the hand-picked ones.
- `tools/refresh.mjs` pulls the newest videos and posts from the channels and blogs listed in `feed.json`.
- `.github/workflows/refresh.yml` runs the refresh every morning and publishes to GitHub Pages.

To add or drop a source, edit `sources` in `feed.json`.
