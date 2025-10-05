from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from jeem.auth import login_required
from jeem.db import get_db

import random

bp = Blueprint('album', __name__)

@bp.route('/album')
@bp.route('/album/<int:album_id>', methods=('GET', 'POST'))

@login_required
def index(album_id=None):

    db = get_db()
    random_album_id = None

    # If no album_id provided, redirect to a random album
    if album_id is None:
        album_count = db.execute('SELECT COUNT(*) AS count FROM albums').fetchone()
        random_album_id = random.randint(1, album_count['count'])
        return redirect(url_for('album.index', album_id=random_album_id))
    else:
        random_album_id = album_id
    
    album = db.execute('SELECT * FROM albums WHERE id = ? LIMIT 1;', (album_id,)).fetchone()

    
    if album is None:
        abort(404, f"Album id {album_id} doesn't exist.")
    else:
        db.execute('INSERT INTO generations (user_id, album_id) VALUES (?,?)',
                   (session['user_id'], album_id))
        db.commit()
    

    if request.method == 'POST':
        rating = request.form['rating']
        error = None

        if error is not None:
            flash(error)
        else: 
            db.execute(
                'INSERT INTO ratings (user_id, album_id, rating)'
                'VALUES (?, ?, ?)',
                (session['user_id'], album_id, rating)
            )
            db.commit()
            db.execute(
                '''
                DELETE FROM ratings
                WHERE id NOT IN (
                    SELECT id FROM ratings WHERE album_id = (?) AND user_id = (?) ORDER BY rated_on desc LIMIT 1 
                )
                AND album_id = (?)
                AND user_id = (?)
                ''',
                (random_album_id, session['user_id'], random_album_id, session['user_id'])
            )
            db.commit()
            return redirect(url_for('album.index', album_id=random_album_id))
        
        



    ratings = db.execute('SELECT * '
        ' FROM ratings r '
        ' LEFT JOIN user u ON r.user_id = u.id '
        ' WHERE album_id = ? ORDER BY rated_on desc limit 10;', (album_id,)
    ).fetchall()

    rating_data = db.execute('SELECT COUNT(*) AS cnt, ROUND(AVG(rating),2) AS avg ' 
        ' FROM ratings r ' 
        ' WHERE album_id = ?;', (album_id,)
    ).fetchone()

    return render_template('album/index.html', album=album, ratings=ratings, rating_data=rating_data)


    