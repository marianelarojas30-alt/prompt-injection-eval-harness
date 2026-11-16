import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import ollama_client


class OllamaResponseTests(unittest.TestCase):
    def generate(self, body):
        reply = requests.Response()
        reply.status_code = 200
        reply._content = body
        with patch.object(ollama_client._SESSION, "post", return_value=reply):
            return ollama_client.generate_with_ollama("fixture", "synthetic")

    def test_invalid_json_is_a_server_error(self):
        with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
            self.generate(b"")

    def test_missing_or_non_text_response_is_a_server_error(self):
        for body in (b"[]", b"{}", b'{"response":null}', b'{"response":42}'):
            with self.subTest(body=body), self.assertRaisesRegex(RuntimeError, "text response field"):
                self.generate(body)

    def test_genuine_empty_answer_is_returned_for_scoring(self):
        self.assertEqual(self.generate(b'{"response":""}'), "")
