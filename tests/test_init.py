"""This module tests the entry point."""

from pytest import CaptureFixture

from xmlcustomformatter import main


class TestInit:
    """This class tests the entry point."""

    def test_main_prints_hello(self, capsys: CaptureFixture[str]) -> None:
        """Tests that the main function prints correctly."""
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "Hello from xmlcustomformatter!"
