import os
import time
import gzip
from datetime import datetime
from prometheus_client import start_http_server, Summary, Gauge, Counter
from dotenv import load_dotenv
import requests
from path import Path


load_dotenv()


EXPORTER_PORT = os.getenv("EXPORTER_PORT")
BACKUP_PATH = Path(os.getenv("BACKUP_PATH"))

process_time = Summary("processing_seconds", "Time spent processing backup")

backup_pg_dump_count = Gauge(
    "backup_pg_dump_count", "Number of pg dump in backup folder"
)
backup_pg_dump_size = Gauge(
    "backup_pg_dump_size", "Size of pg_dump folder in backup folder"
)
backup_last_pg_dump_size = Gauge("backup_last_pg_dump_size", "Size of the last pg_dump")
backup_last_pg_dump_lines = Gauge(
    "backup_last_pg_dump_lines", "Number of line of the last pg_dump"
)
backup_last_pg_dump_age = Gauge(
    "backup_last_pg_dump_age", "Age in days of the last pg_dump"
)

backup_reports_count = Gauge(
    "backup_reports_count", "Number of reports in backup folder"
)
backup_reports_size = Gauge("backup_reports_size", "Size of reports in backup folder")

failure = Counter("backup_failure", "number of failure of the backup processing")


@process_time.time()
def process_backup():
    pg_dump = BACKUP_PATH / "pg_dump"
    backup_pg_dump_count.set(len(pg_dump.glob("*.sql.gz")))
    backup_pg_dump_size.set(sum([f.getsize() for f in pg_dump.walkfiles()]))

    # Search for last backup
    l = pg_dump.glob("*.sql.gz")
    l.sort()
    last_backup = l[-1]

    backup_last_pg_dump_size.set(last_backup.getsize())

    # name is like dump_2021_05_29_14_03_20.sql.gz
    _, year, month, day, hour, minute, second = (
        last_backup.basename().split(".")[0].split("_")
    )
    last_backup_datetime = datetime(
        int(year), int(month), int(day), int(hour), int(minute), int(second)
    )
    t = datetime.now() - last_backup_datetime
    backup_last_pg_dump_age.set(t.total_seconds() / (60 * 60 * 24))

    with gzip.open(last_backup, "rb") as f:
        backup_last_pg_dump_lines.set(len(f.readlines()))

    reports = BACKUP_PATH / "reports"
    f_reports = [f for f in reports.walkfiles() if f.endswith("pdf")]
    backup_reports_count.set(len(f_reports))
    backup_reports_size.set(sum([f.getsize() for f in f_reports]))


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(int(EXPORTER_PORT))
    # Generate some ping requests.
    while True:
        try:
            process_backup()
        except Exception as e:
            print(e)
            failure.inc()
        # Every 60 seconds
        time.sleep(60)