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
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    
    def test_delete_error(self, requests_mock):
        requests_mock.delete('https://test.alation.com/test/delete', json={'error': 'Not found'}, status_code=404)
        with pytest.raises(HTTPError) as context:
            self.handler.delete('/test/delete')
        assert context.value.response.status_code == 404

    
    def test_get(self, requests_mock):
        requests_mock.get('https://test.alation.com/test/get', json=[{'id': 1, 'name': 'Test'}])
        result = self.handler.get('/test/get')
        assert result == [{'id': 1, 'name': 'Test'}]
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    
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

    def test_get_nested_results(self, requests_mock):
        requests_mock.get(
            'https://test.alation.com/test/nested-get',
            json={
                'count': 2,
                'next': '/test/nested-get?limit=1&offset=1',
                'previous': None,
                'results': [{'id': 1, 'name': 'Test 1'}],
            },
        )
        requests_mock.get(
            'https://test.alation.com/test/nested-get?limit=1&offset=1',
            json={
                'count': 2,
                'next': None,
                'previous': '/test/nested-get?limit=1&offset=0',
                'results': [{'id': 2, 'name': 'Test 2'}],
            },
        )

        result = self.handler.get_nested_results('/test/nested-get')

        assert result == [{'id': 1, 'name': 'Test 1'}, {'id': 2, 'name': 'Test 2'}]
        assert requests_mock.call_count == 2

    def test_get_nested_results_error(self, requests_mock):
        requests_mock.get(
            'https://test.alation.com/test/nested-get',
            json={
                'count': 2,
                'next': '/test/nested-get?limit=1&offset=1',
                'previous': None,
                'results': [{'id': 1, 'name': 'Test 1'}],
            },
        )
        requests_mock.get(
            'https://test.alation.com/test/nested-get?limit=1&offset=1',
            json={'error': 'Server error'},
            status_code=500,
        )

        with pytest.raises(HTTPError) as context:
            self.handler.get_nested_results('/test/nested-get')

        assert context.value.response.status_code == 500

    
    def test_patch(self, requests_mock):
        requests_mock.patch('https://test.alation.com/test/patch', json={'id': 1, 'name': 'Updated Test'})
        result = self.handler.patch('/test/patch', {'name': 'Updated Test'})
        assert result == {'id': 1, 'name': 'Updated Test'}
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    
    def test_patch_error(self, requests_mock):
        requests_mock.patch('https://test.alation.com/test/patch', json={'error': 'Bad request'}, status_code=400)
        with pytest.raises(HTTPError) as context:
            self.handler.patch('/test/patch', {'name': 'Updated Test'})
        assert context.value.response.status_code == 400

    
    def test_post(self, requests_mock):
        requests_mock.post('https://test.alation.com/test/post', json={'id': 2, 'name': 'New Test'})
        result = self.handler.post('/test/post', {'name': 'New Test'})
        assert result == {'id': 2, 'name': 'New Test'}
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    def test_post_paginated(self, requests_mock):
        requests_mock.post(
            'https://test.alation.com/test/post',
            json=[{'id': 1, 'name': 'Test 1'}],
            headers={'X-Next-Page': '/test/post?skip=1&limit=1'},
        )
        requests_mock.post(
            'https://test.alation.com/test/post?skip=1&limit=1',
            json=[{'id': 2, 'name': 'Test 2'}],
        )

        result = self.handler.post_paginated('/test/post', {'name': 'New Test'})

        assert result == [{'id': 1, 'name': 'Test 1'}, {'id': 2, 'name': 'Test 2'}]
        assert requests_mock.call_count == 2
        assert requests_mock.request_history[0].json() == {'name': 'New Test'}
        assert requests_mock.request_history[1].json() == {'name': 'New Test'}

    def test_post_paginated_error(self, requests_mock):
        requests_mock.post(
            'https://test.alation.com/test/post',
            json=[{'id': 1, 'name': 'Test 1'}],
            headers={'X-Next-Page': '/test/post?skip=1&limit=1'},
        )
        requests_mock.post(
            'https://test.alation.com/test/post?skip=1&limit=1',
            json={'error': 'Server error'},
            status_code=500,
        )

        with pytest.raises(HTTPError) as context:
            self.handler.post_paginated('/test/post', {'name': 'New Test'})

        assert context.value.response.status_code == 500

    
    def test_post_error(self, requests_mock):
        requests_mock.post('https://test.alation.com/test/post', json={'error': 'Server error'}, status_code=500)
        with pytest.raises(HTTPError) as context:
            self.handler.post('/test/post', {'name': 'New Test'})
        assert context.value.response.status_code == 500

    
    def test_put(self, requests_mock):
        requests_mock.put('https://test.alation.com/test/put', json={'id': 3, 'name': 'Put Test'})
        result = self.handler.put('/test/put', {'name': 'Put Test'})
        assert result == {'id': 3, 'name': 'Put Test'}
        assert requests_mock.last_request.headers['Authorization'] == 'Bearer test_token'

    
    def test_put_error(self, requests_mock):
        requests_mock.put('https://test.alation.com/test/put', json={'error': 'Not found'}, status_code=404)
        with pytest.raises(HTTPError) as context:
            self.handler.put('/test/put', {'name': 'Put Test'})
        assert context.value.response.status_code == 404


class TestRequestSuccessMapping:
    @pytest.mark.parametrize("use_keyword_argument", [False, True], ids=["positional", "keyword"])
    @pytest.mark.parametrize(
        "response_data",
        [
            pytest.param({"id": 1}, id="dictionary"),
            pytest.param([{"id": 1}], id="list"),
            pytest.param("Completed", id="text"),
            pytest.param(None, id="none"),
            pytest.param({}, id="empty-dictionary"),
            pytest.param([], id="empty-list"),
            pytest.param("", id="empty-text"),
        ],
    )
    def test_response_remains_in_result(self, response_data: object, use_keyword_argument: bool) -> None:
        """Preserve response payloads and the default empty success message.

        Args:
            response_data (object): API response payload to preserve.
            use_keyword_argument (bool): Whether to pass the payload by name.

        Returns:
            None: Asserts the success mapping retains the existing contract.
        """
        if use_keyword_argument:
            result = RequestHandler._map_request_success_to_job_details(response_data=response_data)
        else:
            result = RequestHandler._map_request_success_to_job_details(response_data)

        assert result == {"status": "successful", "msg": "", "result": response_data}

    def test_success_without_response(self) -> None:
        """Support successful endpoints that return no response content.

        Args:
            None.

        Returns:
            None: Asserts an omitted payload maps to a successful empty result.
        """
        result = RequestHandler._map_request_success_to_job_details()

        assert result == {"status": "successful", "msg": "", "result": None}

    @pytest.mark.parametrize("message", ["Data product updated", None])
    def test_success_with_message_only(self, message: str | None) -> None:
        """Preserve explicit messages when no response payload is supplied.

        Args:
            message (str | None): Message supplied by the API, including None.

        Returns:
            None: Asserts message-only calls retain the supplied message.
        """
        result = RequestHandler._map_request_success_to_job_details(msg=message)

        assert result == {"status": "successful", "msg": message, "result": None}

    def test_success_with_response_and_message(self) -> None:
        """Keep the response payload and explicit success message separate.

        Args:
            None.

        Returns:
            None: Asserts a positional payload supports a keyword message.
        """
        response_data = {"product_id": "finance:sales"}

        result = RequestHandler._map_request_success_to_job_details(response_data, msg="Data product updated")

        assert result == {"status": "successful", "msg": "Data product updated", "result": response_data}
