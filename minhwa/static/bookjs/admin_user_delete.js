const admin_delete_user = document.getElementsByClassName('admin_delete_user');

Array.from(admin_delete_user).forEach(function(element) {
    element.addEventListener('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = this.dataset.uri;
        };
    });
});

const modal_btn = document.getElementsByClassName('modal_show_btn');











