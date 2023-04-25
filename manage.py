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


@cli.command("create-superuser")
@click.argument("email")
@click.argument("password")
def create_superuser(email, password):
    from src.app import app
    from src.db import db_models
    from src.repositories.auth_repository import AuthRepository
    from src.repositories.role_repository import RolesRepository
    from src.services.auth_service import AuthService

    app.app_context().push()
    db_models.db.create_all()

    auth_repository = AuthRepository(db_models.db)
    roles_repository = RolesRepository(db_models.db)
    auth_service = AuthService(
        auth_repository=auth_repository, roles_repository=roles_repository
    )
    auth_service.create_admin(email, password)


if __name__ == "__main__":
    cli()
