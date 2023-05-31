import unittest
from unittest import mock
from unittest.mock import Mock

import requests

import main

_range = 2
skill_list = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}]
skill_id = ['2.A.1.a']


class MyTestCase(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['engineer', 'No'])
    def test_get_claimants_jobs(self, mock):
        expected_data = ['engineer']
        actual_data = main.get_claimants_jobs()
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_get_soc_code(self, mocked_request):
        job = "1"
        expected_data = 3113

        mocked_request.return_value = Mock(text='[{"soc":3113}]', status_code=200)
        actual_data = main.get_soc_code(job)
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/search?q=1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_soc_to_onet(self, mocked_request):
        soc = "1"
        expected_data = "53-6041.00"

        mocked_request.return_value = Mock(text='{"onetCodes":[{"code":"53-6041.00"}]}')
        actual_data = main.soc_to_onet(soc)
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/soc2onet/1', verify=False)
        self.assertEqual(expected_data, actual_data)

    def test_key(self):
        e = {'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}
        expected_data = 4.0
        actual_data = main.key(e)
        self.assertEqual(expected_data, actual_data)

    @mock.patch("main.skill_list", skill_list)
    @mock.patch('main.skill_id', skill_id)
    @mock.patch('main.skill_sort')
    @mock.patch('requests.get')
    @mock.patch('requests.models.Response.json')
    def test_onet_skills(self, mocked_json, mocked_request, mocked_sort):
        onet = '1'
        expected_data = ['2.A.1.a', '2.A.1.b']
        mocked_request.return_value = mocked_json
        mocked_json.json.return_value = {"scales": [{"id": "LV", "skills": [
            {"id": "2.A.1.a", "name": "Reading Comprehension", "value": 4.0},
            {"id": "2.A.1.b", "name": "Active Listening", "value": 3.62}]}]}
        mocked_sort.return_value = ['2.A.1.a', '2.A.1.b']
        actual_data = main.onet_skills(onet, _range)
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/skills/1', verify=False)
        mocked_sort.assert_called_with([{"id": "2.A.1.a", "name": "Reading Comprehension", "value": 4.0},
                                        {"id": "2.A.1.b", "name": "Active Listening", "value": 3.62}])
        self.assertEqual(expected_data, actual_data)

    @mock.patch("main.skill_list", [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}])
    @mock.patch('main.skill_id', ['2.A.1.a'])
    def test_skill_sort(self):
        skill = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 3.0}]
        expected_data = ['2.A.1.a']
        actual_data = main.skill_sort(skill)
        self.assertEqual(expected_data, actual_data)

    def test_skill_sort_different_name(self):
        skill = [{'id': '2.A.1.a', 'name': 'writing Comprehension', 'value': 3.0}]
        expected_data = ['2.A.1.a']
        actual_data = main.skill_sort(skill)
        self.assertEqual(expected_data, actual_data)

    def test_skill_sort_multiple_skills(self):
        skill = [{'id': '2.A.1.a', 'name': 'writing Comprehension', 'value': 3.0},
                 {"id": "2.A.1.b", "name": "Active Listening", "value": 67.62}]
        expected_data = ['2.A.1.a', '2.A.1.b']
        actual_data = main.skill_sort(skill)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_reverse_search(self, mocked_request):
        skills = '1'
        expected_data = 1115
        mocked_request.return_value = Mock(text='{"selection":{"skills":{"2.A.1.c":"Writing", '
                                                '"2.A.1.d":"Speaking"}}, "results":[{"likely_soc_codes":[1115]}]}')
        actual_data = main.reverse_search(skills)
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/reversematch?weights=100%2C100'
                                          '%2C100%2C100&skills=1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_find_job(self, mocked_request):
        rev = '1'
        expected_data = 'Chief executives and senior officials'
        mocked_request.return_value = Mock(text='{"soc":1115,"title":"Chief executives and senior officials"}',
                                           status_code=200)

        actual_data = main.find_job(rev)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/code/1', verify=False)
        self.assertEqual(expected_data, actual_data)

    def test_invalid_job_input(self):
        job = "invalid_job"
        expected_data = job + " is not a valid input"
        try:
            actual_data = main.get_soc_code(job)
        except Exception as e:
            actual_data = str(e)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_no_response_from_API(self, mocked_request):
        expected_data = 'There seems to be a issue getting your job recommendations back to you, please try again later'
        mocked_request.return_value = Mock(status_code=400)

        try:
            actual_data = main.api_call('https://api.lmiforall.org.uk/api/v1/soc/search?q=', 'plumber')
        except Exception as e:
            actual_data = str(e)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/search?q=plumber', verify=False)
        self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
