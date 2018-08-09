import unittest

from click.testing import CliRunner

from readme.readme import cli


class TestSource(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()
        self._cli = cli

    def test_help(self):
        result = self._runner.invoke(self._cli, ["source", "--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("get latest news from different sources", result.output)

    def test_for_a_source_name(self):
        source_name = "hacker-news"
        result = self._runner.invoke(self._cli, ["source", source_name])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Fetching news from source: %s" % source_name, result.output)

    def test_when_missing_source(self):
        result = self._runner.invoke(self._cli, ["source"])

        self.assertNotEqual(0, result.exit_code)
        self.assertIn("Error: Missing argument \"source_name\".", result.output)

class TestSourceList(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()
        self._cli = cli

    def test_typical(self):
        result = self._runner.invoke(self._cli, ["source", "list"])
        self.assertIn("Currently the plugin supports the following sources", result.output)
        self.assertIn("hacker-new", result.output)
