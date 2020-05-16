from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from .web_scraping import WebScrap
from .pdf import pdf_read


def total_info(html, text):
    element = html.find(string=text).parent.next_sibling.next_sibling
    text = element.text.strip()
    return text


def case_info(cur_element, isParcent=None):
    if isParcent is None:
        element = cur_element.parent.span
    else:
        element = cur_element.parent.strong
    return element.text.strip()


def active_cases_info(html):
    content = {}
    try:
        element = html.find(string="Currently Infected Patients").parent
        active_case_element = element.parent.div
        active_cases = active_case_element.text.strip()

        element = html.find(string="in Mild Condition").parent
        mild_cases_number = case_info(element)
        mild_cases_percent = case_info(element, True)

        element = html.find(string="Serious or Critical").parent
        serious_cases_number = case_info(element)
        serious_cases_percent = case_info(element, True)
    except:
        print('error occurred during html parsing')

    else:
        content = {
            "active_cases": active_cases,
            "mild_cases_number": mild_cases_number,
            "mild_cases_percent": mild_cases_percent,
            "serious_cases_number": serious_cases_number,
            "serious_cases_percent": serious_cases_percent
        }
    return content


def closed_cases_info(html):
    content = {}
    try:
        element = html.find(string="Cases which had an outcome:").parent
        closed_case_element = element.parent.div
        closed_cases = closed_case_element.text.strip()

        element = html.find(string="Recovered / Discharged").parent
        recovered_cases_number = case_info(element)
        recovered_cases_percent = case_info(element, True)

        element = html.find(string="Deaths").parent
        death_cases_number = case_info(element)
        death_cases_percent = case_info(element, True)
    except:
        print('error occurred during html parsing')

    else:
        content = {
            "closed_cases": closed_cases,
            "closed_cases_number": recovered_cases_number,
            "closed_cases_percent": recovered_cases_percent,
            "death_cases_number": death_cases_number,
            "death_cases_percent": death_cases_percent
        }
    return content


def get_content(html):
    html = BeautifulSoup(html, 'html.parser')
    total_cases = total_info(html, "Coronavirus Cases:")
    total_deaths = total_info(html, "Deaths:")
    total_recovered = total_info(html, "Recovered:")
    content = {
        "cases": total_cases,
        "deaths": total_deaths,
        "recovered": total_recovered
    }
    #get_full_stat(html, "")
    return closed_cases_info(html)
    return active_cases_info(html)
    print(content)
    return content


class CoronaStatList(APIView):
    def get(self, request, format=None):
        url = 'https://www.worldometers.info/coronavirus/'
        web_scrap = WebScrap(url)
        res = web_scrap.simple_get()

        if res is None:
            return Response('error', status=status.HTTP_400_BAD_REQUEST)

        content = web_scrap.get_full_stat()
        return Response(content, status=status.HTTP_200_OK)


class CoronaStatOfDistrict(APIView):
    def get(self, request, format=None):
        print('request come')
        try:
            pdf_url = "https://www.iedcr.gov.bd/website/images/files/nCoV/Case_dist_10_May_upload.pdf"
            affected_number = {}
            pdf_read(pdf_url)
            return Response(affected_number, status=status.HTTP_200_OK)
        except:
            print("error")
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

