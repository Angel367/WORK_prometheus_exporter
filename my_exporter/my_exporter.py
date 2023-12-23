import time

import requests
from prometheus_client import start_http_server, Gauge

# Create a Gauge metric
frontend_http_status_code_metric = Gauge('frontend_http_status_code', 'HTTP status code from main web-page')
frontend_latency_metric = Gauge('frontend_latency', 'latency in ms for main webpage')

backend_http_status_code_metric = Gauge('backend_http_status_code', 'HTTP status code from one of endpoint')
backend_latency_metric = Gauge('backend_latency', 'latency in ms for one of endpoint')


def check_frontend_http_code(url='https://moy-zakupki.ru/'):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.exceptions.RequestException:
        return -1


def check_backend_http_code(url='https://moy-zakupki.ru/api/okpd/'):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.exceptions.RequestException:
        return -1


def check_frontend_latency(url='https://moy-zakupki.ru/'):
    try:
        response = requests.get(url)
        return response.elapsed.total_seconds()
    except requests.exceptions.RequestException:
        return 0


def check_backend_latency(url='https://moy-zakupki.ru/api/okpd/'):
    try:
        response = requests.get(url)
        return response.elapsed.total_seconds()
    except requests.exceptions.RequestException:
        return 0


def collect_metrics():
    frontend_http_status_code_metric.set(int(check_frontend_http_code()))
    backend_http_status_code_metric.set(int(check_backend_http_code()))

    frontend_latency_metric.set(int(check_frontend_latency() * 1000))
    backend_latency_metric.set(int(check_backend_latency() * 1000))


if __name__ == '__main__':
    start_http_server(9101)
    while True:
        collect_metrics()
        time.sleep(5)
