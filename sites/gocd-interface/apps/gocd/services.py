import requests
import json


class GOCDService(object):
    def test_connection(self, host, port, username, password):
        url = "http://%s:%s@%s:%s" % (
            username, password, host, port)
        response = requests.get(url)
        if response.status_code >= 200 and response.status_code < 400:
            return True, "OK"
        elif response.status_code == 401:
            return False, "Unauthorised"
        else:
            return False, "Down"

    def get_pipeline_groups(self, host, port, username, password):
        url = "http://%s:%s@%s:%s/go/api/config/pipeline_groups" % (
            username, password, host, port)

        response = requests.get(url)
        return json.loads(response.content)
