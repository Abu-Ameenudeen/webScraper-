import unittest
from crawl import (
    normalize_url,
    get_heading_from_html, 
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data,    
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
        
    def test_normalize_url_protocol(self) -> None:
        input_url = "https://crawler-test.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_slash(self) -> None:
        input_url = "https://crawler-test.com/path/"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_capitals(self) -> None:
        input_url = "https://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http(self) -> None:
        input_url = "http://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)
        
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"

        actual = get_heading_from_html(input_body)

        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self):
        input_body = "<html><body><h2>Test Subtitle</h2></body></html>"

        actual = get_heading_from_html(input_body)

        expected = "Test Subtitle"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_heading(self):
        input_body = "<html><body><p>No heading</p></body></html>"

        actual = get_heading_from_html(input_body)

        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_basic(self):
        input_body = "<html><body><p>First paragraph.</p></body></html>"

        actual = get_first_paragraph_from_html(input_body)

        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""

        actual = get_first_paragraph_from_html(input_body)

        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self):
        input_body = "<html><body><h1>Only heading</h1></body></html>"

        actual = get_first_paragraph_from_html(input_body)

        expected = ""
        self.assertEqual(actual, expected)
        
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com">Boot.dev</a></body></html>'

        actual = get_urls_from_html(input_body, input_url)

        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/blog">Blog</a></body></html>'

        actual = get_urls_from_html(input_body, input_url)

        expected = ["https://crawler-test.com/blog"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <a href="/blog">Blog</a>
            <a href="/about">About</a>
            <a href="https://example.com">Example</a>
        </body></html>"""

        actual = get_urls_from_html(input_body, input_url)

        expected = [
            "https://crawler-test.com/blog",
            "https://crawler-test.com/about",
            "https://example.com",
        ]
        self.assertEqual(actual, expected)
        
    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png"></body></html>'

        actual = get_images_from_html(input_body, input_url)

        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'

        actual = get_images_from_html(input_body, input_url)

        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="Logo"></body></html>'

        actual = get_images_from_html(input_body, input_url)

        expected = []
        self.assertEqual(actual, expected)
    
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }

        self.assertEqual(actual, expected)
        
    def test_extract_page_data_empty(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body></body></html>"

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }

        self.assertEqual(actual, expected)
        
    def test_extract_page_data_multiple_links_and_images(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h2>Test Heading</h2>
            <p>Test paragraph.</p>
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <img src="/image1.jpg">
            <img src="/image2.jpg">
        </body></html>"""

        actual = extract_page_data(input_body, input_url)

        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Heading",
            "first_paragraph": "Test paragraph.",
            "outgoing_links": [
                "https://crawler-test.com/page1",
                "https://crawler-test.com/page2",
            ],
            "image_urls": [
                "https://crawler-test.com/image1.jpg",
                "https://crawler-test.com/image2.jpg",
            ],
        }

        self.assertEqual(actual, expected)
        
        
if __name__ == "__main__":
    unittest.main()