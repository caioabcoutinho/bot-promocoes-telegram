import run


def test_supervisor_uses_current_python_and_both_components():
    assert run.CHILDREN == ("run_phase3.py", "run_bot.py")
    assert run.ROOT.is_dir()
