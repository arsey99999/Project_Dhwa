# 동화책 대여 서비스 (Dhwa Project)

동화에서 D를 본따 D-Hwa로 프로젝트명을 정하였습니다.  
아이들을 위한 동화책을 대여할 수 있는 Flask 기반 웹 프로젝트입니다.  
이미지 기반 도서 등록, 장바구니, 회원가입/로그인, 관리자 기능을 포함합니다.

---

## 주요 기능
- 도서 목록 및 검색
- 장바구니 기능
- 상품페이지, 관리자 도서 관리 페이지 (my role)
- SQLite 기반 DB + Flask-Migrate

---

## Skill & Tools
- Python, Flask
- HTML, CSS, JS
- VSCode, GitHub, DB Browser for SQLite

---

## ER Diagram  
<img src="README/ER Diagram.png" alt="ER Diagram" width="700"/>

## Usecase Diagram  
<img src="README/Usecase Diagram.png" alt="Usecase Diagram" width="700"/>

---

## Screen View

### 메인페이지 (웹)
<img src="README/메인페이지.png" alt="메인페이지" width="600"/>

### 메인페이지 (모바일)
<img src="README/메인페이지(모바일).png" alt="모바일 메인페이지" width="300"/>

### 상품관리 페이지
<img src="README/상품관리페이지.png" alt="상품관리페이지" width="600"/>

---

## 실행 방법

```bash
# 가상환경 활성화
venv\Scripts\activate

# 서버 실행
flask run
