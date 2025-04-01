from flask import Blueprint, url_for, render_template, flash, request, session, g, current_app, app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools

from minhwa import db
from minhwa.forms import UserLoginForm, UserCreateForm, UpdateForm
from minhwa.models import DHWAUSER

from datetime import timedelta, datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        print("Before validation:", dict(session))  # 세션 상태 확인
        error = None
        user = DHWAUSER.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()  # 세션 초기화
            session['user_id'] = user.id  # 로그인한 사용자 정보를 세션에 저장
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=1)
            return redirect(url_for('dhwa_list._list'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()  # 세션 초기화
    session.pop('user_id', None)
    session.permanent = False 
    app.permanent_session_lifetime = timedelta(seconds=0)
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('auth.login'))



@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = DHWAUSER.query.filter_by(username=form.username.data).first()
        email = DHWAUSER.query.filter_by(email=form.email.data).first()
        
        if user or email:
            flash('이미 사용 중인 사용자 ID 또는 이메일입니다.')
        
        elif not user:
            user = DHWAUSER(username=form.username.data,
                            password=generate_password_hash(form.password1.data),
                            tell=form.tell.data,
                            email=form.email.data,
                            address=form.address.data,
                            postcode=form.postcode.data)
            db.session.add(user)
            db.session.commit()
            if g.user and g.user.username == 'admin':
                return redirect(url_for('auth.select_users'))
        return redirect(url_for('auth.login'))        

    return render_template('auth/signup.html', form=form)

@bp.route('/admin_users/')
def select_users(): 
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('q', type=str, default='') 

    query = DHWAUSER.query.order_by(DHWAUSER.id.desc())

    if kw:
        search = f"%{kw}%"
        query = query.filter(
            (DHWAUSER.username.ilike(search)) | 
            (DHWAUSER.email.ilike(search)) |
            (DHWAUSER.tell.ilike(search))
        )

    admin_users = query.paginate(page=page, per_page=8)

    admin_user_id = session.get('user_id')

    if not admin_user_id:
        flash('로그인이 필요한 페이지입니다.')
        return redirect(url_for('auth.login'))

    admin_user = DHWAUSER.query.get(admin_user_id)

    if admin_user.username != 'admin':
        flash('회원 관리 페이지는 관리자만 접속할 수 있습니다.')
        return redirect(url_for('auth.login'))
        
        
    return render_template('auth/admin_users.html', admin_users=admin_users, kw=kw)



@bp.route('/admin_user_delete/<int:user_id>')
def admin_delete_user(user_id):
    user_delete = DHWAUSER.query.get_or_404(user_id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("회원 정보 삭제 중 오류가 발생했습니다: {}".format(str(e)), "danger")
    
    return redirect(url_for('auth.select_users'))

