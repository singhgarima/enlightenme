import unittest
from unittest import mock
from unittest.mock import call

from click.testing import CliRunner

from readme.readme import cli
from tests.fixtures import create_news


class TestSource(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()
        self._cli = cli

    def test_help(self):
        result = self._runner.invoke(self._cli, ["source", "--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("get latest news from different sources", result.output)

    @mock.patch('readme.sources.hacker_news.HackerNews.fetch')
    def test_source_when_typical_then_should_display_help_text(self, mock_fetch):
        source_name = "hacker-news"
        result = self._runner.invoke(self._cli, ["source", source_name])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Fetching news from source: %s" % source_name, result.output)
        mock_fetch.assert_called_once()

    @mock.patch('readme.sources.hacker_news.HackerNews.fetch')
    @mock.patch('readme.news.ConsoleNewsFormatter')
    def test_source_when_typical_then_should_display_stories(self, mock_formatter, mock_fetch):
        news_list = [(create_news()), (create_news())]
        mock_fetch.return_value = news_list

        source_name = "hacker-news"
        self._runner.invoke(self._cli, ["source", source_name])

        mock_fetch.assert_called_once()
        mock_formatter.assert_has_calls([call(news_list), call().format(), call().send()])

    def test_when_missing_source(self):
        result = self._runner.invoke(self._cli, ["source"])

        self.assertNotEqual(0, result.exit_code)
        self.assertIn("Error: Missing argument \"source_name\".", result.output)

    def test_when_invalid_source(self):
        result = self._runner.invoke(self._cli, ["source", "invalid"])

        self.assertIn("Invalid source supplied. See --help", result.output)


class TestSourceList(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()
        self._cli = cli

    def test_typical(self):
        result = self._runner.invoke(self._cli, ["source", "list"])
        self.assertIn("Currently the plugin supports the following sources", result.output)
        self.assertIn("hacker-new", result.output)
