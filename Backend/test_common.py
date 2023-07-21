import unittest
from unittest import mock
from unittest.mock import Mock

from Backend import common

URL = 'https://api.lmiforall.org.uk/api/v1/soc/search?q=plumber'


class MyTestCase(unittest.TestCase):
    @mock.patch('requests.get')
    def test_api_call(self, mocked_request):
        expected_data = {"test": "job"}
        mocked_request.return_value = Mock(status_code=200, text='{"test":"job"}')

        actual_data = common.api_call(URL)

        self.assertEqual(actual_data, expected_data)
        mocked_request.assert_called_with(URL, verify=False)

    @mock.patch('requests.get')
    def test_too_many_calls_from_API(self, mocked_request):
        expected_data = 'too many calls'
        mocked_request.return_value = Mock(status_code=503)

        actual_data = common.api_call(URL)

        self.assertEqual(actual_data, expected_data)
        mocked_request.assert_called_with(URL, verify=False)

    @mock.patch('requests.get')
    def test_no_response_from_API(self, mocked_request):
        expected_data = 'not found'
        mocked_request.return_value = Mock(status_code=400)

        actual_data = common.api_call(URL)

        self.assertEqual(actual_data, expected_data)
        mocked_request.assert_called_with(URL, verify=False)

    @mock.patch('requests.get')
    def test_no_response_from_API(self, mocked_request):
        expected_data = 'not found'
        mocked_request.return_value = Mock(status_code=400)

        actual_data = common.api_call(URL)

        self.assertEqual(actual_data, expected_data)
        mocked_request.assert_called_with(URL, verify=False)

    @mock.patch('requests.get')
    def test_other_error_API(self, mocked_request):
        expected_data = 'There seems to be a issue getting your job recommendations back to you, please try again later'
        mocked_request.return_value = Mock(status_code=404)

        with self.assertRaises(Exception) as context:
            common.api_call(URL)

        self.assertEqual(str(context.exception), expected_data)
        mocked_request.assert_called_with(URL, verify=False)

    def test_key(self):
        e = {'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}
        expected_data = 4.0
        actual_data = common.key(e)
        self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
