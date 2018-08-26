import unittest
from unittest import mock
from unittest.mock import call

from click.testing import CliRunner

from enlightenme.enlightenme import cli
from tests.fixtures import create_news


class TestSource(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()
        self._cli = cli

    def test_help(self):
        result = self._runner.invoke(self._cli, ["source", "--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("get latest news from different sources", result.output)
        self.assertIn("--format [list|csv]  Displays news in a format", result.output)
        self.assertIn("--output TEXT        Write to FILE instead of stdout", result.output)

    @mock.patch('enlightenme.commands.helpers.fetcher.Fetcher.fetch_and_format')
    @mock.patch('enlightenme.commands.helpers.fetcher.Fetcher.valid', return_value = True)
    def test_source_when_typical_then_should_display_help_text(self, _, __):

        source_name = "hacker-news"
        result = self._runner.invoke(self._cli, ["source", source_name])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Fetching news from source: %s" % source_name, result.output)

    @mock.patch('enlightenme.commands.helpers.fetcher.Fetcher.valid')
    @mock.patch('enlightenme.commands.helpers.fetcher.Fetcher.fetch_and_format')
    def test_source_when_typical_then_fetch_and_format_using_fetcher(self, mock_fetch_and_format, mock_valid):
        mock_valid.return_value = True

        source_name = "hacker-news"
        self._runner.invoke(self._cli, ["source", source_name])

        mock_fetch_and_format.assert_called_once_with()

    @mock.patch('enlightenme.commands.helpers.fetcher.Fetcher')
    def test_source_when_keywords_provided_then_fetch_and_format_using_fetcher(self, mock_fetcher):
        mock_object = mock.Mock()
        mock_fetcher.return_value = mock_object
        mock_object.mock_valid.return_value = True
        mock_object.fetch_and_format.return_value = None

        source_name = "hacker-news"
        self._runner.invoke(self._cli, ["source", source_name, "--keywords", "python,chaos"])

        mock_fetcher.assert_called_once_with(source_name, format_type='list', keywords=["python", "chaos"])
        mock_object.fetch_and_format.assert_called_once_with()

    @mock.patch('enlightenme.commands.helpers.fetcher.Fetcher.fetch_and_format')
    @mock.patch('enlightenme.news.news_output.NewsOutput')
    def test_source_when_typical_then_should_display_stories(self, mock_output, mock_fetch_and_format):
        news_list = [(create_news()), (create_news())]
        mock_fetch_and_format.return_value = news_list

        source_name = "hacker-news"
        self._runner.invoke(self._cli, ["source", source_name])

        mock_output.assert_has_calls([call(news_list), call().write_to(file_name=None)])

    def test_when_missing_source(self):
        result = self._runner.invoke(self._cli, ["source"])

        self.assertNotEqual(0, result.exit_code)
        self.assertIn("Error: Missing argument \"source_name\".", result.output)

    @mock.patch('enlightenme.commands.helpers.fetcher.Fetcher.valid')
    def test_when_invalid_source(self, mock_valid):
        mock_valid.return_value = False

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


