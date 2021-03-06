import unittest

from click.testing import CliRunner

from enlightenme.enlightenme import cli


class TestEnlightenme(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()
        self._cli = cli

    def test_base_command(self):
        result = self._runner.invoke(self._cli)

        self.assertEqual(0, result.exit_code)
        self.assertIn("collect news/updates from your favorite tech channels", result.output)

    def test_help(self):
        result = self._runner.invoke(self._cli, ["--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("collect news/updates from your favorite tech channels", result.output)

    def test_list_of_commands(self):
        result = self._runner.invoke(self._cli, ["--help"])

        self.assertIn("source", result.output)

    def test_invalid_command(self):
        result = self._runner.invoke(self._cli, ["invalid"])

        self.assertNotEqual(0, result.exit_code)
        self.assertIn('Error: No such command "invalid".', result.output)
