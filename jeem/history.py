from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from jeem.auth import login_required
from jeem.db import get_db

bp = Blueprint('history', __name__)
@bp.route('/history')
def index():
    db = get_db()
    generations = db.execute(
        'SELECT g.generated_on, a.id, a.album_name, a.band_name, r.rating, r.rated_on ' \
        'FROM generations g ' \
        'LEFT JOIN albums a ' \
        'ON g.album_id = a.id ' \
        'LEFT JOIN ratings r ' \
        'ON r.album_id = a.id ' \
        'ORDER BY g.generated_on desc ' \
        'LIMIT 10 ' 
    ).fetchall()
    return render_template('history/index.html', generations=generations)
