from xmlcustomformatter import main


def test_main_prints_hello(monkeypatch, capsys) -> None:
    # Act
    main()

    # Capture printed output
    captured = capsys.readouterr()

    # Assert
    assert captured.out.strip() == "Hello from xmlcustomformatter!"
