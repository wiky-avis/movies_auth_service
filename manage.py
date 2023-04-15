import os

import click
from dotenv import load_dotenv


load_dotenv()


@click.group()
def cli():
    pass


@cli.command("api")
def api():
    from src.app import app

    app.run(
        host=os.getenv("HTTP_HOST", default="localhost"),
        port=int(os.getenv("HTTP_PORT", default=8000)),
        debug=True,
    )


if __name__ == "__main__":
    cli()
