import unittest

from wiki.creole_parser import parse

class CreoleParsingTests(unittest.TestCase):
    def test_link_to_wiki_page(self):
        self.assertEquals(parse('[[foo]]'),
                          u'<p><a href="/foo/">foo</a></p>\n')

    def test_link_to_wiki_subpage(self):
        self.assertEquals(parse('[[foo/bar]]'),
                          u'<p><a href="/foo/bar/">foo/bar</a></p>\n')

    def test_link_to_other_site_page(self):
        self.assertEquals(parse('[[/foo]]'),
                          u'<p><a href="/foo">/foo</a></p>\n')

    def test_external_link(self):
        self.assertEquals(parse('[[http://example.com]]'),
                          u'<p><a href="http://example.com">http://example.com</a></p>\n')
