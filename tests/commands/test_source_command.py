import unittest
from unittest import mock
from unittest.mock import call

from click.testing import CliRunner

from enlightenme.enlightenme import cli
from tests.fixtures import create_news


class TestSourceCommand(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()
        self._cli = cli

    def test_help(self):
        result = self._runner.invoke(self._cli, ["source", "--help"])

        self._assert_result_contains_help_text(result)

    def test_when_source_command_executed_without_source_name(self):
        result = self._runner.invoke(self._cli, ["source"])

        self._assert_result_contains_help_text(result)

    @mock.patch('enlightenme.news.news_manager.NewsManager.fetch_and_format')
    def test_source_when_typical_then_should_display_help_text(self, _):
        source_name = "hacker-news"
        result = self._runner.invoke(self._cli, ["source", source_name])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Fetching news from source: %s" % source_name, result.output)

    @mock.patch('enlightenme.news.news_manager.NewsManager.fetch_and_format')
    def test_source_when_typical(self, mock_fetch_and_format):
        source_name = "hacker-news"
        self._runner.invoke(self._cli, ["source", source_name])

        mock_fetch_and_format.assert_called_once_with()

    @mock.patch('enlightenme.news.news_manager.NewsManager')
    def test_source_when_keywords_provided(self, mock_fetcher):
        mock_object = mock.Mock()
        mock_fetcher.return_value = mock_object
        mock_object.mock_valid.return_value = True
        mock_object.fetch_and_format.return_value = None

        source_name = "hacker-news"
        self._runner.invoke(self._cli, ["source", "--keywords", "python,chaos", source_name])

        mock_fetcher.assert_called_once_with(source_name,
                                             source_params={},
                                             format_type='list',
                                             keywords=["python", "chaos"])
        mock_object.fetch_and_format.assert_called_once_with()

    @mock.patch('enlightenme.news.news_manager.NewsManager')
    def test_source_when_keywords_and_command_params_are_provided(self, mock_fetcher):
        mock_object = mock.Mock()
        mock_fetcher.return_value = mock_object
        mock_object.mock_valid.return_value = True
        mock_object.fetch_and_format.return_value = None

        source_name = "reddit"
        self._runner.invoke(self._cli, ["source", "--keywords", "python,chaos",
                                        source_name,
                                        '--client-id', 'reddit-identifier',
                                        '--client-secret', 'reddit-app-secret'
                                        ])

        mock_fetcher.assert_called_once_with(source_name,
                                             format_type='list',
                                             keywords=["python", "chaos"],
                                             source_params={
                                                 'client_id': 'reddit-identifier',
                                                 'client_secret': 'reddit-app-secret'}
                                             )
        mock_object.fetch_and_format.assert_called_once_with()

    @mock.patch('enlightenme.news.news_manager.NewsManager.fetch_and_format')
    @mock.patch('enlightenme.news.news_output.NewsOutput')
    def test_source_when_typical_then_should_display_stories(self, mock_output, mock_fetch_and_format):
        news_list = [(create_news()), (create_news())]
        mock_fetch_and_format.return_value = news_list

        source_name = "hacker-news"
        self._runner.invoke(self._cli, ["source", source_name])

        mock_output.assert_has_calls([call(news_list), call().write_to(file_name=None)])

    def test_when_invalid_source(self):
        result = self._runner.invoke(self._cli, ["source", "invalid"])

        self.assertIn("Error: Invalid source invalid supplied. See --help", result.output)

    def _assert_result_contains_help_text(self, result):
        self.assertEqual(0, result.exit_code)
        self.assertIn("helps getting latest news from specified sources", result.output)
        self.assertIn("--format [list|csv]  Displays news in a format", result.output)
        self.assertIn("--output TEXT        Write to FILE instead of stdout", result.output)
        self.assertIn("reddit       Source: Reddit (http://reddit.com/)", result.output)
        self.assertIn("hacker-news  Source: hacker-news (https://news.ycombinator.com/)", result.output)
