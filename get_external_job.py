import queue
import scanner
import threading
import sevices.check_ip_port_job

q = queue.Queue()


def handle():
    q_size = q.qsize()
    if q_size > 50:
        return

    data = scanner.get_jobs()
    if 'data' not in data.keys():
        return

    collect = data['data']

    for item in collect:
        q.put(item)


def worker():
    while True:
        item = q.get()

        sevices.check_ip_port_job.handle(item)

        q.task_done()


threading.Thread(target=worker, daemon=True).start()
