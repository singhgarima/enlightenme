import unittest
from unittest import mock
from unittest.mock import call

from enlightenme.news.news_output import NewsOutput


class TestNewsOutput(unittest.TestCase):
    def setUp(self):
        self._content = 'Hello World'
        self._output = NewsOutput(self._content)

    @mock.patch('click.echo')
    def test_write_to_when_option_is_console_will_print_the_output(self, mock_echo):
        self._output.write_to()

        mock_echo.assert_called_once_with(self._content)

    @mock.patch("builtins.open", create=True)
    def test_write_to_when_option_is_file_will_write_to_a_file(self, mock_open):
        file_name = 'test.txt'

        self._output.write_to(file_name)

        mock_open.assert_has_calls([call(file_name, 'w'),
                                    call().__enter__(),
                                    call().__enter__().write(self._content),
                                    call().__exit__(None, None, None)])
