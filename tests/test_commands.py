import unittest

from click.testing import CliRunner

from readme.readme import cli


class TestSource(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()
        self._cli = cli

    def test_typical(self):
        source_name = "hacker-news"
        result = self._runner.invoke(self._cli, ["source", source_name])
        self.assertIn("Fetching news from source: %s" % source_name, result.output)

    def test_when_missing_source(self):
        pass
