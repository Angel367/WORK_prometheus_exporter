import re
import subprocess


def get_docker_logs(container_id, since_time):
    # Формируем команду
    command = f"docker logs {container_id} --since {since_time}"

    try:
        # Выполняем команду и получаем вывод
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Проверяем, была ли успешно выполнена команда
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error executing command: {result.stderr}"

    except Exception as e:
        return f"Exception: {str(e)}"


if __name__ == "__main__":
    status_pattern = re.compile(r'\s(\d{3})\s')
    response_codes_count = {}
    container_id = "ad21902b9c080bd4fdd924f63430308b19a1a6b78f9ec8c1d354fb2f9ae5d09b"
    since_time = "10m"
    logs = get_docker_logs(container_id, since_time)
    logs = """
158.160.129.126 - - [23/Dec/2023:12:02:05 +0000] "GET / HTTP/1.1" 200 28696 "-" "python-requests/2.31.0"
158.160.129.126 - - [23/Dec/2023:12:02:05 +0000] "GET /api/okpd/ HTTP/1.1" 200 879 "-" "python-requests/2.31.0"
158.160.129.126 - - [23/Dec/2023:12:02:05 +0000] "GET / HTTP/1.1" 200 28696 "-" "python-requests/2.31.0"
158.160.129.126 - - [23/Dec/2023:12:02:05 +0000] "GET /api/okpd/ HTTP/1.1" 200 879 "-" "python-requests/2.31.0"
194.87.35.109 - - [23/Dec/2023:12:02:06 +0000] "GET / HTTP/1.1" 200 28696 "-" "python-requests/2.31.0"
158.160.129.126 - - [23/Dec/2023:12:02:10 +0000] "GET / HTTP/1.1" 200 28696 "-" "python-requests/2.31.0"
158.160.129.126 - - [23/Dec/2023:12:02:10 +0000] "GET /api/okpd/ HTTP/1.1" 200 879 "-" "python-requests/2.31.0"
158.160.129.126 - - [23/Dec/2023:12:02:10 +0000] "GET / HTTP/1.1" 200 28696 "-" "python-requests/2.31.0"
158.160.129.126 - - [23/Dec/2023:12:02:10 +0000] "GET /api/okpd/ HTTP/1.1" 200 879 "-" "python-requests/2.31.0"
    """
    for log_entry in logs.split('\n'):
        match = status_pattern.search(log_entry)
        if match:
            status = match.group(1)
            response_codes_count[status] = response_codes_count.get(status, 0) + 1

    # Выводим результаты
    for code, count in response_codes_count.items():
        print(f"HTTP Status {code}: {count} entries")
