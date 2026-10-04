from urllib.parse import urlsplit


def normalize_url(input_url):
    url = urlsplit(input_url)
    return url.netloc + url.path


def get_heading_from_html(html: str) -> str:
    pass
