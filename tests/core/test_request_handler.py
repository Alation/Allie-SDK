import unittest

import requests
import requests_mock
from requests import HTTPError

from allie_sdk.core.request_handler import RequestHandler

class TestRequestHandler(unittest.TestCase):

    def setUp(self):
        self.session = requests.Session()
        self.host = 'https://test.alation.com'
        self.access_token = 'test_token'
        self.handler = RequestHandler(self.session, self.host, self.access_token)

    @requests_mock.Mocker()
    def test_delete(self, m):
        m.delete('https://test.alation.com/test/delete', json={'message': 'Deleted successfully'}, status_code=204)
        result = self.handler.delete('/test/delete')
        self.assertEqual(result, {'msg': '',
         'result': {'message': 'Deleted successfully'},
         'status': 'successful'})
        self.assertEqual(m.last_request.headers['Token'], 'test_token')

    @requests_mock.Mocker()
    def test_delete_error(self, m):
        m.delete('https://test.alation.com/test/delete', json={'error': 'Not found'}, status_code=404)
        with self.assertRaises(HTTPError) as context:
            self.handler.delete('/test/delete')
        self.assertEqual(context.exception.response.status_code, 404)

    @requests_mock.Mocker()
    def test_get(self, m):
        m.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test'}])
        result = self.handler.get('/test/get')
        self.assertEqual(result, [{'id': 1, 'name': 'Test'}])
        self.assertEqual(m.last_request.headers['Token'], 'test_token')

    @requests_mock.Mocker()
    def test_get_empty_response(self, m):
        m.get('https://test.alation.com/test/get', json=[])
        result = self.handler.get('/test/get')
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_get_error(self, m):
        m.get('https://test.alation.com/test/get', json={'error': 'Unauthorized'}, status_code=401)
        with self.assertRaises(HTTPError) as context:
            self.handler.get('/test/get')
        self.assertEqual(context.exception.response.status_code, 401)

    @requests_mock.Mocker()
    def test_get_with_pagination(self, m):
        m.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test 1'}],
              headers={'X-Next-Page': '/test/get?page=2'})
        m.get('https://test.alation.com/test/get?page=2', json=[{'id': 2, 'name': 'Test 2'}])
        result = self.handler.get('/test/get')
        self.assertEqual(result, [{'id': 1, 'name': 'Test 1'}, {'id': 2, 'name': 'Test 2'}])
        self.assertEqual(m.call_count, 2)

    @requests_mock.Mocker()
    def test_get_with_pagination_error(self, m):
        m.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test 1'}],
              headers={'X-Next-Page': '/test/get?page=2'})
        m.get('https://test.alation.com/test/get?page=2', json={'error': 'Server error'}, status_code=500)

        with self.assertRaises(HTTPError) as context:
            self.handler.get('/test/get')
        self.assertEqual(context.exception.response.status_code, 500)

    @requests_mock.Mocker()
    def test_patch(self, m):
        m.patch('https://test.alation.com/test/patch', json={'id': 1, 'name': 'Updated Test'})
        result = self.handler.patch('/test/patch', {'name': 'Updated Test'})
        self.assertEqual(result, {'id': 1, 'name': 'Updated Test'})
        self.assertEqual(m.last_request.headers['Token'], 'test_token')

    @requests_mock.Mocker()
    def test_patch_error(self, m):
        m.patch('https://test.alation.com/test/patch', json={'error': 'Bad request'}, status_code=400)
        with self.assertRaises(HTTPError) as context:
            self.handler.patch('/test/patch', {'name': 'Updated Test'})
        self.assertEqual(context.exception.response.status_code, 400)

    @requests_mock.Mocker()
    def test_post(self, m):
        m.post('https://test.alation.com/test/post', json={'id': 2, 'name': 'New Test'})
        result = self.handler.post('/test/post', {'name': 'New Test'})
        self.assertEqual(result, {'id': 2, 'name': 'New Test'})
        self.assertEqual(m.last_request.headers['Token'], 'test_token')

    @requests_mock.Mocker()
    def test_post_error(self, m):
        m.post('https://test.alation.com/test/post', json={'error': 'Server error'}, status_code=500)
        with self.assertRaises(HTTPError) as context:
            self.handler.post('/test/post', {'name': 'New Test'})
        self.assertEqual(context.exception.response.status_code, 500)

    @requests_mock.Mocker()
    def test_put(self, m):
        m.put('https://test.alation.com/test/put', json={'id': 3, 'name': 'Put Test'})
        result = self.handler.put('/test/put', {'name': 'Put Test'})
        self.assertEqual(result, {'id': 3, 'name': 'Put Test'})
        self.assertEqual(m.last_request.headers['Token'], 'test_token')

    @requests_mock.Mocker()
    def test_put_error(self, m):
        m.put('https://test.alation.com/test/put', json={'error': 'Not found'}, status_code=404)
        with self.assertRaises(HTTPError) as context:
            self.handler.put('/test/put', {'name': 'Put Test'})
        self.assertEqual(context.exception.response.status_code, 404)

if __name__ == '__main__':
    unittest.main()