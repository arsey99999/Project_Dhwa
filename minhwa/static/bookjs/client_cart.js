// 전체 선택 / 해제 기능
document.getElementById('select-all').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('.dhwa-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = this.checked);
});

// 선택된 항목 삭제
document.getElementById("delete-selected").addEventListener("click", function() {
    let selectedIds = [];
    document.querySelectorAll(".dhwa-checkbox:checked").forEach(function(checkbox) {
        selectedIds.push(checkbox.getAttribute("data-id"));
    });

    if (selectedIds.length > 0) {
        // 선택된 아이디들을 폼에 추가
        document.getElementById("deleteIds").value = selectedIds.join(",");
        
        // 폼 제출
        document.getElementById("deleteItemsForm").submit();
    } else {
        alert("삭제할 항목을 선택해 주세요.");
    }
});


// 선택된 항목 대여
document.getElementById('rent-selected').addEventListener('click', function() {
    const selectedIds = getSelectedIds();
    
    if (selectedIds.length === 0) {
        alert('대여할 항목이 선택되지 않았습니다.');
        return; 
    }

    const userConfirmed = confirm("선택한 항목을 대여하시겠습니까?");
    if (!userConfirmed) return; 

    document.getElementById('rentIds').value = selectedIds.join(','); 
    document.getElementById('rentItemsForm').submit(); 

    alert('대여가 완료되었습니다.');
});

// 선택된 항목 대여
document.getElementById("rent-selected").addEventListener("click", function() {
    let selectedIds = [];
    document.querySelectorAll(".dhwa-checkbox:checked").forEach(function(checkbox) {
        selectedIds.push(checkbox.getAttribute("data-id"));
    });

    if (selectedIds.length > 0) {
        // 선택된 아이디들을 폼에 추가
        document.getElementById("rentIds").value = selectedIds.join(",");
        
        // 폼 제출
        document.getElementById("rentItemsForm").submit();
    } else {
        alert("삭제할 항목을 선택해 주세요.");
    }
});

// 선택된 체크박스의 ID 가져오기
function getSelectedIds() {
    const checkboxes = document.querySelectorAll('.dhwa-checkbox:checked');
    const ids = Array.from(checkboxes).map(checkbox => checkbox.value);
    return ids;
}


