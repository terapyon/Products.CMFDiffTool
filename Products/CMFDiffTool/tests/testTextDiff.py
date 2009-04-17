# -*- coding: utf-8 -*-
#
# CMFDiffTool tests
#

from Testing import ZopeTestCase
from Products.CMFDiffTool.TextDiff import TextDiff
        
_marker = []

class A:
    attribute = "कामसूत्र"
    def method(self):
        return "method कामसूत्र"

class B:
    attribute = "karôshi"
    def method(self):
        return "method karôshi"

class TestTextDiff(ZopeTestCase.ZopeTestCase):
    """Test the TextDiff class"""

    def testInterface(self):
        """Ensure that tool instances implement the portal_diff interface"""
        from Products.CMFDiffTool.interfaces.portal_diff import IDifference
        self.failUnless(IDifference.isImplementedByInstancesOf(TextDiff))
    
    def testAttributeSame(self):
        """Test attribute with same value"""
        a = A()
        fd = TextDiff(a, a, 'attribute')
        self.failUnless(fd.same)

    def testMethodSame(self):
        """Test method with same value"""
        a = A()
        fd = TextDiff(a, a, 'method')
        self.failUnless(fd.same)

    def testAttributeDiff(self):
        """Test attribute with different value"""
        a = A()
        b = B()
        fd = TextDiff(a, b, 'attribute')
        self.failIf(fd.same)

    def testMethodDiff(self):
        """Test method with different value"""
        a = A()
        b = B()
        fd = TextDiff(a, b, 'method')
        self.failIf(fd.same)

    def testGetLineDiffsSame(self):
        """test getLineDiffs() method with same value"""
        a = A()
        fd = TextDiff(a, a, 'attribute')
        expected = [('equal', 0, 1, 0, 1)]
        self.assertEqual(fd.getLineDiffs(), expected)

    def testGetLineDiffsDifferent(self):
        """test getLineDiffs() method with different value"""
        a = A()
        b = B()
        fd = TextDiff(a, b, 'attribute')
        expected = [('replace', 0, 1, 0, 1)]
        self.assertEqual(fd.getLineDiffs(), expected)
        
    def testSameText(self):
        """Test text diff output with same value"""
        a = A()
        fd = TextDiff(a, a, 'attribute')
        self.assertEqual(fd.ndiff(), '  कामसूत्र')

    def testDiffText(self):
        """Test text diff output with different value"""
        a = A()
        b = B()
        expected = "- कामसूत्र\n+ karôshi"
        fd = TextDiff(a, b, 'attribute')
        self.assertEqual(fd.ndiff(), expected)

    def testUnifiedDiff(self):
        """Test text diff output with different value"""
        a = A()
        b = B()
        expected = """--- None 

+++ None 

@@ -1,1 +1,1 @@

-कामसूत्र
+karôshi"""
        fd = TextDiff(a, b, 'attribute')
        self.assertEqual(fd.unified_diff(), expected)

    def testHTMLDiff(self):
        """Test text diff output with different value"""
        a = A()
        b = B()
        expected = """
    <table class="diff" id="difflib_chg_to0__top"
           cellspacing="0" cellpadding="0" rules="groups" >
        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
        <thead><tr><th class="diff_next"><br /></th><th colspan="2" class="diff_header">None</th><th class="diff_next"><br /></th><th colspan="2" class="diff_header">None</th></tr></thead>
        <tbody>
            <tr><td class="diff_next" id="difflib_chg_to0__0"><a href="#difflib_chg_to0__top">t</a></td><td class="diff_header" id="from0_1">1</td><td nowrap="nowrap"><span class="diff_sub">\xe0\xa4\x95\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xb8\xe0\xa5\x82\xe0\xa4\xa4\xe0\xa5\x8d\xe0\xa4\xb0</span></td><td class="diff_next"><a href="#difflib_chg_to0__top">t</a></td><td class="diff_header" id="to0_1">1</td><td nowrap="nowrap"><span class="diff_add">kar\xc3\xb4shi</span></td></tr>
        </tbody>
    </table>"""
        fd = TextDiff(a, b, 'attribute')
        self.assertEqual(fd.html_diff(), expected)

def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTextDiff))
    return suite
