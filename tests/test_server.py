import json
import sys
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server

class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        server.DB = Path(cls.temp.name) / 'data' / 'stories.sqlite3'
        cls.http = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.base = f'http://127.0.0.1:{cls.http.server_port}'
        threading.Thread(target=cls.http.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.temp.cleanup()

    def call(self, path, data=None, method=None):
        req = urllib.request.Request(self.base + path, data=json.dumps(data).encode() if data is not None else None, method=method, headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.status, json.load(response)

    def test_offline_status(self):
        with patch.object(server, 'ollama', side_effect=OSError):
            _, result = self.call('/api/status')
        self.assertFalse(result['ready'])

    def test_generate_save_read_delete(self):
        with patch.object(server, 'ollama', return_value={'response':json.dumps({'title':'A little light', 'body':'The kettle cooled.\n\nThe cottage rested.'})}) as model:
            code, story = self.call('/api/generate', {'setting':'A woodland cottage','mood':'Cozy','minutes':3,'detail':'a cat'})
            self.assertEqual(code, 201)
            self.assertEqual(model.call_args.args[0], '/api/generate')
        _, library = self.call('/api/stories')
        self.assertTrue(any(s['id'] == story['id'] for s in library))
        _, result = self.call('/api/stories/' + story['id'], method='DELETE')
        self.assertTrue(result['deleted'])

    def test_invalid_input(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.call('/api/generate', {'setting':'unknown'})
        self.assertEqual(caught.exception.code, 400)

    def test_bad_model_response(self):
        with patch.object(server, 'ollama', return_value={'response':'not json'}):
            with self.assertRaises(urllib.error.HTTPError) as caught:
                self.call('/api/generate', {'setting':'A night train','mood':'Cozy','minutes':3})
        self.assertEqual(caught.exception.code, 502)

    def test_model_unreachable(self):
        with patch.object(server, 'ollama', side_effect=OSError):
            with self.assertRaises(urllib.error.HTTPError) as caught:
                self.call('/api/generate', {'setting':'A quiet bookshop','mood':'Dreamlike','minutes':5})
        self.assertEqual(caught.exception.code, 503)

if __name__ == '__main__':
    unittest.main()
