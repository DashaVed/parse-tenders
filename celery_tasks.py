import re

import httpx
import xmltodict
from bs4 import BeautifulSoup
from celery import Celery, Task

from constants import URL, URL_XML, HEADERS

app = Celery("celery_tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")


class FetchTask(Task):

    def run(self, page_number: int, *args, **kwargs) -> list[str]:
        links = []
        response = httpx.get(f"{URL}{page_number}", headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all(href=re.compile("printForm/view")):
                links.append(link["href"])
        return links


class ParseXMLTask(Task):
    def run(self, reg_number: str, *args, **kwargs) -> str:
        response = httpx.get(f"{URL_XML}{reg_number}", headers=HEADERS)
        if response.status_code == 200:
            dict_data = xmltodict.parse(response.text)
            return dict_data[list(dict_data.keys())[0]]["commonInfo"]["publishDTInEIS"]


FetchTask = app.register_task(FetchTask())
ParseXMLTask = app.register_task(ParseXMLTask())
