$(function() {
    $("#icon-dropzone").dropzone();
});

function addBookmarkPost(post_id) {
    let del_flg = $(`#del_flg_${post_id}`).val();
    del_flg = toBoolean(del_flg);

    let url = `${$SCRIPT_ROOT}bookmark/post/add`;
    if (del_flg) {
        url = `${$SCRIPT_ROOT}bookmark/post/rmv`;
    }

    let data = {
        'post_id': post_id,
        'csrf_token': $('#csrf_token').val()
    };

    $.ajax({
        url: url,
        type: 'POST',
        data: data
    }).done((data) => {
        $(`#bookmark_cnt_id_${post_id}`).html(data['bookmark_count']);
        $(`#del_flg_${post_id}`).val(data['del_flg']);
        toastr.success(data['msg']);
    }).fail((data) => {
        toastr.error('通信エラー');
    }).always((data) => {
        console.log(data);
    })
}

function addBookmarkUser(user_id) {
    let del_flg = $('#del_flg').val();
    del_flg = toBoolean(del_flg);

    let url = `${$SCRIPT_ROOT}bookmark/user/add`;
    if (del_flg) {
        url = `${$SCRIPT_ROOT}bookmark/user/rmv`;
    }

    let data = {
        'user_id': user_id,
        'csrf_token': $('#csrf_token').val()
    };

    $.ajax({
        url: url,
        type: 'POST',
        data: data
    }).done((data) => {
        $('#bookmark_cnt_id').html(data['bookmark_count']);
        $('#del_flg_').val(data['del_flg']);
        toastr.success(data['msg']);
    }).fail((data) => {
        toastr.error('通信エラー');
    }).always((data) => {
        console.log(data);
    })
}

function toBoolean(str) {
    return str.toLowerCase() === 'true';
}

function showModal(post_id) {
    let src_org = $(`#post-img-${post_id}`).attr('src');
    $('#postModalImg').attr('src', src_org);
    $('#postModal').modal('show');
}