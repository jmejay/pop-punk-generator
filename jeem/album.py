from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from jeem.auth import login_required
from jeem.db import get_db

bp = Blueprint('album', __name__)

@bp.route('/album')
def index():
    db = get_db()
    albums = db.execute(
        'SELECT *'
        'FROM albums ORDER BY RANDOM() limit 1;'
    ).fetchall()
    return render_template('album/index.html', albums=albums)