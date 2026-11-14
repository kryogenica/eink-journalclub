# eink-journalclub

Publishes the title of the newest [journalclub.io](https://journalclub.io/episodes) episode as
`episode.json`, so an e-ink dashboard page can display it.

Journal Club's site cannot be loaded directly by another web page, so a scheduled GitHub Actions
job fetches the public episodes page about once an hour (no login) and commits the newest title
here. The dashboard then reads:

    https://raw.githubusercontent.com/kryogenica/eink-journalclub/main/episode.json

Only the episode title, its ID and its publication time are stored.
