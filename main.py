import logging
import os
import time

from bs4 import BeautifulSoup

from consumer import Consumer
from doc_extractor import DocExtractor
from dto.raw_data_dto import RawDataDto
from producer import Producer
from raw_data_provider import RawDataProvider

ADDR = os.environ['ADDRESS']
KAFKA_ADDR = os.environ['KAFKA_ADDRESS']
RAW_QUEUE_TOPIC = os.environ['RAW_QUEUE_TOPIC']
LINK_QUEUE_TOPIC = os.environ['LINK_QUEUE_TOPIC']
DOC_QUEUE_TOPIC = os.environ['DOC_QUEUE_TOPIC']
RESOURCE_CACHE_ADDRESS = os.environ['RESOURCE_CACHE_ADDRESS']


class DocService(object):
    # TODO: add default values
    def __init__(self, kafka_addr, link_queue_topic, raw_queue_topic,
                 doc_queue_topic, resource_cache_address):
        self._raw_data_producer = Producer(kafka_addr, raw_queue_topic)
        self._doc_producer = Producer(kafka_addr, doc_queue_topic)
        self._link_consumer = Consumer(kafka_addr, link_queue_topic)
        self._raw_data_provider = RawDataProvider(resource_cache_address)

        self.serve()

    def serve(self):
        self._link_consumer.add_handler(self.handle_link)
        self._raw_data_producer.start()
        self._doc_producer.start()
        self._link_consumer.start()

    def handle_link(self, link):
        logging.log(logging.INFO, "Handle link: " + link)
        raw_data = self._raw_data_provider.get_data(link)
        parser_raw_data = BeautifulSoup(raw_data)
        extractor = DocExtractor(parser_raw_data)
        if extractor.is_document():
            doc = extractor.get_document()
            doc.url = link
            self._doc_producer.add_message(doc)
        else:
            raw_data_dto = RawDataDto(raw_data, link)
            self._raw_data_producer.add_message(raw_data_dto)


def main():
    DocService(kafka_addr=KAFKA_ADDR, link_queue_topic=LINK_QUEUE_TOPIC, raw_queue_topic=RAW_QUEUE_TOPIC,
               doc_queue_topic=DOC_QUEUE_TOPIC, resource_cache_address=RESOURCE_CACHE_ADDRESS)

    # TODO: change to long time leave
    while True:
        time.sleep(20)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()
