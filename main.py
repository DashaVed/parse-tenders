from urllib.parse import urlparse, parse_qs

import celery_tasks
from constants import PAGE_NUMBERS


def main():
    for page_number in range(1, PAGE_NUMBERS + 1):
        links = celery_tasks.FetchTask.delay(page_number)
        for link in links.get():
            reg_number: str = parse_qs(urlparse(link).query)["regNumber"][0]
            date = celery_tasks.ParseXMLTask.delay(reg_number)
            print(f"{link} - {date.get()}")


if __name__ == "__main__":
    main()
