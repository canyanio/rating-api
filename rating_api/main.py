import click
import uvicorn  # type: ignore

from .app import get_app


@click.command()
@click.option("-h", "--host", type=click.STRING, default="0.0.0.0", show_default=True)
@click.option("-p", "--port", type=click.INT, default=8000, show_default=True)
@click.option(
    "--mongodb-uri",
    type=click.STRING,
    default="mongodb://localhost:27017",
    show_default=True,
)
@click.option(
    "--mongodb-db", type=click.STRING, default="rating_api", show_default=True
)
@click.option("-d", "--debug/--no-debug", default=False)
def main(
    host: str = "0.0.0.0",
    port: int = 8000,
    mongodb_uri: str = "mongodb://localhost:27017",
    mongodb_db: str = "rating_api",
    debug: bool = False,
    **kw,
):
    config = dict(
        host=host,
        port=port,
        mongodb_uri=mongodb_uri,
        mongodb_db=mongodb_db,
        debug=debug,
    )
    app = get_app(config)
    log_level = "info" if not config["debug"] else "debug"
    uvicorn.run(
        app,
        host=config["host"],
        port=config["port"],
        log_level=log_level,
    )


def main_with_env():  # pragma: no cover
    main(auto_envvar_prefix="RATING_API")
