import unittest
from server.server import *
from unittest.mock import patch, Mock, MagicMock


class TestPreProcessingHandler(unittest.TestCase):
    @patch("os.getenv")
    @patch('server.server.handle_relation_post_request', return_value=Mock())  
    @patch.object(PreProcessingHandler, 'wrongly_formatted_request_response')
    @patch.object(PreProcessingHandler, 'handled_request_body', return_value=True)
    @patch.object(PreProcessingHandler, '__init__', return_value=None)
    def test_do_post_tripleconstruction_valid(self, mock_init, mock_handled_body, mock_wrong_resp, mock_handle_relation, mock_os):
        mock_init.return_value = None
        mock_os.return_value="env_var"
        handler = PreProcessingHandler()
        handler.rfile = MagicMock()
        handler.wfile = MagicMock()
        handler.headers = {'Content-Length': '0', "Access-Authorization": "env_var"}
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()

        # simulate a post request call to '/tripleconstruction'
        handler.path = '/tripleconstruction'
        handler.do_POST()
        self.assertTrue(mock_handled_body.called)
        mock_handle_relation.assert_called_once()
        handler.send_response.assert_called_once_with(200)
        handler.send_header.assert_called_once_with('Content-type', 'text/html')
        handler.end_headers.assert_called_once()


    @patch("os.getenv")
    @patch('server.server.handle_relation_post_request', return_value=Mock())  
    @patch.object(PreProcessingHandler, 'wrongly_formatted_request_response')
    @patch.object(PreProcessingHandler, 'handled_request_body', return_value=True)
    @patch.object(PreProcessingHandler, '__init__', return_value=None)
    def test_do_post_invalid_endpoint(self, mock_init, mock_handled_body, mock_wrong_resp, mock_handle_relation, mock_os):
        mock_init.return_value = None
        mock_os.return_value="env_var"
        handler = PreProcessingHandler()
        handler.rfile = MagicMock()
        handler.wfile = MagicMock()
        handler.headers = {'Content-Length': '0', "Access-Authorization": "env_var"}
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()

        # simulate a post request call to an invalid endpoint
        handler.path = '/invalid-endpoint'
        handler.send_response.reset_mock()
        handler.send_header.reset_mock()
        handler.end_headers.reset_mock()
        handler.do_POST()
        handler.send_response.assert_called_once_with(404)
        handler.send_header.assert_called_once_with('Content-type','text/html')
        handler.end_headers.assert_called_once()

    @patch("os.getenv")
    @patch('server.server.handle_relation_post_request', return_value=Mock())  
    @patch.object(PreProcessingHandler, 'wrongly_formatted_request_response')
    @patch.object(PreProcessingHandler, 'handled_request_body', return_value=True)
    @patch.object(PreProcessingHandler, '__init__', return_value=None)
    def test_do_post_wrongly_formatted_request(self, mock_init, mock_handled_body, mock_wrong_resp, mock_handle_relation, mock_os):
        mock_init.return_value = None
        mock_os.return_value="env_var"
        handler = PreProcessingHandler()
        handler.rfile = MagicMock()
        handler.wfile = MagicMock()
        handler.headers = {'Content-Length': '0', "Access-Authorization": "env_var"}
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        mock_handle_relation.side_effect = Exception("test exception")

        # simulate a post request call to an invalid endpoint
        handler.path = '/tripleconstruction'
        handler.do_POST()
        mock_wrong_resp.assert_called_once_with("test exception")
        
    @patch.object(PreProcessingHandler, '__init__', return_value=None)
    def test_wrongly_formatted_request_response(self, mock_init):
        mock_init.return_value = None
        handler = PreProcessingHandler()
        handler.rfile = MagicMock()
        handler.wfile = MagicMock()
        handler.wfile.write = MagicMock()
        handler.headers = {'Content-Length': '0'}
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()

        handler.wrongly_formatted_request_response("test message")
        handler.send_response.assert_called_once_with(422)
        handler.send_header.assert_called_once_with('Content-type','text/html')
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once()

    @patch("os.getenv")
    @patch('server.server.handle_relation_post_request', return_value=Mock())  
    @patch.object(PreProcessingHandler, 'wrongly_formatted_request_response')
    @patch.object(PreProcessingHandler, 'handled_request_body', return_value=True)
    @patch.object(PreProcessingHandler, '__init__', return_value=None)
    def test_do_post_unauthrorized(self, mock_init, mock_handled_body, mock_wrong_resp, mock_handle_relation, mock_os):
        mock_init.return_value = None
        mock_os.return_value="env_var"
        handler = PreProcessingHandler()
        handler.rfile = MagicMock()
        handler.wfile = MagicMock()
        handler.headers = {'Content-Length': '0', "Access-Authorization": "invalid_var"}
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        mock_handle_relation.side_effect = Exception("test exception")

        # simulate a post request call to an invalid endpoint
        handler.path = '/tripleconstruction'
        handler.do_POST()
        mock_wrong_resp.assert_not_called()
        handler.send_response.assert_called_once_with(401)
        handler.send_header.assert_called_once_with('Content-type','text/html')
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once()



    @patch('server.server.PreProcessingHandler.wrongly_formatted_request_response')
    @patch.object(PreProcessingHandler, '__init__', return_value=None)
    def test_handled_request_body_exception(self, mock_init, mock_wrongly_formatted_request_response):
        mock_init.return_value = None
        pph = PreProcessingHandler()

        encoded_content = "Wrongly_formatted_data".encode()
        post_content = {"post_data": encoded_content, "post_json": {}}
        result = pph.handled_request_body(post_content)

        self.assertFalse(result)
        mock_wrongly_formatted_request_response.assert_called_once() 


    @patch('server.server.PreProcessingHandler.wrongly_formatted_request_response')
    @patch.object(PreProcessingHandler, '__init__', return_value=None)
    def test_handled_request_returns_true(self, mock_init, mock_wrongly_formatted_request_response):
        mock_init.return_value = None
        pph = PreProcessingHandler()

        encoded_content = json.dumps({"test": "correct data"}).encode()
        post_content = {"post_data": encoded_content, "post_json": {}}
        result = pph.handled_request_body(post_content)

        self.assertTrue(result)
        mock_wrongly_formatted_request_response.assert_not_called() 

if __name__ == '__main__':
    unittest.main()