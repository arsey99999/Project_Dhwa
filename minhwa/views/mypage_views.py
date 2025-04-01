from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from minhwa.forms import UpdateForm
from minhwa.models import DHWAUSER
from minhwa import db
from werkzeug.security import generate_password_hash

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

# 세션에서 로그인된 사용자 정보를 로드
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id:
        g.user = DHWAUSER.query.get(user_id)
    else:
        g.user = None

@bp.route('/mypage/', methods=['GET'])
def mypage():
    if g.user:
        # 탭에 따라 페이지 제목을 변경합니다.
        active_tab = request.args.get('tab', 'profile')  # 기본값은 'profile'
        
       
        
        return render_template('mypage/mypage.html', user=g.user, active_tab=active_tab)
    
    flash('로그인이 필요합니다.')
    return redirect(url_for('auth.login'))

@bp.route('/update_mypage/', methods=['GET', 'POST'])
def update_mypage():
    if g.user is None:
        flash('로그인이 필요합니다.')
        return redirect(url_for('auth.login'))

    form = UpdateForm(obj=g.user)

    if request.method == 'POST' and form.validate_on_submit():
        g.user.username = form.username.data
        
        # 비밀번호가 수정된 경우에만 해시 처리
        if form.password.data:
            g.user.password = generate_password_hash(form.password.data)  # 비밀번호 해시화
        
        g.user.email = form.email.data
        g.user.tell = form.tell.data
        g.user.address = form.address.data
        g.user.postcode = form.postcode.data
        db.session.commit()
        flash('회원 정보가 수정되었습니다.', 'success')  # 정보 수정 후 성공 메시지
        return redirect(url_for('mypage.mypage'))

    return render_template('mypage/update_mypage.html', form=form)

@bp.route('/cancel_update/')
def cancel_update():
    flash('회원 정보 수정이 취소가 되었습니다.', 'warning')
    return redirect(url_for('mypage.mypage'))

@bp.route('/delete/', methods=['POST'])
def delete_mypage():
    if g.user is None:
        flash('로그인이 필요합니다.')
        return redirect(url_for('auth.login'))

    try:
        db.session.delete(g.user)  # 사용자 삭제
        db.session.commit()  # 변경 사항 커밋
        session.pop('user_id', None)  # 세션에서 사용자 정보 삭제
        g.user = None
        flash('회원 탈퇴 되었습니다. 그동안 이용해 주셔서 감사합니다.', 'danger')
        return redirect(url_for('auth.login'))
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        flash(f'탈퇴 처리 중 오류가 발생했습니다: {e}', 'danger')
        return redirect(url_for('mypage.mypage'))
