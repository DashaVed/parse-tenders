import re
from urllib.parse import urlparse, parse_qs

import httpx
import xmltodict
from bs4 import BeautifulSoup

URL = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1"
URL_XML = "https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}


def parse_xml(reg_number: str) -> str:
    response = httpx.get(f"{URL_XML}{reg_number}", headers=HEADERS)
    if response.status_code == 200:
        dict_data = xmltodict.parse(response.text)
        return dict_data[list(dict_data.keys())[0]]["commonInfo"]["publishDTInEIS"]


def main():
    response = httpx.get(URL, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all(href=re.compile("printForm/view")):
            parsed_url = urlparse(link["href"])
            reg_number = parse_qs(parsed_url.query)["regNumber"][0]
            date = parse_xml(reg_number)
            print(f"{link['href']} - {date}")


if __name__ == "__main__":
    main()
