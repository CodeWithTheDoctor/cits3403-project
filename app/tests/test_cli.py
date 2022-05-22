def test_commands_printed(runner):
    options = ["add-puzzle", "delete-puzzle", "delete-user", "puzzles", "users"]
    for option in options:
        assert option in runner.invoke(args="--help").output


def test_puzzle_added(runner):
    result = runner.invoke(args="add-puzzle '123 \n'")
    assert "success" in result.output

    result = runner.invoke(args="puzzles")
    assert "Puzzle: 4" in result.output


def test_print_puzzles(runner):
    result = runner.invoke(args="puzzles")
    assert "Puzzle" in result
