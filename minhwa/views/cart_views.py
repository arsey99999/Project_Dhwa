from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash, g, session
from .. import db 
from minhwa.models import DHWALIST, DHWACART, DHWAUSER
from sqlalchemy import func
from .auth_views import login_required
from datetime import datetime, timedelta

# 블루프린트 설정
bp = Blueprint('cart', __name__, url_prefix='/cart')

# 장바구니 페이지 렌더링
@bp.route('/client_cart')
def client_cart():
    user_id = session.get('user_id')  # 현재 로그인한 사용자 ID 가져오기

    if not user_id:  # 로그인하지 않았으면 로그인 페이지로 리디렉션
        flash('로그인 후 이용할 수 있습니다.', 'error')
        return redirect(url_for('auth.login'))
    
    user = DHWAUSER.query.get(user_id)  # 로그인한 사용자 정보 가져오기
    if not user:
        flash('사용자 정보를 찾을 수 없습니다.', 'error')
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', type=int, default=1)  # 페이징
    
    # 로그인한 사용자의 장바구니 목록만 가져오기
    dhwa_cart = DHWACART.query.filter_by(username=user.username).order_by(DHWACART.id.desc()).paginate(page=page, per_page=8)
    
    return render_template('cart/client_cart.html', dhwa_cart=dhwa_cart, active_tab='cart')

# 장바구니에 상품 추가
@bp.route('/add_to_cart/<int:dhwa_id>', methods=['POST'])
def add_to_cart(dhwa_id):
    dhwa_list = DHWALIST.query.get_or_404(dhwa_id)
    user_id = session.get('user_id')  # 로그인한 사용자의 ID

    if not user_id:
        # 현재 페이지 URL을 세션에 저장
        session['next_url'] = request.referrer  
        return redirect(url_for('auth.login'))
        
    user = DHWAUSER.query.get(user_id)
    if not user:
        flash('사용자 정보를 찾을 수 없습니다.')
        return redirect(url_for('auth.login'))
    
    # 도서 정보 가져오기
    dhwa = DHWALIST.query.get_or_404(dhwa_id)
    
    # 요청에서 수량 가져오기
    quantity = int(request.form.get('quantity', 1))  
    if quantity < 1:
        flash('수량은 1 이상이어야 합니다.', 'error')
        return redirect(url_for('cart.client_cart'))

    # 이미 장바구니에 같은 도서가 있는지 확인
    cart_item = DHWACART.query.filter_by(username=user.username, list_id=dhwa_id).first()
    
    if cart_item:  # 이미 있는 경우 수량 추가
        cart_item.amount += quantity
    else:  # 없는 경우 새로 추가
        new_cart_item = DHWACART(
            list_id=dhwa.list_id,
            username=user.username,
            subject=dhwa.subject,
            writer=dhwa.writer,
            publi=dhwa.publi,
            amount=quantity  # 선택한 수량만큼 추가
        )
        db.session.add(new_cart_item)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"오류가 발생했습니다: {str(e)}", 'error')
    
    return redirect(url_for('cart.client_cart'))


# 장바구니에서 선택된 항목 삭제
@bp.route('/delete', methods=['POST'])
def delete():
    cart_ids = request.form.get('ids')  # 여러 개의 ID 가져오기
    if not cart_ids:
        return redirect(url_for('cart.client_cart'))
    
    try:
        ids = cart_ids.split(',')  # cart_ids를 리스트로 변환
        for cart_id in ids:
            cart_item = DHWACART.query.get_or_404(cart_id)
            db.session.delete(cart_item)  # 항목 삭제
        db.session.commit()  # 변경 사항 저장
    except Exception as e:
        db.session.rollback()
        flash(f'삭제 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('cart.client_cart'))

@bp.route('/delete_item/<int:cart_id>', methods=['POST'])
def delete_item(cart_id):
    try:
        cart_item = DHWACART.query.get_or_404(cart_id)
        db.session.delete(cart_item)  # 개별 항목 삭제
        db.session.commit()  # 변경 사항 저장
    except Exception as e:
        db.session.rollback()
    
    return redirect(url_for('cart.client_cart'))

@bp.route('/modify/<int:cart_id>', methods=['POST'])
def client_modify(cart_id):
    try:
        new_amount = int(request.form.get('amount', 1))
        if new_amount < 1:
            return redirect(url_for('cart.client_cart'))
        
        cart_item = DHWACART.query.get_or_404(cart_id)
        cart_item.amount = new_amount
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    
    return redirect(url_for('cart.client_cart'))
    

# 장바구니 항목 대여
@bp.route('/rent_selected', methods=['POST'])
def rent_selected():
    user_id = session.get('user_id')  # 현재 로그인한 사용자 ID 가져오기
    item_ids = request.form.getlist('dhwa_id')  # 선택된 항목의 ID 목록 가져오기
    
    if not item_ids:  # 항목이 선택되지 않았을 때 경고 메시지 출력

        return redirect(url_for('cart.client_cart'))
    
    try:
        for item_id in item_ids:  
            cart_item = DHWACART.query.filter_by(id=item_id, username=user_id).first()  # 사용자의 장바구니 항목 중 선택된 항목 찾기
            if cart_item:  # 항목이 존재하면 대여 정보 업데이트
                cart_item.rent_date = datetime.now()  # 대여 날짜 현재 시간으로 설정
                cart_item.return_date = datetime.now() + timedelta(days=7)  # 반납일
                
        db.session.commit()  
        flash('선택된 항목이 성공적으로 대여되었습니다.', 'success')
    except Exception as e:
        db.session.rollback()  
        flash('대여 처리 중 오류가 발생했습니다.', 'error')
    
    return redirect(url_for('cart.client_cart'))  # 장바구니 페이지로 리디렉션

 
#관리자 화면(유저 목록)
@bp.route('/admin_cart_users', methods=['GET'])
@login_required
def admin_cart_users():
    page = request.args.get('page', 1, type=int)
    aduser = DHWAUSER.query.order_by(DHWAUSER.username).paginate(page=page)
    adcart = DHWACART.query.all()
    
    
      
    return render_template('cart/admin_cart_users.html', aduser=aduser, adcart=adcart)

#관리자화면(개인 카트 목록)
@bp.route('/admin_cart/<int:adlist_id>/', methods=['GET'])
@login_required
def admin_cart(adlist_id):
    page = request.args.get('page', 1, type=int)
    uname = DHWAUSER.query.get(adlist_id).username
    uscart = DHWACART.query.all()
    aduser = DHWAUSER.query.order_by(DHWAUSER.username).paginate(page=page)
    
    
    return render_template('cart/admin_cart.html', uscart=uscart,uname=uname, aduser=aduser)  


@bp.route('/admin_modify/<int:ucart_id>', methods=['GET','POST'])
@login_required
def admin_modify(ucart_id):
    if request.method == "POST":
        a = DHWACART.query.get_or_404(ucart_id)
        a.amount = int(request.form['ucart_amount'])
        db.session.commit()
        flash('수량이 수정 되었습니다.')
    return redirect(url_for('cart.admin_cart_users'))


@bp.route('/admin_delete/<int:ucart_id>', methods=['GET','POST'])
@login_required
def admin_delete(ucart_id):
    d = DHWACART.query.get(ucart_id)
    if g.user.username == 'admin':
        db.session.delete(d)
        db.session.commit()
        flash('선택한 항목이 삭제되었습니다.')
        return redirect(url_for('cart.admin_cart_users'))

@bp.route('/admin_delete_all/<uname>', methods=['GET','POST'])
@login_required
def admin_delete_all(uname):
    dcart = DHWACART.query.all()
    delname = uname
    if g.user.username == 'admin':
        for delcart in dcart:
            if delcart.username == delname:
                db.session.delete(delcart)
                db.session.commit()
                flash('선택한 항목이 삭제되었습니다.')
    return redirect(url_for('cart.admin_cart_users'))


@bp.route('/admin_cart_search', methods=['GET'])
def admin_cart_search():
    """카트 검색"""
    query = request.args.get('q', '').lower()
    page = request.args.get('page', 1, type=int)
    
    # 검색어에서 공백을 제거
    query_clean = query.replace(' ', '')  # 사용자 검색어에서 공백 제거

    # 공백을 제거한 검색어로 제목, 저자, 출판사에서 검색
    if query_clean:
        dhwa_cart = DHWACART.query.filter(
            func.replace(DHWACART.subject, ' ', '').ilike(f'%{query_clean}%') |
            func.replace(DHWACART.writer, ' ', '').ilike(f'%{query_clean}%') |
            func.replace(DHWACART.username, ' ', '').ilike(f'%{query_clean}%')
            ).paginate(page=page, per_page=10)
        dhwa_user = DHWAUSER.query.all()
    else:
        
        return redirect(url_for('cart.admin_cart_users'))
    
    return render_template('cart/admin_cart_search.html', dhwa_cart=dhwa_cart, dhwa_user=dhwa_user, query=query)


@bp.route('/admin_user_search', methods=['GET'])
def admin_user_search():
    """유저 검색"""
    query = request.args.get('q', '').lower()
    page = request.args.get('page', 1, type=int)
    
    # 검색어에서 공백을 제거
    query_clean = query.replace(' ', '')  # 사용자 검색어에서 공백 제거

    # 공백을 제거한 검색어로 제목, 저자, 출판사에서 검색
    if query_clean:
        dhwa_cart = DHWAUSER.query.filter(
            func.replace(DHWAUSER.username, ' ', '').ilike(f'%{query_clean}%')).paginate(page=page, per_page=10)
    else:
        
        return redirect(url_for('cart.admin_cart_users'))
    
    return render_template('cart/admin_cart_search.html', dhwa_cart=dhwa_cart, query=query)