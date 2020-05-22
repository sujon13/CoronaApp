from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from .web_scraping import WebScrap, get_full_stat


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
    def get(self, request, day, format=None):
        url = 'https://www.worldometers.info/coronavirus/'

        try:
            web_scrap = WebScrap(url)
            res = web_scrap.simple_get()
        except Exception as e:
            print('exception is: ' + str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            content = get_full_stat(res, day)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(content, status=status.HTTP_200_OK)



