import click
from flask.cli import with_appcontext
import subprocess

from .extensions import db
from .models import User, Doodle

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name="drop_tables")
@with_appcontext
def drop_tables():
    db.drop_all()

@click.command(name="db")
@with_appcontext
def database():
    p = subprocess.call(["sqlite3", "rpgdle/db.sqlite3"])
