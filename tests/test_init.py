from xmlcustomformatter import main
from pytest import CaptureFixture


class TestInit:
    def test_main_prints_hello(self, capsys: CaptureFixture[str]) -> None:
        """Tests that the main function prints correctly"""
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "Hello from xmlcustomformatter!"
