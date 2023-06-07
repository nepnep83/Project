import unittest
from unittest import mock
from unittest.mock import Mock

import recommend_jobs

_range = 2
interests_range = 1
job_num = 1


class MyTestCase(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['engineer', 'No'])
    def test_get_claimants_jobs(self, mock):
        expected_data = ['engineer']
        actual_data = recommend_jobs.get_claimants_jobs()
        self.assertEqual(expected_data, actual_data)

    @mock.patch('builtins.input', side_effect=['plumber'])
    def test_get_claimants_interests(self, mock):
        expected_data = ['plumber']
        actual_data = recommend_jobs.get_claimants_interests()
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_get_soc_code(self, mocked_request):
        job = "1"
        expected_data = 3113

        mocked_request.return_value = Mock(text='[{"soc":3113}]', status_code=200)
        actual_data = recommend_jobs.get_soc_code(job)
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/search?q=1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_invalid_job_input(self, mocked_request):
        job = "invalid_job"
        expected_data = job + " is not a valid input"
        mocked_request.return_value = Mock(text='[]', status_code=200)
        try:
            actual_data = recommend_jobs.get_soc_code(job)
        except Exception as e:
            actual_data = str(e)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/search?q=invalid_job', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_soc_to_onet(self, mocked_request):
        soc = "1"
        expected_data = "53-6041.00"

        mocked_request.return_value = Mock(text='{"onetCodes":[{"code":"53-6041.00"}]}', status_code=200)
        actual_data = recommend_jobs.soc_to_onet(soc)
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/soc2onet/1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('recommend_jobs.skill_sort')
    @mock.patch('requests.get')
    @mock.patch('requests.models.Response.json')
    def test_onet_skills(self, mocked_json, mocked_request, mocked_sort):
        onet = '1'
        expected_data = ['2.A.1.a', '2.A.1.b']
        skill_list = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}]
        mocked_request.return_value = mocked_json
        mocked_json.json.return_value = {"scales": [{"id": "LV", "skills": [
            {"id": "2.A.1.a", "name": "Reading Comprehension", "value": 4.0},
            {"id": "2.A.1.b", "name": "Active Listening", "value": 3.62}]}]}
        mocked_sort.return_value = ['2.A.1.a', '2.A.1.b']

        actual_data = recommend_jobs.onet_skills(onet, skill_list, _range)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/skills/1', verify=False)
        mocked_sort.assert_called_with([{"id": "2.A.1.a", "name": "Reading Comprehension", "value": 4.0},
                                        {"id": "2.A.1.b", "name": "Active Listening", "value": 3.62}], skill_list)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('common.api_call')
    def test_onet_interests(self, mock_api):
        onet = '1'
        expected_data = [{'id': '1.B.1.a', 'name': 'Realistic', 'value': 1.33}]
        mock_api.return_value = {'onetcode': '23-1011.00',
                                 'scales': [{'id': 'IH', 'interests': [
                                     {'id': '1.B.1.g', 'name': 'First Interest High-Point', 'value': 5.0}]},
                                            {'id': 'OI', 'interests': [
                                                {'id': '1.B.1.a', 'name': 'Realistic', 'value': 1.33}]}]}

        actual_data = recommend_jobs.onet_interests(onet, 1)

        mock_api.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/interests/1')
        self.assertEqual(expected_data, actual_data)

    def test_skill_sort(self):
        skill = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 3.0}]
        skill_list = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}]
        expected_data = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 7.0}]
        actual_data = recommend_jobs.skill_sort(skill, skill_list)
        self.assertEqual(expected_data, actual_data)

    def test_skill_sort_different_name(self):
        skill = [{'id': '2.A.1.a', 'name': 'writing Comprehension', 'value': 3.0}]
        skill_list = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}]
        expected_data = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 7.0}]
        actual_data = recommend_jobs.skill_sort(skill, skill_list)
        self.assertEqual(expected_data, actual_data)

    def test_skill_sort_multiple_skills(self):
        skill_list = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0}]
        skill = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 3.0},
                 {"id": "2.A.1.b", "name": "Active Listening", "value": 67.62}]
        expected_data = [{"id": "2.A.1.b", "name": "Active Listening", "value": 67.62},
                         {'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 7.0}]
        actual_data = recommend_jobs.skill_sort(skill, skill_list)
        self.assertEqual(expected_data, actual_data)

    def test_get_ids(self):
        skill = [{'id': '2.A.1.a', 'name': 'writing Comprehension', 'value': 3.0},
                 {"id": "2.A.1.b", "name": "Active Listening", "value": 67.62}]
        expected_data = ['2.A.1.a', '2.A.1.b']
        actual_data = recommend_jobs.get_ids(skill)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_reverse_search(self, mocked_request):
        skills = '1'
        interests = '1'
        expected_data = [1115]
        mocked_request.return_value = Mock(text='{"selection":{"skills":{"2.A.1.c":"Writing", '
                                                '"2.A.1.d":"Speaking"}}, "results":[{"likely_soc_codes":[1115]}]}',
                                           status_code=200)
        actual_data = recommend_jobs.reverse_search(skills, interests)
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/reversematch?weights=100%2C100'
                                          '%2C100%2C100&interests=1&skills=1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_find_job(self, mocked_request):
        rev = ['1']
        job_num = 1
        expected_data = ['Chief executives and senior officials']
        mocked_request.return_value = Mock(text='{"soc":1115,"title":"Chief executives and senior officials"}',
                                           status_code=200)

        actual_data = recommend_jobs.find_job(rev, job_num)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/code/1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('builtins.input', side_effect=['engineer', 'No', 'engineer'])
    @mock.patch('recommend_jobs.get_soc_code')
    @mock.patch('recommend_jobs.soc_to_onet')
    @mock.patch('recommend_jobs.onet_skills')
    @mock.patch('recommend_jobs.onet_interests')
    @mock.patch('recommend_jobs.reverse_search')
    @mock.patch('recommend_jobs.find_job')
    def test_run(self, mocked_job, mocked_search, mocked_onet_interests,
                 mocked_onet_skills, mocked_onet, mocked_soc, Mock):
        expected_data = ['plumber']
        mocked_job.return_value = ['plumber']
        mocked_search.return_value = [1115]
        mocked_onet_interests.return_value = [{'id': '1.B.1.a', 'name': 'Realistic', 'value': 1.33}]
        mocked_onet_skills.return_value = [{'id': '2.A.1.a', 'name': 'Reading Comprehension', 'value': 4.0},
                                           {'id': '2.A.1.b', 'name': 'Writing Comprehension', 'value': 4.0}]
        mocked_onet.return_value = '2'
        mocked_soc.return_value = '1'

        actual_data = recommend_jobs.run(_range, interests_range, job_num)

        self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
