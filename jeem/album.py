from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from jeem.auth import login_required
from jeem.db import get_db

import random

bp = Blueprint('album', __name__)

@bp.route('/album')
@bp.route('/album/<album_id>', methods=('GET', 'POST'))

@login_required
def index(album_id=None):

    db = get_db()
    random_album_id = None
    album_age = request.args.get('album_age')
    if album_age not in ['10', '20']:
        album_age = None
    elif album_age == '10':
        album_age = "< '2011-01-01'"
    elif album_age == '20':
        album_age = "> '2020-01-01'"
    album_type = request.args.get('album_type')
    if album_type not in ['pop punk', 'emo']:
        album_type = None

    # If no album_id provided, redirect to a random album
    if album_type is not None and album_id is None and not album_age:
        # generate a pp only ID and set albumtype null, redirect with ID
        album_id = db.execute(f'SELECT a.album_id FROM albums a '\
                              ' LEFT JOIN album_genres ag ' \
                              ' ON a.album_id = ag.album_id '
                              ' AND ag.genre = \'{album_type}\' '\
                                ' ORDER BY RANDOM() LIMIT 1;'
                                 ).fetchone()
        random_album_id = album_id['album_id']
        return redirect(url_for('album.index', album_id=random_album_id, album_type='x'))
    
    elif album_age and album_type and album_id is None:
        album_id = db.execute(f'SELECT album_id FROM albums WHERE band_genre = \'{album_type}\' '\
                              f' AND release_date {album_age} ' \
                                ' ORDER BY RANDOM() LIMIT 1;'
                                 ).fetchone()
        random_album_id = album_id['album_id']
        return redirect(url_for('album.index', album_id=random_album_id, album_type='x'))

    elif album_id is None:
        album_count = db.execute(' SELECT album_id FROM albums ORDER BY RANDOM() LIMIT 1; ').fetchone()
        # random_album_id = random.randint(1, album_count['count'])
        random_album_id = album_count['album_id']
        return redirect(url_for('album.index', album_id=random_album_id, album_type='x'))

    else:
        random_album_id = album_id
    
    album = db.execute('SELECT * FROM albums a '
                       ' WHERE album_id = ? LIMIT 1;', (random_album_id,)).fetchone()

    
    if album is None:
        abort(404, f"Album id {album_id} doesn't exist.")
    else:
        db.execute('INSERT INTO generations (user_id, spotify_id) VALUES (?,?)',
                   (session['user_id'], album_id))
        db.commit()
    

    if request.method == 'POST':
        rating = request.form['rating']
        error = None

        if error is not None:
            flash(error)
        else: 
            db.execute(
                'INSERT INTO ratings (user_id, spotify_id, rating)'
                'VALUES (?, ?, ?)',
                (session['user_id'], album_id, rating)
            )
            db.commit()
            db.execute(
                '''
                DELETE FROM ratings
                WHERE id NOT IN (
                    SELECT id FROM ratings WHERE spotify_id = (?) AND user_id = (?) ORDER BY rated_on desc LIMIT 1 
                )
                AND spotify_id = (?)
                AND user_id = (?)
                ''',
                (random_album_id, session['user_id'], random_album_id, session['user_id'])
            )
            db.commit()
            return redirect(url_for('album.index', album_id=random_album_id))
        
        



    ratings = db.execute('SELECT * '
        ' FROM ratings r '
        ' LEFT JOIN user u ON r.user_id = u.id '
        ' WHERE spotify_id = ? ORDER BY rated_on desc limit 10;', (album_id,)
    ).fetchall()

    rating_data = db.execute('SELECT COUNT(*) AS cnt, ROUND(AVG(rating),2) AS avg ' 
        ' FROM ratings r ' 
        ' WHERE spotify_id = ?;', (album_id,)
    ).fetchone()

    return render_template('album/index.html', album=album, ratings=ratings, rating_data=rating_data)


    