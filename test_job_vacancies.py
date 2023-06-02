import unittest
from unittest import mock
from unittest.mock import Mock

import job_vacancies


class MyTestCase(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['10', 'da1'])
    def test_get_claimants_jobs(self, mock):
        expected_data = '10', 'da1'
        actual_data = job_vacancies.get_claimant_info()
        self.assertEqual(expected_data, actual_data)

    @mock.patch('recommend_jobs.run')
    def test_get_recommended_jobs(self, mocked_recommendation):
        expected_data = 'plumber'
        mocked_recommendation.return_value = 'plumber'

        actual_data = job_vacancies.get_recommend_jobs()

        self.assertEqual(expected_data, actual_data)

    @mock.patch('common.api_call')
    def test_find_vacancies(self, mocked_api):
        distance = '1'
        location = '2'
        job = '3'
        expected_data = [
            {
                "id": 12119846,
                "title": "Plumber",
                "summary": "Plumber Bromley Monday to Friday Mobile - Personal Use of Vehicle Door to Door Are you looking for a new maintenance role as a Plumber? An opportunity to complete work as a plumber on a large commercial retail contract has become available with one of our clients. As a plumber on this contract, you will be responsible for all planned and reactive plumbing maintenance. Plumber - Company Benefits: • Personal Use of Vehicle • Door to Door travel • 25 days holiday  8 Bank Holidays • Extra day off on your birthday • Employee of the Month awards • Annual Salary Uplifts • Further Training and Progression Plumber - Essential Qualifications: • NVQ L3 Plumbing • Experience completing commercial maintenance If this position as a Plumber is of interest to you, click APPLY and send your CV directly to us. Or call 0208 092 6500 and ask for Hannah.",
                "company": "HVAC Recruitment Ltd",
                "activedate": {
                    "start": "2023-05-05T15:45:00Z",
                    "end": "2023-06-04T15:45:00Z"
                }}]
        mocked_api.return_value = [
            {
                "id": 12119846,
                "title": "Plumber",
                "summary": "Plumber Bromley Monday to Friday Mobile - Personal Use of Vehicle Door to Door Are you looking for a new maintenance role as a Plumber? An opportunity to complete work as a plumber on a large commercial retail contract has become available with one of our clients. As a plumber on this contract, you will be responsible for all planned and reactive plumbing maintenance. Plumber - Company Benefits: • Personal Use of Vehicle • Door to Door travel • 25 days holiday  8 Bank Holidays • Extra day off on your birthday • Employee of the Month awards • Annual Salary Uplifts • Further Training and Progression Plumber - Essential Qualifications: • NVQ L3 Plumbing • Experience completing commercial maintenance If this position as a Plumber is of interest to you, click APPLY and send your CV directly to us. Or call 0208 092 6500 and ask for Hannah.",
                "company": "HVAC Recruitment Ltd",
                "activedate": {
                    "start": "2023-05-05T15:45:00Z",
                    "end": "2023-06-04T15:45:00Z"
                }}]

        actual_data = job_vacancies.find_vacancies(distance, location, job)

        mocked_api.assert_called_with("https://api.lmiforall.org.uk/api/v1/vacancies/search?limit=5&radius=1&location=2&keywords=3")
        self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
