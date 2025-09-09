"""This module tests the entry point."""

from unittest.mock import patch

from pytest import MonkeyPatch

from xmlcustomformatter import main


class TestInit:
    """This class tests the entry point."""

    @staticmethod
    def test_main_invokes_formatter(monkeypatch: MonkeyPatch) -> None:
        """Tests that main creates XMLCustomFormatter with correct args."""

        test_args = [
            "xmlfmt",
            "input.xml",
            "output.xml",
        ]
        monkeypatch.setattr("sys.argv", test_args)

        with patch("xmlcustomformatter.XMLCustomFormatter") as mock_formatter:
            main()

        mock_formatter.assert_called_once()
        args = mock_formatter.call_args

        assert args.args[0] == "input.xml" and args.args[1] == "output.xml"
