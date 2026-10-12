import sys
import unittest
from pathlib import Path
from unittest import mock

import requests
from requests.adapters import BaseAdapter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import ollama_client


class RedirectTrap(BaseAdapter):
    def __init__(self, code):
        self.code = code
        self.sent = []

    def send(self, request, **kwargs):
        self.sent.append(request)
        response = requests.Response()
        response.request = request
        response.url = request.url
        response.status_code = self.code if len(self.sent) == 1 else 200
        response._content = b'{"response": "synthetic reply"}'
        if len(self.sent) == 1:
            response.headers["Location"] = "https://outside.invalid/collect"
        return response

    def close(self):
        pass


class LocalTransportSecurityTests(unittest.TestCase):
    def test_redirects_never_forward_local_prompts(self):
        for code in (301, 302, 303, 307, 308):
            with self.subTest(code=code):
                session = requests.Session()
                session.trust_env = False
                trap = RedirectTrap(code)
                session.mount("http://", trap)
                session.mount("https://", trap)
                with mock.patch.object(ollama_client, "_SESSION", session):
                    try:
                        ollama_client.generate_with_ollama("fixture", "SYNTHETIC-PRIVATE-PROMPT")
                    except (RuntimeError, requests.RequestException):
                        pass
                self.assertEqual(len(trap.sent), 1, "Local data crossed a redirect boundary")
                session.close()

    def test_redirect_response_is_not_accepted_as_model_output(self):
        session = requests.Session()
        trap = RedirectTrap(307)
        session.mount("http://", trap)
        session.mount("https://", trap)
        with mock.patch.object(ollama_client, "_SESSION", session):
            with self.assertRaises((RuntimeError, requests.RequestException)):
                ollama_client.generate_with_ollama("fixture", "synthetic")
        session.close()

    def test_direct_local_response_still_works(self):
        session = requests.Session()
        trap = RedirectTrap(200)
        session.mount("http://", trap)
        with mock.patch.object(ollama_client, "_SESSION", session):
            self.assertEqual(ollama_client.generate_with_ollama("fixture", "synthetic"), "synthetic reply")
        self.assertEqual(len(trap.sent), 1)
        session.close()
