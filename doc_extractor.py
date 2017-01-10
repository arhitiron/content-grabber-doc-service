import logging
import sys

import unicodedata

from dto.doc_dto import DocDto


# TODO: Temporary implementation, it should looks like dsl parser

def transform(string):
    return unicodedata.normalize('NFKD', string).encode('utf-8', 'ignore').strip().replace('  ', '')


class DocExtractor:
    def __init__(self, parser_raw_data):
        self._parser_raw_data = parser_raw_data

    # TODO: should be configurable
    def is_document(self):
        doc_title_box = self._parser_raw_data.findAll("div", {"class": "offer-titlebox"})
        if doc_title_box:
            return True
        else:
            return False

    # TODO: should be configurable
    def get_document(self):
        doc = DocDto(title=self._get_title(),
                     description=self._get_description(),
                     location=self._get_location(),
                     date=self._get_publish_date(),
                     author=self._get_author(),
                     author_location=self._get_author_location())
        return doc

    def _get_title(self):
        try:
            doc_title_box = self._parser_raw_data.findAll("div", {"class": "offer-titlebox"})
            if doc_title_box:
                title_box = doc_title_box.pop()
                title = title_box('h1').pop().next.strip()
                return transform(title)
        except:
            logging.info("Catch exception:")
            logging.info(sys.exc_info()[0])
        return ""

    def _get_description(self):
        try:
            description_content = self._parser_raw_data.findAll("div", {"class": "descriptioncontent"})
            if description_content:
                description = description_content.pop()
                pretty_desc = description.prettify()
                description = pretty_desc.replace('\n', '').replace('\r', '')
                return description
        except:
            logging.info("Catch exception:")
            logging.info(sys.exc_info()[0])
        return ""

    def _get_location(self):
        try:
            title_box_details = self._parser_raw_data.findAll("div", {"class": "offer-titlebox__details"})
            if title_box_details:
                details = title_box_details.pop()
                location = details('a').pop().next.next
                return transform(location)
        except:
            logging.info("Catch exception:")
            logging.info(sys.exc_info()[0])
        return ""

    def _get_publish_date(self):
        try:
            title_box_details = self._parser_raw_data.findAll("div", {"class": "offer-titlebox__details"})
            if title_box_details:
                details = title_box_details.pop()
                date = details('em').pop().next
                return transform(date)
        except:
            logging.info("Catch exception:")
            logging.info(sys.exc_info()[0])
        return ""

    def _get_author(self):
        try:
            user_details = self._parser_raw_data.findAll("div", {"class": "offer-user__details"})
            if user_details:
                details = user_details.pop()
                user = details('a').pop().next
                return transform(user)
        except:
            logging.info("Catch exception:")
            logging.info(sys.exc_info()[0])
        return ""

    def _get_author_location(self):
        try:
            user_details = self._parser_raw_data.findAll("div", {"class": "offer-user__location"})
            if user_details:
                details = user_details.pop()
                user = details('p').pop().next
                return transform(user)
        except:
            logging.info("Catch exception:")
            logging.info(sys.exc_info()[0])
        return ""
