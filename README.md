# Boot.dev Web Scraper

A Python web crawler built as part of the [Boot.dev](https://www.boot.dev/) Backend Developer course.

The project progressively builds a web scraper that can crawl a website, extract useful page information, handle concurrent requests, limit the number of pages crawled, and generate a JSON report.

## Features

- URL normalization
- HTML parsing with Beautiful Soup
- Extract page headings (`h1` / `h2`)
- Extract the first paragraph
- Extract outgoing links
- Extract image URLs
- Convert relative URLs to absolute URLs
- Fetch HTML pages using `aiohttp`
- Recursive website crawling
- Asynchronous/concurrent crawling
- Configurable request concurrency
- Configurable maximum number of pages
- Duplicate URL detection
- Same-domain crawling
- JSON report generation

## Tech Stack

- Python
- Beautiful Soup
- aiohttp
- asyncio
- uv
- JSON

## Project Structure

```text
bootDevWebScrapper/
├── crawl.py
├── json_report.py
├── main.py
├── test_crawl.py
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
