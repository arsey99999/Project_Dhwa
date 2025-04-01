from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_dhwa():
    return 'Hello, dhwa!'

@bp.route('/')
def index():
    return redirect(url_for('dhwa_list._list'))

@bp.route('/login')
def auth_views():
    return render_template('auth/login.html', form = form)

@bp.route('/mypage')
def mypage_views():
    return render_template('mypage/mypage.html', form = form)