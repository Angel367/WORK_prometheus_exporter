import time

import requests
from prometheus_client import start_http_server, Gauge

# Create a Gauge metric
frontend_http_status_code_metric = Gauge('frontend_http_status_code', 'HTTP status code from main webpage')
backend_http_status_code_metric = Gauge('backend_http_status_code', 'HTTP status code from main webpage')


def check_frontend_status(url='https://moy-zakupki.ru/'):
    try:
        response = requests.get(url)
        return response.status_code

    except requests.exceptions.RequestException:
        return -1


def check_backend_status(url='https://moy-zakupki.ru/api/okpd/'):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.exceptions.RequestException:
        return -1


def collect_metrics():
    frontend_http_status_code_metric.set(int(check_frontend_status()))
    backend_http_status_code_metric.set(int(check_backend_status()))


if __name__ == '__main__':
    start_http_server(9102)
    while True:
        collect_metrics()
        time.sleep(5)
