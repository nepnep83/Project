import unittest
from unittest import mock
from unittest.mock import Mock

import common


class MyTestCase(unittest.TestCase):
    @mock.patch('requests.get')
    def test_no_response_from_API(self, mocked_request):
        expected_data = 'There seems to be a issue getting your job recommendations back to you, please try again later'
        mocked_request.return_value = Mock(status_code=400)

        with self.assertRaises(Exception) as context:
            common.api_call('https://api.lmiforall.org.uk/api/v1/soc/search?q=' + 'plumber')

        self.assertEqual(expected_data, str(context.exception))
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/search?q=plumber', verify=False)

    def test_key(self):
        e = {'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}
        expected_data = 4.0
        actual_data = common.key(e)
        self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
