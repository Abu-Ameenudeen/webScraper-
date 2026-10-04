from urllib.parse import urlsplit


def normalize_url(input_url):
    url = urlsplit(input_url)
    return url.netloc + url.path