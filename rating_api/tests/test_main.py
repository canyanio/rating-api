from click.testing import CliRunner


def test_main():
    # monkey-patch uvicorn.run
    import uvicorn  # type: ignore

    def _run(*args, **kw):
        pass

    saved_run = uvicorn.run
    uvicorn.run = _run
    #
    from rating_api.main import main

    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    #
    uvicorn.run = saved_run
