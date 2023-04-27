import os
import sys

import zulip


class Zulip:
    def __init__(self, api_key=os.environ['ZULIP_API_KEY'], email=os.environ['ZULIP_EMAIL'], site=os.environ['ZULIP_SITE']):
        self.api_key = api_key
        self.email = email
        self.site = site
        self.client = zulip.Client(api_key=self.api_key, email=self.email, site=self.site)

    def send_msg(self, msg1, zulip_stream=os.environ['ZULIP_STREAM'], zulip_topic=os.environ['ZULIP_TOPIC']):
        request = {
            "type": "stream",
            "to": zulip_stream,
            "topic": zulip_topic,
            "content": msg1
        }
        res = self.client.send_message(request)
        print (res)


if __name__ == '__main__':
    zulip_obj = Zulip()
    #zulip_obj.send_msg(sys.argv[1], sys.argv[2])
    #zulip_obj.send_msg("TEST")
