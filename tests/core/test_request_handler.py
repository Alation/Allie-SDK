import pytest
import requests
from requests import HTTPError

from allie_sdk.core.request_handler import RequestHandler

class TestRequestHandler:

    def setup_method(self):
        self.session = requests.Session()
        self.host = 'https://test.alation.com'
        self.access_token = 'test_token'
        self.handler = RequestHandler(self.session, self.host, self.access_token)

    
    def test_delete(self, requests_mock):
        requests_mock.delete('https://test.alation.com/test/delete', json={'message': 'Deleted successfully'}, status_code=204)
        result = self.handler.delete('/test/delete')
        assert result == {'msg': '',
         'result': {'message': 'Deleted successfully'},
         'status': 'successful'}
        assert requests_mock.last_request.headers['Token'] == 'test_token'

    
    def test_delete_error(self, requests_mock):
        requests_mock.delete('https://test.alation.com/test/delete', json={'error': 'Not found'}, status_code=404)
        with pytest.raises(HTTPError) as context:
            self.handler.delete('/test/delete')
        assert context.value.response.status_code == 404

    
    def test_get(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test'}])
        result = self.handler.get('/test/get')
        assert result == [{'id': 1, 'name': 'Test'}]
        assert requests_mock.last_request.headers['Token'] == 'test_token'

    
    def test_get_empty_response(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[])
        result = self.handler.get('/test/get')
        assert result == []

    
    def test_get_error(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json={'error': 'Unauthorized'}, status_code=401)
        with pytest.raises(HTTPError) as context:
            self.handler.get('/test/get')
        assert context.value.response.status_code == 401

    
    def test_get_with_pagination(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test 1'}],
              headers={'X-Next-Page': '/test/get?page=2'})
        requests_mock.get('https://test.alation.com/test/get?page=2', json=[{'id': 2, 'name': 'Test 2'}])
        result = self.handler.get('/test/get')
        assert result == [{'id': 1, 'name': 'Test 1'}, {'id': 2, 'name': 'Test 2'}]
        assert requests_mock.call_count == 2

    
    def test_get_with_pagination_error(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test 1'}],
              headers={'X-Next-Page': '/test/get?page=2'})
        requests_mock.get('https://test.alation.com/test/get?page=2', json={'error': 'Server error'}, status_code=500)

        with pytest.raises(HTTPError) as context:
            self.handler.get('/test/get')
        assert context.value.response.status_code == 500

    
    def test_patch(self, requests_mock):
        requests_mock.patch('https://test.alation.com/test/patch', json={'id': 1, 'name': 'Updated Test'})
        result = self.handler.patch('/test/patch', {'name': 'Updated Test'})
        assert result == {'id': 1, 'name': 'Updated Test'}
        assert requests_mock.last_request.headers['Token'] == 'test_token'

    
    def test_patch_error(self, requests_mock):
        requests_mock.patch('https://test.alation.com/test/patch', json={'error': 'Bad request'}, status_code=400)
        with pytest.raises(HTTPError) as context:
            self.handler.patch('/test/patch', {'name': 'Updated Test'})
        assert context.value.response.status_code == 400

    
    def test_post(self, requests_mock):
        requests_mock.post('https://test.alation.com/test/post', json={'id': 2, 'name': 'New Test'})
        result = self.handler.post('/test/post', {'name': 'New Test'})
        assert result == {'id': 2, 'name': 'New Test'}
        assert requests_mock.last_request.headers['Token'] == 'test_token'

    
    def test_post_error(self, requests_mock):
        requests_mock.post('https://test.alation.com/test/post', json={'error': 'Server error'}, status_code=500)
        with pytest.raises(HTTPError) as context:
            self.handler.post('/test/post', {'name': 'New Test'})
        assert context.value.response.status_code == 500

    
    def test_put(self, requests_mock):
        requests_mock.put('https://test.alation.com/test/put', json={'id': 3, 'name': 'Put Test'})
        result = self.handler.put('/test/put', {'name': 'Put Test'})
        assert result == {'id': 3, 'name': 'Put Test'}
        assert requests_mock.last_request.headers['Token'] == 'test_token'

    
    def test_put_error(self, requests_mock):
        requests_mock.put('https://test.alation.com/test/put', json={'error': 'Not found'}, status_code=404)
        with pytest.raises(HTTPError) as context:
            self.handler.put('/test/put', {'name': 'Put Test'})
        assert context.value.response.status_code == 404