from urllib.parse import (
    urlsplit,
    urljoin,
)
from bs4 import BeautifulSoup, Tag


def normalize_url(input_url):
    url = urlsplit(input_url)
    return (
        (url.netloc + url.path).rstrip("/").lower()
    )


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    
    h_tag = soup.find("h1")
    
    if not isinstance(h_tag, Tag):
        h_tag = soup.find("h2")
    
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main = soup.find("main")

    if isinstance(main, Tag):
        p_tag = main.find("p")
        if isinstance(p_tag, Tag):
            return p_tag.get_text(strip=True)

    p_tag = soup.find("p")

    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""    


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")

    urls = []

    for link in links:
        href = link.get("href")

        if href:
            urls.append(urljoin(base_url, href))

    return urls


def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")

    urls = []

    for image in images:
        src = image.get("src")

        if src:
            urls.append(urljoin(base_url, src))

    return urls


def extract_page_data(html: str, page_url: str):
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }
