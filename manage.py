import click


@click.group()
def cli():
    pass


@cli.command("api")
def api():
    from src.app import app

    app.run(
        host=app.config["HTTP_HOST"],
        port=app.config["HTTP_PORT"],
        debug=True,
    )


if __name__ == "__main__":
    cli()
