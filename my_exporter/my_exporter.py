import time

import requests
from prometheus_client import start_http_server, Gauge

# Create a Gauge metric
my_metric = Gauge('frontend_http_status_code', 'HTTP status code from main webpage')


def check_image_status(url='https://moy-zakupki.ru/'):
    try:
        response = requests.get(url)
        return response.status_code

    except requests.exceptions.RequestException as e:
        return -1


def collect_metrics():
    metric_value = check_image_status()
    my_metric.set(int(metric_value))


if __name__ == '__main__':
    # Start an HTTP server to expose metrics
    start_http_server(9101)

    # Periodically collect and update metrics
    while True:
        collect_metrics()
        time.sleep(5)  # Adjust the sleep interval as needed
