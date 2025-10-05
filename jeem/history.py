from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from jeem.auth import login_required
from jeem.db import get_db

bp = Blueprint('history', __name__)
@bp.route('/history')
def index():
    username = session.get('username')
    db = get_db()
    generations = db.execute(
        'SELECT MAX(g.generated_on) as generated_on, a.id, a.album_name, a.band_name, r.rating, r.rated_on ' \
        'FROM generations g ' \
        'LEFT JOIN albums a ' \
        'ON g.album_id = a.id ' \
        'LEFT JOIN ratings r ' \
        'ON r.album_id = a.id ' \
        'WHERE g.generated_on = (SELECT MAX(generated_on) from generations WHERE user_id = ? AND album_id = a.id) ' \
        'AND g.user_id = ? ' \
        'GROUP BY a.id, a.album_name, a.band_name, r.rating, r.rated_on '
        'ORDER BY g.generated_on desc ' \
        'LIMIT 10 ',
        (session['user_id'],session['user_id'],)
    ).fetchall()
    allgen = db.execute(
        'SELECT MAX(g.generated_on) as generated_on, a.id, a.album_name, a.band_name, r.rating, r.rated_on, u.username ' \
        'FROM generations g ' \
        'LEFT JOIN albums a ' \
        'ON g.album_id = a.id ' \
        'LEFT JOIN ratings r ' \
        'ON r.album_id = a.id ' \
        'LEFT JOIN user u ' \
        'ON g.user_id = u.id ' \
        'WHERE g.generated_on = (SELECT MAX(generated_on) from generations WHERE user_id <> ? AND album_id = a.id) ' \
        'AND g.user_id <> ? ' \
        'GROUP BY a.id, a.album_name, a.band_name, r.rating, r.rated_on '
        'ORDER BY g.generated_on desc ' \
        'LIMIT 10 ',
        (session['user_id'],session['user_id'],)
    ).fetchall()
    return render_template('history/index.html', generations=generations, allgen=allgen, username=username)


