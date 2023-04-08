import os

import click


@click.group()
def cli():
    pass


@cli.command("api")
def api():
    from src.app import app

    app.run(
        host=os.getenv("HTTP_HOST", default="localhost"),
        port=int(os.getenv("HTTP_PORT", default=5000)),
        debug=bool(os.getenv("DEBUG", default=1)),
    )


if __name__ == "__main__":
    cli()
