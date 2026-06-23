import io
import os
import unittest
from unittest import mock

import social_media_scheduler


class XquikBackendTest(unittest.TestCase):
    def test_twitter_backend_uses_existing_key_by_default(self):
        with mock.patch.dict(os.environ, {"TWITTER_API_KEY": "twitter-key"}, clear=True):
            self.assertEqual(social_media_scheduler.get_api_key("twitter"), "twitter-key")

    def test_xquik_backend_requires_account(self):
        env = {
            "TWITTER_BACKEND": "xquik",
            "XQUIK_API_KEY": "xquik-key",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            result = social_media_scheduler.simulate_post("twitter", "hello")

        self.assertEqual(result, "FAILURE: Missing XQUIK_ACCOUNT for Xquik Twitter/X posting.")

    def test_xquik_backend_accepts_pending_write_action(self):
        env = {
            "TWITTER_BACKEND": "xquik",
            "XQUIK_API_KEY": "xquik-key",
            "XQUIK_ACCOUNT": "@example",
        }
        response = FakeResponse(b'{"writeActionId":"wa_123"}', 202)

        with mock.patch.dict(os.environ, env, clear=True):
            with mock.patch.object(social_media_scheduler.request, "urlopen", return_value=response) as urlopen:
                result = social_media_scheduler.simulate_post("twitter", "hello from tests")

        self.assertEqual(
            result,
            "SUCCESS: Xquik accepted the tweet for posting. Write action ID: wa_123",
        )
        sent_request = urlopen.call_args.args[0]
        self.assertEqual(sent_request.headers["Authorization"], "Bearer xquik-key")
        self.assertEqual(sent_request.headers["Content-type"], "application/json")
        self.assertEqual(sent_request.data, b'{"account": "@example", "text": "hello from tests"}')


class FakeResponse:
    def __init__(self, body, status_code):
        self._body = io.BytesIO(body)
        self._status_code = status_code

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self._body.read()

    def getcode(self):
        return self._status_code


if __name__ == "__main__":
    unittest.main()
