from crawler import WebCrawler
import unittest


class WebCrawlerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.webCrawler = WebCrawler("https://google.com")

    def tearDown(self):
        pass


    def test_parse_html(self):
        f = open("test.html", "r")
        html = f.read()
        f.close()
        self.webCrawler.parse_html(html)
        # expecting 6, base url and links in the html file
        self.assertEqual(self.webCrawler.unvisited_url.qsize(), 6)
        
        # testing if absolute link is  built from relative url 
        self.assertTrue("https://google.com/about" in self.webCrawler.unvisited_url.queue)
        self.assertTrue("https://google.com/help" in self.webCrawler.unvisited_url.queue)
    
    def test_fetch(self):
        
        # test if fetch not fails for unexpected inputs
        try:
            self.webCrawler.fetch("randomtext")
            self.webCrawler.fetch("")
            self.webCrawler.fetch(None)
        except Exception:
            self.fail("fetch() raised Exception unexpectedly!")
    

if __name__ == "__main__":
    unittest.main()
