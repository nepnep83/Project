import unittest
from unittest import mock

from Backend import job_vacancies

job = 'plumber'
_range = 1
expected_data_1 = [{'id': 12181272, 'title': 'Plumber', 'summary': "Plumbers", 'company': 'Talent Finder',
                          'activedate': {'start': '2023-05-15T15:31:00Z', 'end': '2023-06-14T15:31:00Z'},
                          'location': {'location': 'BR1 3NN', 'city': '', 'area': '', 'postcode': '', 'country': ''},
                          'link': 'https://findajob.dwp.gov.uk/details/12181272'}]


class MyTestCase(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['10', 'da1'])
    def test_get_claimants_jobs(self, mock):
        expected_data = '10', 'da1'

        actual_data = job_vacancies.get_claimant_info()

        self.assertEqual(expected_data, actual_data)

    @mock.patch('Backend.recommend_jobs.run')
    def test_get_recommended_jobs(self, mocked_recommendation):
        expected_data = 'plumber'
        mocked_recommendation.return_value = 'plumber'

        actual_data = job_vacancies.get_recommend_jobs()

        self.assertEqual(expected_data, actual_data)

    @mock.patch('Backend.common.api_call')
    def test_find_vacancies(self, mocked_api):
        distance = '1'
        location = '2'
        job = '3'
        mocked_api.return_value = [{'id': 12181272, 'title': 'Plumber', 'summary': "Plumbers", 'company': 'Talent Finder',
                          'activedate': {'start': '2023-05-15T15:31:00Z', 'end': '2023-06-14T15:31:00Z'},
                          'location': {'location': 'BR1 3NN', 'city': '', 'area': '', 'postcode': '', 'country': ''},
                          'link': 'https://findajob.dwp.gov.uk/details/12181272'}]

        actual_data = job_vacancies.find_vacancies(distance, location, job)

        mocked_api.assert_called_with(
            "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=1&location=2&keywords=3")
        self.assertEqual(expected_data_1, actual_data)

    @mock.patch('Backend.job_vacancies.find_vacancies')
    @mock.patch('Backend.job_vacancies.get_claimant_info')
    def test_run(self, mocked_info, mocked_vacancies):
        mocked_info.return_value = [10, 'da1']
        mocked_vacancies.return_value = [
            {'id': 12181272, 'title': 'Plumber', 'summary': "Plumbers", 'company': 'Talent Finder',
             'activedate': {'start': '2023-05-15T15:31:00Z', 'end': '2023-06-14T15:31:00Z'},
             'location': {'location': 'BR1 3NN', 'city': '', 'area': '', 'postcode': '', 'country': ''},
             'link': 'https://findajob.dwp.gov.uk/details/12181272'}]

        actual_data = job_vacancies.run(job, _range)

        self.assertEqual(expected_data_1, actual_data)
        mocked_vacancies.assert_called_with(10, 'da1', 'plumber')


if __name__ == '__main__':
    unittest.main()
