from xmlcustomformatter import main
from pytest import MonkeyPatch, CaptureFixture


class TestInit:
    def test_main_prints_hello(
        self, monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
    ) -> None:
        """Tests that the main function prints correctly"""
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "Hello from xmlcustomformatter!"
