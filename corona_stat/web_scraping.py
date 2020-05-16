from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

col_name = [
        "demo",
        "country",
        "total cases",
        "new cases",
        "total deaths",
        "new deaths",
        "total recovered",
        "active cases",
        "serious/ critical",
        "total cases/1M",
        "deaths/1M",
        "total tests",
        "test/1M population",
        "population",
        "region"
    ]


def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


class WebScrap:
    def __init__(self, url):
        self.url = url
        self.html = None

    def get_full_stat(self):
        table = self.html.find(id='main_table_countries_today')
        tbody = table.tbody
        rows = tbody.find_all('tr')

        corona_stat = []
        for tr in rows:
            row_stat = {}
            row = tr.find_all('td')
            ind = 0

            for td in row:
                text = td.text.strip()
                text = text.replace(',', '')
                if is_number(text):
                    text = int(text)
                row_stat[col_name[ind]] = text
                ind = ind + 1

            country = row[0].text.strip().lower()
            corona_stat.append(row_stat)

        return corona_stat

    def simple_get(self):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(get(self.url, stream=True)) as resp:
                if self.is_good_response(resp):
                    self.html = BeautifulSoup(resp.content, 'html.parser')
                    return resp.content
                else:
                    return None

        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None

    def is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    def log_error(self, e):
        """
        It is always a good idea to log errors.
        This function just prints them, but you can
        make it do anything.
        """
        print(e)
