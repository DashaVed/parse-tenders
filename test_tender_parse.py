from random import randint
from urllib.parse import urlparse, parse_qs

import celery_tasks


def test_fetch_links():
    page_number = randint(1, 10)
    links = celery_tasks.FetchTask.run(page_number)

    assert len(links) == 10
    assert type(parse_qs(urlparse(links[0]).query)["regNumber"][0]) == str


def test_parse_xml():
    reg_number = "0338300047924000057"
    publish_date = celery_tasks.ParseXMLTask.run(reg_number)

    assert publish_date == "2024-03-16T17:42:49.541+12:00"
