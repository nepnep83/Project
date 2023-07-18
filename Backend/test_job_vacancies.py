import unittest
from unittest import mock

from Backend import job_vacancies

job = 'plumber'
interest = 'engineer'
_range = 1
place_holder_distance = '10'
place_holder_location = 'da1'
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
        expected_data = ('plumber', 'engineer')
        mocked_recommendation.return_value = ('plumber', 'engineer')

        actual_data = job_vacancies.get_recommend_jobs(job)

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

        actual_data = job_vacancies.get_vacancies_from_soc_codes(distance, location, job, _range)

        mocked_api.assert_called_with(
            "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=1&location=2&keywords=3")
        self.assertEqual(expected_data_1, actual_data)

    @mock.patch('Backend.job_vacancies.find_vacancies')
    @mock.patch('Backend.job_vacancies.get_recommend_jobs')
    def test_run(self, mocked_info, mocked_vacancies):
        mocked_info.return_value = ['plumber', 'engineer']
        mocked_vacancies.return_value = [
            {'id': 12181272, 'title': 'Plumber', 'summary': "Plumbers", 'company': 'Talent Finder',
             'activedate': {'start': '2023-05-15T15:31:00Z', 'end': '2023-06-14T15:31:00Z'},
             'location': {'location': 'BR1 3NN', 'city': '', 'area': '', 'postcode': '', 'country': ''},
             'link': 'https://findajob.dwp.gov.uk/details/12181272'}]

        actual_data_1 = job_vacancies.run(job, place_holder_distance, place_holder_location, _range)

        self.assertEqual(expected_data_1, actual_data_1)
        mocked_vacancies.assert_has_calls([mock.call('10', 'da1', 'plumber', 1), mock.call('10', 'da1', 'engineer', 1)])


if __name__ == '__main__':
    unittest.main()
