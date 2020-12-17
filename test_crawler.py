from crawler import WebCrawler
import unittest


class WebCrawlerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.webCrawler = WebCrawler("http://rescale.com/about")

    def tearDown(self):
        pass

    def test_rool_url(self):
        self.assertEqual(self.webCrawler.root_url, "http://rescale.com")

    def test_parse_links(self):
        f = open("test.html", "r")
        html = f.read()
        f.close()
        self.webCrawler.parse_links(html)
        # expecting 2, base url and link in the html file
        self.assertEqual(self.webCrawler.unvisited_url.qsize(), 4)
        
        self.webCrawler.parse_links(None)
        self.assertEqual(self.webCrawler.unvisited_url.qsize(), 4)

    def test_run_crawler(self):
        

if __name__ == "__main__":
    unittest.main()
