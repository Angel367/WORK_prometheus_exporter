import subprocess
import time, re

from prometheus_client import start_http_server, Counter

http_status_counter = Counter('http_codes_status_counter', 'Amount of each http code status from server', ['status'])


def get_docker_container_id_by_name(name="mz_nginx"):
    command = f"docker ps -q --filter ancestor={name}"
    try:
        container_id = subprocess.run(command, shell=True, capture_output=True, text=True)
        if container_id.returncode == 0:
            return container_id.stdout[:-1]
        else:
            return f"Error executing command: {container_id.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"


def get_docker_logs(container_id, since_time):
    command = f"docker logs {container_id} --since {since_time}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error executing command: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"


def parse_docker_logs(logs):
    status_pattern = re.compile(r'\s(\d{3})\s')
    response_codes_count = {
                            '200': 0, '201': 0, '202': 0, '203': 0, '204': 0, '205': 0, '206': 0, '207': 0, '208': 0,
                            '300': 0, '301': 0, '302': 0, '303': 0, '304': 0, '305': 0, '306': 0, '307': 0, '308': 0,
                            '400': 0, '401': 0, '402': 0, '403': 0, '404': 0, '405': 0, '408': 0, '409': 0,
                            '500': 0, '501': 0, '502': 0, '503': 0, '504': 0, '521': 0, '522': 0, '523': 0, '524': 0
                            }
    for log_entry in logs.split('\n'):
        match = status_pattern.search(log_entry)
        if match:
            status = match.group(1)
            response_codes_count[status] = response_codes_count.get(status, 0) + 1
    return response_codes_count


def collect_metrics(response_codes_count):
    for status_code, value in response_codes_count.items():
        http_status_counter.labels(status_code).inc(value)


if __name__ == '__main__':
    start_http_server(9101)
    while True:
        container_id = get_docker_container_id_by_name()
        logs = get_docker_logs(get_docker_container_id_by_name(), "5s")
        parsed_logs = parse_docker_logs(logs)
        collect_metrics(parsed_logs)
        time.sleep(5)
