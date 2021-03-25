#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 21:08:56 2020

@author: hypo
"""

import cv2
import sys
import os
import pickle
import logging
import time

from libs.HTMLSimilarity.htmlparser import HTMLParser
from libs.HTMLSimilarity.domtree2data import Converter
from libs.HTMLSimilarity.calc import calculated_similarity


logging.basicConfig(stream=sys.stdout, format="%(levelname)s: %(asctime)s: %(message)s", level=logging.INFO, datefmt='%a %d %b %Y %H:%M:%S')
log = logging.getLogger(__name__)

class HTMLSimilarityWrapper:
    def __init__(self):
        self._dimension = 5000

    def _get_dom_eigenvector(self, file_in_check):
        with open(file_in_check, 'r') as frh:
            hp = HTMLParser(frh)
            html_doc_dom_tree = hp.get_dom_structure_tree()
            converter = Converter(html_doc_dom_tree, self._dimension)
        return converter.get_eigenvector()

    def _get_similarity(self, dom1_eigenvector, dom2_eigenvector):
        value = calculated_similarity(dom1_eigenvector, dom2_eigenvector, self._dimension)
        if value > 0.2:
            return False, value
        else:
            return True, value

    def search_html(self, file, db_file):
        retMe = {}
        if not os.access(db_file, os.R_OK):
            log.info("build db first")
            return
        with open(db_file, 'rb') as f:
            db = pickle.load(f)

        dom_eigenvector = self._get_dom_eigenvector(file)
        for k, v in db.items():
            try:
                B, R = self._get_similarity(dom_eigenvector, v["eigenvector"])
            except:
                log.error("error matching".format(k))
                continue

            # R = float(len(good)) * 2 / (len(des) + len(v["des"]))
            retMe[k] = R

        return retMe

    def build_db(self, path, db_file):
        '''
        db formant:
        path: {"des": des}
        '''
        # "html", "html5", "xml"

        html_extension = [".html", ".htm", ".xml"] # check BeautifulSoup.init
        if not os.access(db_file, os.R_OK):
            db = {}
        else:
            with open(db_file, 'rb') as f:
                db = pickle.load(f)

        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                file_in_check = os.path.join(os.path.abspath(dirpath), f)
                if not os.path.isfile(file_in_check):
                    continue
                if db.__contains__(file_in_check):
                    continue
                if os.path.splitext(file_in_check)[-1].lower() not in html_extension:
                    continue

                try:
                    dom_eigenvector = self._get_dom_eigenvector(file_in_check)
                except:
                    log.error("error when processing: {}".format(file_in_check))
                    continue

                db[file_in_check] = {"eigenvector": dom_eigenvector}

        log.info("total {} html files are found".format(len(db)))

        with open(db_file, 'wb') as f:
            pickle.dump(db, f)

def main():
    '''
    1. build the db firstly.
    2. then feed an html file and get the result.
    '''
    begin = time.time()

    m = HTMLSimilarityWrapper()

    # "build db firstly"
    m.build_db("../../working_folder", "All.pkl")

    "compare one by one"
    html = "/Users/panmac/Desktop/workspace/WebAppSecProj/ResExtractor/working_folder/yingyuan.2021.01.12/APICloud/882f9292700f68b221f7716b7bceec9b50b1892f/localres/widget/error/error.html"
    res = m.search_img(html, "../../img.db.pkl")
    for i in sorted(res.items(), key=lambda kv: (kv[1], kv[0]), reverse=False):
        log.info(i)

    end = time.time()
    print(end - begin)

if __name__== "__main__":
    sys.exit(main())
