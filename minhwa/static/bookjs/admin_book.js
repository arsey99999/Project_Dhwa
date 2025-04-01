// static/js/script.js

// 전체 선택 체크박스를 클릭했을 때
const selectAllCheckbox = document.getElementById("select-all");
if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener("change", function() {
        const checkboxes = document.querySelectorAll(".book-checkbox");
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = selectAllCheckbox.checked;  // 전체 선택 상태로 변경
        });
    });
}

// 각 개별 체크박스가 변경될 때 전체 선택 체크박스 상태 업데이트
const bookCheckboxes = document.querySelectorAll(".book-checkbox");
if (bookCheckboxes) {
    bookCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener("change", function() {
            const checkboxes = document.querySelectorAll(".book-checkbox");
            const allChecked = Array.from(checkboxes).every(function(cb) {
                return cb.checked;
            });

            // 전체 선택 체크박스 상태 업데이트 (모두 선택된 경우 체크, 아니면 해제)
            selectAllCheckbox.checked = allChecked;

            // 일부만 선택된 경우, 전체 선택 체크박스를 부분 선택 상태로 설정
            selectAllCheckbox.indeterminate = !allChecked && Array.from(checkboxes).some(function(cb) {
                return cb.checked;
            });
        });
    });
}

document.getElementById("book_delete-selected").addEventListener("click", function(event) {
    // 확인 메시지 표시
    if (confirm('선택한 항목을 정말로 삭제하시겠습니까?')) {
        let selectedIds = [];
        
        // 선택된 항목 체크박스를 가져와서 id들을 selectedIds 배열에 추가
        document.querySelectorAll(".book-checkbox:checked").forEach(function(checkbox) {
            selectedIds.push(checkbox.getAttribute("data-id"));
        });

        if (selectedIds.length > 0) {
            // 선택된 아이디들을 폼에 추가
            document.getElementById("deleteIds").value = selectedIds.join(",");
            
            // 폼 제출
            document.getElementById("deleteBooksForm").submit();
        } else {
            alert("삭제할 항목을 선택해 주세요.");
        }
    } else {
        // 취소를 클릭하면 폼 제출을 막음
        event.preventDefault();  // preventDefault()로 기본 동작(폼 제출)을 막음
    }
}); 