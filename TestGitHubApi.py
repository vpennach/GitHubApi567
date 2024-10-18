import unittest
from unittest.mock import patch
import requests

from GitHubApi import get_repos_and_commits

class TestGitHubRepos(unittest.TestCase):
    
    @patch('requests.get')
    def test_valid_user_with_repos(self, mock_get):
        #Has to mock the test cause the API will change
        mock_repos_response = [
            {"name": "Repo1"},
            {"name": "Repo2"}
        ]
        
        mock_commits_response = [{"vin": "123"}, {"vin": "456"}]

        mock_get.side_effect = [
            unittest.mock.Mock(status_code=200, json=lambda: mock_repos_response),
            unittest.mock.Mock(status_code=200, json=lambda: mock_commits_response),  # For Repo1
            unittest.mock.Mock(status_code=200, json=lambda: mock_commits_response)   # For Repo2
        ]

        result = get_repos_and_commits("valid_user")

        expected = [
            "Repo: Repo1 Number of commits: 2",
            "Repo: Repo2 Number of commits: 2"
        ]

        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_invalid_username(self, mock_get):
        mock_get.return_value = unittest.mock.Mock(status_code=404, json=lambda: {"message": "Not Found"})

        result = get_repos_and_commits("invalid_user")

        self.assertEqual(result, "Error: Username 'invalid_user' not found")
        
    @patch('requests.get')
    def test_other_error(self, mock_get):
        mock_get.return_value = unittest.mock.Mock(status_code=500, json=lambda: {"message": "Not Found"})

        result = get_repos_and_commits("valid_name")

        self.assertEqual(result, "Error: Unable to fetch data")

if __name__ == '__main__':
    unittest.main()
