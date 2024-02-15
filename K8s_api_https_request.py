import json
import traceback
import requests
import urllib3
from datetime import datetime
import time
from requests.models import Response
from datetime import timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
######################################
sleep_time = 1
ymd = datetime.now().strftime("%Y%m%d-%H%M%S")
log_file = "./" + ymd + "_K8s-api-http-request.log"
errlog_file = "./" + ymd + "_K8s-api-http-request-error.log"
######################################


def out_log(status, txt, response_time):
    level = "INFO" if status < 400 else "WARN"
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d %H:%M:%S\t[{}]\t".format(level))
    log_content = dt + str(status) + "\tresponse time:\t" + str(response_time) + " ms\t" + str(txt)
    print(log_content)
    with open(log_file, "a") as f:
        f.write(log_content + "\n")
    if level == "WARN" or response_time > 100:
        with open(errlog_file, "a") as f:
            f.write(log_content + "\n")

def get_mock_response(status_code, content, elapsed):
    res = Response()
    res.status_code = status_code
    res._content = content
    res.elapsed = elapsed
    return res

def send_request():
    api_server_url = "  "
    auth_token = "  "
    headers = {'Authorization': 'Bearer {}'.format(auth_token)}
    try:
        res = requests.get(api_server_url,headers=headers,verify=False,timeout=None)
    except Exception:
        traceback_log = traceback.format_exc()
        content = json.dumps(
            {"metadata": {"name": str(traceback_log)}}
        ).encode('utf-8')
        res = get_mock_response(
            status_code=1000,
            content=content,
            elapsed=timedelta(0)
        )
    return res

def run():
    while True:
        res = send_request()
        out_log(
            status=res.status_code,
            txt=res.json().get('metadata').get('name'),
            response_time=round(res.elapsed.total_seconds()*1000, 2)
        )
        time.sleep(sleep_time)


if __name__ == "__main__":
    run()
