import sqlite3
from datetime import datetime

import click
from flask import current_app, g

import csv


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(): # this is run via flask --app jeem init-db in terminal / flask --app jeem init-db   
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))



    with open('jeem/data.csv') as data:
        datareader = csv.DictReader(data)
        for row in datareader:
            db.execute('INSERT INTO albums (album_name, album_id, release_date,total_tracks, spotify_album_link, spotify_album_image_url, band_name, band_id, band_popularity, band_spotify_url, band_genre) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        (row['name'],
                        row['id'],
                        row['release_date'],
                        row['total_tracks'],
                        row['link'],
                        row['img'],
                        row['band_spotify_name'],
                        row['band_spotify_id'],
                        row['band_spotify_popularity'],
                        row['band_spotify_link'],
                        row['band_genre'])
            )
        db.commit()
                           


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)