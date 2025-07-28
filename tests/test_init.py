from xmlcustomformatter import main
from pytest import MonkeyPatch, CaptureFixture


def test_main_prints_hello(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello from xmlcustomformatter!"
