from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from minhwa import db
from minhwa.models import DHWALIST, DHWAUSER  # 모델 임포트
from sqlalchemy import func
import os  # 파일 경로 설정에 필요한 os 모듈
import uuid  # 파일명 중복 방지를 위한 uuid 모듈


# Blueprint 정의
bp = Blueprint('dhwa_list', __name__, url_prefix='/dhwa_list')

@bp.route('/')
def _list():
    """메인 도서 목록 페이지"""
    # 페이지 번호 가져오기
    page = request.args.get('page', 1, type=int)
    
    # 도서 목록 가져오기 (최신순 정렬)
    dhwa_list = DHWALIST.query.order_by(DHWALIST.list_id.desc()).paginate(page=page, per_page=9)
    
    return render_template('list/dhwa_list.html', dhwa_list=dhwa_list)

@bp.route('/dhwa_detail/<int:dhwa_id>/')
def detail(dhwa_id):
    """도서 상세 보기"""
    dhwa = DHWALIST.query.get_or_404(dhwa_id)
    return render_template('list/dhwa_detail.html', dhwa=dhwa)

@bp.route('/admin_book', methods=['GET'])
def book():
    """관리 페이지 (장바구니, 회원 관리, 상품 관리 탭 포함 + 관리자 확인)"""
    # 관리자 확인
    admin_user_id = session.get('user_id')  # 세션에서 user_id 가져오기
    if not admin_user_id:
        flash('로그인이 필요한 페이지입니다.')
        return redirect(url_for('auth.login'))

    admin_user = DHWAUSER.query.get(admin_user_id)  # 사용자 정보 조회
    if admin_user.username != 'admin':
        flash('상품 관리 페이지는 관리자만 접속할 수 있습니다.')
        return redirect(url_for('auth.login'))

    # 페이지 번호와 검색어 가져오기
    page = request.args.get('page', 1, type=int)
    per_page = 8  # 한 페이지당 표시할 항목 수
    active_tab = request.args.get('active_tab', 'books')  # 기본 탭은 상품 관리
    query = request.args.get('q', '')  # 검색어 가져오기

    # 도서 목록 페이징 처리 및 검색어 반영
    if query:
        # 검색어에서 공백을 제거하여 쿼리로 필터링
        query_clean = query.replace(' ', '')  # 공백 제거
        dhwa_list = DHWALIST.query.filter(
            func.replace(DHWALIST.subject, ' ', '').ilike(f'%{query_clean}%') |
            func.replace(DHWALIST.writer, ' ', '').ilike(f'%{query_clean}%') |
            func.replace(DHWALIST.publi, ' ', '').ilike(f'%{query_clean}%')
        ).paginate(page=page, per_page=per_page)
    else:
        # 검색어가 없을 경우 최신순으로 도서 목록을 반환
        dhwa_list = DHWALIST.query.order_by(DHWALIST.list_id.desc()).paginate(page=page, per_page=per_page, error_out=False)

    # 도서 관리 템플릿 렌더링
    return render_template(
        'list/admin_book.html',
        dhwa_list=dhwa_list,
        active_tab=active_tab,
        query=query  # 검색어를 템플릿에 전달
    )

@bp.route('/add_book/', methods=['POST'])
def add_book():
    """도서 등록"""
    # 폼 데이터 가져오기
    subject = request.form['subject']  # 책 제목
    writer = request.form['writer']  # 저자
    publi = request.form.get('publi')  # 출판사 (선택 입력)
    img_file = request.files.get('img')  # 업로드된 이미지 파일

    # 이미지 저장 처리
    filename = None
    if img_file and img_file.filename:  # 파일이 업로드된 경우만 처리
        # 고유 파일명 생성 (UUID 사용)
        filename = f"{uuid.uuid4().hex}_{img_file.filename}"
        
        # 파일 저장 경로 설정 (C:\projects\dhwa\minhwa\static\bookimg)
        upload_dir = os.path.join(current_app.root_path, 'static', 'bookimg')  # 프로젝트의 static 경로
        if not os.path.exists(upload_dir):  # 디렉토리가 없으면 생성
            os.makedirs(upload_dir)
        
        # 업로드된 파일 저장
        img_file.save(os.path.join(upload_dir, filename))

    # 데이터베이스에 저장 (파일명만 저장)
    new_book = DHWALIST(
        subject=subject,
        writer=writer,
        publi=publi,
        img=filename  # DB에는 파일명만 저장
    )
    db.session.add(new_book)
    db.session.commit()

    # 성공 메시지
    flash(f"{subject}이(가) 성공적으로 등록되었습니다.", "success")
    
    # 상품 관리 탭으로 리디렉트
    return redirect(url_for('dhwa_list.book', active_tab='books'))

@bp.route('/edit_book/<int:dhwa_id>/', methods=['POST'])
def edit_book(dhwa_id):
    """도서 수정"""
    # 수정할 도서 조회
    dhwa = DHWALIST.query.get_or_404(dhwa_id)

    # 폼 데이터 가져오기
    subject = request.form['subject']
    writer = request.form['writer']
    publi = request.form.get('publi')
    img_file = request.files.get('img')  # 업로드된 이미지 파일

    # 이미지 수정 처리
    if img_file and img_file.filename:  # 새로운 파일이 업로드된 경우
        # 고유 파일명 생성 (UUID 사용)
        filename = f"{uuid.uuid4().hex}_{img_file.filename}"

        # 파일 저장 경로 설정
        upload_dir = os.path.join(current_app.root_path, 'static', 'bookimg')
        if not os.path.exists(upload_dir):  # 디렉토리가 없으면 생성
            os.makedirs(upload_dir)

        # 기존 이미지 삭제 (필요시)
        if dhwa.img:
            old_file_path = os.path.join(upload_dir, dhwa.img)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        # 새로운 파일 저장
        img_file.save(os.path.join(upload_dir, filename))
        dhwa.img = filename  # DB에 새 파일명 업데이트

    # 텍스트 데이터 수정
    dhwa.subject = subject
    dhwa.writer = writer
    dhwa.publi = publi

    # 데이터베이스에 반영
    db.session.commit()

    # 성공 메시지
    flash(f"{dhwa.subject}이(가) 성공적으로 수정되었습니다.", "success")

    # 상품 관리 페이지로 리디렉트
    return redirect(url_for('dhwa_list.book', active_tab='books'))
    
@bp.route('/delete_books', methods=['POST'])
def delete_books():
    ids_to_delete = request.form.get('ids', '')  # 쉼표로 구분된 ID 문자열
    print("서버로 전달된 IDs:", ids_to_delete)  # 서버 로그 출력

    if not ids_to_delete:
        flash("삭제할 항목이 없습니다.", "error")
        return redirect(url_for('dhwa_list.book', active_tab='books'))

    try:
        id_list = [int(i) for i in ids_to_delete.split(',')]
        DHWALIST.query.filter(DHWALIST.list_id.in_(id_list)).delete(synchronize_session=False)
        db.session.commit()
        flash("선택한 항목이 삭제되었습니다.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"오류 발생: {e}", "error")

    return redirect(url_for('dhwa_list.book', active_tab='books'))

@bp.route('/search', methods=['GET'])
def search():
    """도서 검색"""
    query = request.args.get('q', '').lower()
    page = request.args.get('page', 1, type=int)
    
    # 검색어에서 공백을 제거
    query_clean = query.replace(' ', '')  # 사용자 검색어에서 공백 제거

    # 공백을 제거한 검색어로 제목, 저자, 출판사에서 검색
    if query_clean:
        dhwa_list = DHWALIST.query.filter(
            func.replace(DHWALIST.subject, ' ', '').ilike(f'%{query_clean}%') |
            func.replace(DHWALIST.writer, ' ', '').ilike(f'%{query_clean}%') |
            func.replace(DHWALIST.publi, ' ', '').ilike(f'%{query_clean}%')
        ).paginate(page=page, per_page=9)
    else:
        # 검색어가 없을 경우 최신순으로 도서 목록을 반환
        dhwa_list = DHWALIST.query.order_by(DHWALIST.list_id.desc()).paginate(page=page, per_page=9)
    
    return render_template('list/dhwa_list.html', dhwa_list=dhwa_list, query=query)     