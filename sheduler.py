from datetime import datetime
import schedule
import time
import get_external_job


def get_jobs():
    print(f"schedule I'm working... {datetime.today()}")
    get_external_job.handle()


schedule.every(1).to(1).minutes.do(get_jobs)

while True:
    schedule.run_pending()
    time.sleep(1)
