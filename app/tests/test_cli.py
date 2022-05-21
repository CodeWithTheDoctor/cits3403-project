def test_flask(runner):
    result = runner.invoke(args="--help")
    print(result.output)

    assert False
