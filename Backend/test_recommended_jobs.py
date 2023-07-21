import unittest
from unittest import mock
from unittest.mock import Mock

from Backend import recommend_jobs

job = ['plumber']
onet_1 = "53-6041.00"
SKILL_1 = {'id': 'a', 'name': 'Reading Comprehension', 'value': 1}
SKILL_2 = {'id': 'b', 'name': 'Realistic', 'value': 2}
SKILL_3 = {"id": "c", "name": "Active Listening", "value": 3}
SKILL_4 = {'id': '2.A.1.a', 'name': 'Writing Comprehension', 'value': 4}
skill_id_1 = '2.A.1.a'
skill_id_2 = '2.A.1.b'


class MyTestCase(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=[job, 'No'])
    def test_get_claimants_jobs(self, mock):
        expected_data = [job]

        actual_data = recommend_jobs.get_claimants_jobs()

        self.assertEqual(expected_data, actual_data)

    @mock.patch('builtins.input', side_effect=[job])
    def test_get_claimants_interests(self, mock):
        expected_data = [job]

        actual_data = recommend_jobs.get_claimants_interests()

        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_get_soc_code(self, mocked_request):
        expected_data = 3113
        mocked_request.return_value = Mock(text='[{"soc":3113}]', status_code=200)

        actual_data = recommend_jobs.get_soc_code(job[0])

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/search?q=plumber', verify=False)
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
        expected_data = onet_1
        mocked_request.return_value = Mock(text='{"onetCodes":[{"code":"53-6041.00"}]}', status_code=200)

        actual_data = recommend_jobs.soc_to_onet(soc)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/soc2onet/1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_soc_to_onet_no_onet(self, mocked_request):
        soc = "1"
        expected_data = []
        mocked_request.return_value = Mock(text='{"onetCodes":[]}', status_code=200)

        actual_data = recommend_jobs.soc_to_onet(soc)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/soc2onet/1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    @mock.patch('requests.models.Response.json')
    def test_get_skills_from_onet_code(self, mocked_json, mocked_request):
        expected_data = [SKILL_3, SKILL_2]
        mocked_request.return_value = mocked_json
        mocked_json.json.return_value = {"scales": [{"skills": [SKILL_1, SKILL_2, SKILL_3]}]}

        actual_data = recommend_jobs.get_skills_from_onet_code(onet_1)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/skills/53-6041.00', verify=False)
        self.assertEqual(expected_data, actual_data)

    def test_add_new_skills_and_sort_common_name(self):
        skill_list = [SKILL_1]
        expected_data = [{'id': 'a', 'name': 'Reading Comprehension', 'value': 2}]

        recommend_jobs.add_new_skills_and_sort([SKILL_1], skill_list)

        self.assertEqual(expected_data, skill_list)

    def test_add_new_skills_and_sort_different_name(self):
        skill_list = [SKILL_1]
        expected_data = [SKILL_2, SKILL_1]

        recommend_jobs.add_new_skills_and_sort(skill_list, [SKILL_2])

        self.assertEqual(expected_data, skill_list)

    def test_add_new_skills_and_sort_reduce_common_values(self):
        skill_list = []
        expected_data = [{'id': '2.A.1.a', 'name': 'Writing Comprehension', 'value': 2}]

        recommend_jobs.add_new_skills_and_sort(skill_list, [SKILL_4])

        self.assertEqual(expected_data, skill_list)

    def test_get_skills_ids(self):
        skill = [SKILL_1, SKILL_2]
        expected_data = ['a', 'b']

        actual_data = recommend_jobs.get_skills_ids(skill)

        self.assertEqual(expected_data, actual_data)

    @mock.patch('Backend.common.api_call', side_effect=[{"results": [{"likely_soc_codes": [123], "title": "title"}]}])
    def test_get_recommended_soc_codes(self, mocked_request):
        skills = ['1', '2']
        expected_data = ([123], ['title'])
        actual_data = recommend_jobs.get_recommended_soc_codes(skills)
        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/o-net/reversematch?weights=100%2C100'
                                          '%2C100%2C100&skills=1,2')
        self.assertEqual(expected_data, actual_data)

    @mock.patch('requests.get')
    def test_find_job(self, mocked_request):
        rev = ['1']
        expected_data = ['Chief executives', 'officials senior']
        mocked_request.return_value = Mock(text='{"soc":1115,"add_titles":["Chief executives", "senior, officials"]}',
                                           status_code=200)

        actual_data = recommend_jobs.get_recommended_jobs(rev)

        mocked_request.assert_called_with('https://api.lmiforall.org.uk/api/v1/soc/code/1', verify=False)
        self.assertEqual(expected_data, actual_data)

    @mock.patch('Backend.recommend_jobs.get_soc_code')
    @mock.patch('Backend.recommend_jobs.soc_to_onet')
    @mock.patch('Backend.recommend_jobs.onet_skills')
    @mock.patch('Backend.recommend_jobs.onet_interests')
    @mock.patch('Backend.recommend_jobs.reverse_search')
    @mock.patch('Backend.recommend_jobs.find_job')
    def test_run(self, mocked_job, mocked_search, mocked_onet_interests,
                 mocked_onet_skills, mocked_onet, mocked_soc):

        expected_data = ([job], [job])
        mocked_job.return_value = [job]
        mocked_search.return_value = [1115]
        mocked_onet_interests.return_value = [SKILL_2]
        mocked_onet_skills.return_value = [SKILL_1, SKILL_4]
        mocked_onet.return_value = '2'
        mocked_soc.return_value = '1'

        actual_data = recommend_jobs.run(job)

        mocked_soc.assert_called_with('engineer')
        mocked_onet.assert_called_with('1')
        mocked_onet_skills.assert_called_with('2', [])
        mocked_onet_interests.assert_called_with('2', 1)
        mocked_search.assert_has_calls([mock.call(['2.A.1.a', '2.A.1.b'], ''), mock.call('', ['1.B.1.a'])])
        mocked_job.assert_called_with([1115], 1)
        self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
