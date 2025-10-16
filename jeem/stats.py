from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from jeem.auth import login_required
from jeem.db import get_db

bp = Blueprint('stats', __name__)


@bp.route('/stats')
def index():
    #username = session.get('username')
    db = get_db()

    favourites = db.execute(
        '''select 
            a.band_name,
            ROUND(AVG(r.rating),2) AS "average",
            COUNT(*) AS "ratings",
            AVG(r.rating) / 5  AS sort
        from ratings r 
        left join user u 
        on r.user_id = u.id 
        left join albums a 
        on r.spotify_id  = a.album_id
        where 1=1
        and u.id = ? 
        group by a.band_name
        --having count(*) > 1 
        order by 4 desc 
        limit 15;''',
        (session['user_id'],)
    ).fetchall()

    hated = db.execute(
        '''select 
            a.band_name,
            ROUND(AVG(r.rating),2) AS "average",
            COUNT(*) AS "ratings",
            AVG(r.rating) / 5  AS sort
        from ratings r 
        left join user u 
        on r.user_id = u.id 
        left join albums a 
        on r.spotify_id  = a.album_id
        where 1=1
        and u.id = ? 
        group by a.band_name
        --having count(*) > 1 
        order by 4 
        limit 15;''',
        (session['user_id'],)
    ).fetchall()

    completed = db.execute(
    '''
    select 
        count(*) AS "total",
        count(r.id) AS "rated",
        round((count(r.album_id) * 1.0 / count(*)) * 100, 1) as  "percent",
        a.band_genre 
    from albums a
    left join ratings r 
    on a.album_id = r.spotify_id 
    and r.user_id = ?
    where 1=1
    and a.band_genre <> ''
    group by a.band_genre 
    having count(r.album_id) > 5
    order by 2 desc 
    ''',
    (session['user_id'],)
    ).fetchall()

    user_ratings = db.execute(
    '''
    select 
    count(*) AS "Total Ratings",
    ROUND(avg(r.rating),1) AS "Average Rating",
    u.username 
    from ratings r 
    left join "user" u 
    on r.user_id  = u.id
    group by u.username
    order by 1 desc 
    ''',
    ).fetchall()
    
    return render_template('stats/index.html', favourites=favourites, completed=completed, hated=hated, user_ratings=user_ratings)

