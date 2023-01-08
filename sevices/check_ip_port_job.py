import socket
import threading
import time
import scanner
from http.client import UnknownProtocol, BadStatusLine

checks = []


def handle(item):
    # clear every operation
    checks.clear()

    process(item)
    # send success jobs to server
    data = {item["id"]: checks}
    print(data)
    scanner.success_job(data)


def process(item):
    data = item['payload']['data']

    timeout = data['timeout']

    for port in data['ports']:

        for ip in data['ips']:
            thread = threading.Thread(target=scan_port, args=(ip, port, timeout))
            time.sleep(0.01)
            thread.start()

        thread.join(timeout + 0.4)


def scan_port(ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        s.connect((ip, port))
        s.settimeout(timeout)
        request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % ip
        s.send(request.encode())
        response = s.recv(4096)
        version, status, reason = response_disassemble(response.decode())
        checks.append({"ip": ip, 'port': port, 'status': status, 'data': response.decode()})
        s.close()
    except UnknownProtocol or BadStatusLine:
        try:
            response = response.decode()
            s.close()
        except:
            response = 'undefined protocol'
            s.close()

        checks.append({"ip": ip, 'port': port, 'status': 0, 'data': response})
        s.close()
    except:
        s.close()


# https://github.com/python/cpython/blob/8d4c52ffb47a4d3590758220f297ba58108e1ef3/Lib/http/client.py#L266
def response_disassemble(response):
    try:
        version, status, reason = response.split(None, 2)
    except ValueError:
        try:
            version, status = response.split(None, 1)
            reason = ""
        except ValueError:
            version = ""

    if not version.startswith("HTTP/"):
        raise UnknownProtocol(response)

    try:
        status = int(status)
        if status < 100 or status > 999:
            raise BadStatusLine(response)
    except ValueError:
        raise BadStatusLine(response)

    return version, status, reason
