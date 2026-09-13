"""Unit tests for main module."""

import pytest

from psg.main import main


@pytest.mark.unit
def test_main_function_exists() -> None:
    assert callable(main)


@pytest.mark.unit
def test_main_function_runs(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    captured = capsys.readouterr()
    assert "psg" in captured.out
