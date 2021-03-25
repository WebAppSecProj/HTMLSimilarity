# -*- coding: utf-8 -*-

"""
@author: taoqi
@file: HTMLSimilarity.py
@time: 2019-07-02 16:57
"""
import sys
import logging

from libs.HTMLSimilarity.htmlparser import HTMLParser
from libs.HTMLSimilarity.domtree2data import Converter
from libs.HTMLSimilarity.calc import calculated_similarity


logging.basicConfig(stream=sys.stdout, format="%(levelname)s: %(asctime)s: %(message)s", level=logging.INFO, datefmt='%a %d %b %Y %H:%M:%S')
log = logging.getLogger(__name__)

def get_html_similarity(html_doc1, html_doc2, dimension=5000):
    hp1 = HTMLParser(html_doc1)
    html_doc1_dom_tree = hp1.get_dom_structure_tree()
    hp2 = HTMLParser(html_doc2)
    html_doc2_dom_tree = hp2.get_dom_structure_tree()
    converter = Converter(html_doc1_dom_tree, dimension)
    dom1_eigenvector = converter.get_eigenvector()
    converter = Converter(html_doc2_dom_tree, dimension)
    dom2_eigenvector = converter.get_eigenvector()
    value = calculated_similarity(dom1_eigenvector, dom2_eigenvector, dimension)
    if value > 0.2:
        return False, value
    else:
        return True, value


def main():
    s, r = get_html_similarity(
        open("/Users/panmac/Desktop/workspace/WebAppSecProj/ResExtractor/working_folder/kaizhi.2021.01.11/APICloud/6a4244e94ebfa68ab1a625f900427cacbb9f3150/localres/index.html"),
        #open("/Users/panmac/Desktop/workspace/WebAppSecProj/ResExtractor/working_folder/kaizhi.2021.01.11/APICloud/015d85fa9fdceef340f4a5c69b9d085357a8503c/localres/index.html")
        open("/Users/panmac/Desktop/workspace/WebAppSecProj/ResExtractor/working_folder/kaizhi.2021.01.11/Cordova/9715c1fffc9b6beb1860b3e93dee2b8071b9ac15/localres/index.html")
    )
    log.info("similarity: {}, ratio: {}".format(s, r))
    return

if __name__== "__main__":
    sys.exit(main())
