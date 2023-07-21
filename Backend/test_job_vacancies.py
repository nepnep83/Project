import unittest
from unittest import mock

from Backend import job_vacancies

API_RESPONSE = [{'id': 12181272, 'title': 'Plumber', 'summary': "Plumbers", 'company': 'Talent Finder',
                 'activedate': {'start': '2023-05-15T15:31:00Z', 'end': '2023-06-14T15:31:00Z'},
                 'location': {'location': 'BR1 3NN', 'city': '', 'area': '', 'postcode': '', 'country': ''},
                 'link': 'https://findajob.dwp.gov.uk/details/12181272'}]
TRAVEL_DISTANCE = 10
POSTCODE = "POST_CODE"
TITLE = "job"
TITLE_LIST = ["job", "job 2"]
API_CALL = "https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5" \
           + "&radius=" + str(TRAVEL_DISTANCE) \
           + "&location=" + POSTCODE \
           + "&keywords=" + TITLE


class MyTestCase(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['10', 'da1'])
    def test_get_claimants_jobs(self, mock):
        expected_data = '10', 'da1'

        actual_data = job_vacancies.get_claimant_info()

        self.assertEqual(expected_data, actual_data)

    @mock.patch('Backend.job_vacancies.call_vacancy_api')
    def test_is_at_least_one_vacancy_nationally_true(self, mocked_call):
        mocked_call.return_value = TITLE

        actual_data = job_vacancies.is_at_least_one_vacancy_nationally(TITLE)

        self.assertEqual(actual_data, True)
        mocked_call.assert_called_with(TITLE)

    @mock.patch('Backend.job_vacancies.call_vacancy_api')
    def test_is_at_least_one_vacancy_nationally_false(self, mocked_call):
        mocked_call.return_value = None

        actual_data = job_vacancies.is_at_least_one_vacancy_nationally(TITLE)

        self.assertEqual(actual_data, False)
        mocked_call.assert_called_with(TITLE)

    @mock.patch('Backend.common.api_call')
    def test_call_vacancy_api(self, mocked_api):
        mocked_api.return_value = API_RESPONSE

        actual_data = job_vacancies.call_vacancy_api(TITLE, postcode=POSTCODE, travel_distance=TRAVEL_DISTANCE)

        mocked_api.assert_called_with(API_CALL)
        self.assertEqual(actual_data, API_RESPONSE[0])

    @mock.patch('Backend.common.api_call')
    def test_call_vacancy_api_fewer_inputs(self, mocked_api):
        mocked_api.return_value = API_RESPONSE

        actual_data = job_vacancies.call_vacancy_api(TITLE)

        mocked_api.assert_called_with("https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5"
                                      + "&keywords=" + TITLE)
        self.assertEqual(actual_data, API_RESPONSE[0])

    @mock.patch('Backend.common.api_call')
    def test_call_vacancy_api_not_found(self, mocked_api):
        mocked_api.return_value = "not found"

        actual_data = job_vacancies.call_vacancy_api(TITLE, POSTCODE, TRAVEL_DISTANCE)

        mocked_api.assert_called_with(API_CALL)
        self.assertEqual(actual_data, None)

    @mock.patch('Backend.job_vacancies.call_vacancy_api', side_effect=[{"title": "title 2"}, {"title": "title 3"}])
    def test_get_vacancies_from_titles(self, mocks):
        recommended_jobs = [{"title": "title 1"}]

        job_vacancies.get_vacancies_from_titles(TITLE_LIST, POSTCODE, recommended_jobs)

        self.assertEqual(recommended_jobs, [{"title": "title 1"}, {"title": "title 2"}, {"title": "title 3"}])

    @mock.patch('Backend.job_vacancies.call_vacancy_api', side_effect=[{"title": "title 6"}])
    def test_get_vacancies_from_titles_already_found_5(self, mocks):
        recommended_jobs = [{"title": "title 1"}, {"title": "title 2"}, {"title": "title 3"}, {"title": "title 4"}, {"title": "title 5"}]

        job_vacancies.get_vacancies_from_titles(TITLE_LIST, POSTCODE, recommended_jobs)

        self.assertEqual(recommended_jobs, [{"title": "title 1"}, {"title": "title 2"}, {"title": "title 3"}, {"title": "title 4"}, {"title": "title 5"}])

    @mock.patch('Backend.job_vacancies.call_vacancy_api', side_effect=[{"title": "title 1"}, {"title": "title 1"}, {"title": "title 1"}])
    def test_get_vacancies_from_titles_duplicate_jobs(self, mocks):
        recommended_jobs = [{"title": "title 1"}]

        job_vacancies.get_vacancies_from_titles(TITLE_LIST, POSTCODE, recommended_jobs)

        self.assertEqual(recommended_jobs, [{"title": "title 1"}])


if __name__ == '__main__':
    unittest.main()
