import os
import time
from prometheus_client import start_http_server, Summary, Gauge, Counter
from dotenv import load_dotenv
import requests


load_dotenv()


EXPORTER_PORT = os.getenv("EXPORTER_PORT")
PING_SECRET = os.getenv("PING_SECRET")
ENDPOINT = os.getenv("ENDPOINT")

request_time = Summary(
    "request_processing_seconds", "Time spent processing ping request"
)

default_socle_competency = Gauge(
    "default_socle_competency", "Number of competencies in default socle"
)
default_socle_competency_subject = Gauge(
    "default_socle_competency_subject",
    "Number of competency-subject links in default socle",
)
default_socle_competency_template = Gauge(
    "default_socle_competency_template", "Number of templates in default socle"
)
default_socle_container = Gauge(
    "default_socle_container", "Number of containers in default socle"
)
default_socle_subject = Gauge(
    "default_socle_subject", "Number of subjects in default socle"
)
eval_comment = Gauge("eval_comment", "Number of comments")
eval_evaluation = Gauge("eval_evaluation", "Number of evaluations")
eval_observation = Gauge("eval_observation", "Number of observations")
eval_period = Gauge("eval_period", "Number of periods")
group = Gauge("group", "Number of groups")
report = Gauge("report", "Number of reports")
socle_competency = Gauge("socle_competency", "Number of competencies in socle")
socle_competency_subject = Gauge(
    "socle_competency_subject", "Number of competency-subject links in socle"
)
socle_competency_template = Gauge(
    "socle_competency_template", "Number of templates in socle"
)
socle_container = Gauge("socle_container", "Number of containers in socle")
socle_subject = Gauge("socle_subject", "Number of subjects in socle")
student = Gauge("student", "Number of students")
user = Gauge("user", "Number of users")

failure = Counter("ping_failure", "number of failure of the ping request")

# Decorate function with metric.
@request_time.time()
def do_ping():
    r = requests.post(ENDPOINT, json={"secret": PING_SECRET})
    data = r.json()
    ping = data["ping"]
    default_socle_competency.set(ping["default_socle_competency"])
    default_socle_competency_subject.set(ping["default_socle_competency_subject"])
    default_socle_competency_template.set(ping["default_socle_competency_template"])
    default_socle_container.set(ping["default_socle_container"])
    default_socle_subject.set(ping["default_socle_subject"])
    eval_comment.set(ping["eval_comment"])
    eval_evaluation.set(ping["eval_evaluation"])
    eval_observation.set(ping["eval_observation"])
    eval_period.set(ping["eval_period"])
    group.set(ping["group"])
    report.set(ping["report"])
    socle_competency.set(ping["socle_competency"])
    socle_competency_subject.set(ping["socle_competency_subject"])
    socle_competency_template.set(ping["socle_competency_template"])
    socle_container.set(ping["socle_container"])
    socle_subject.set(ping["socle_subject"])
    student.set(ping["student"])
    user.set(ping["user"])


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(int(EXPORTER_PORT))
    # Generate some ping requests.
    while True:
        try:
            do_ping()
        except Exception as e:
            print(e)
            failure.inc()
        # Every 15 seconds
        time.sleep(15)