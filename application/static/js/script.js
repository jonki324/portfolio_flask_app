$(function() {
    let pagetop = $('.pagetop');
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            pagetop.fadeIn();
        } else {
            pagetop.fadeOut();
        }
    });
    pagetop.on('click', function () {
        $('body, html').animate({ scrollTop: 0 }, 500);
        return false;
    });

    $('.drag-and-drop-area').on('click', function() {
        $('#file').click();
    });

    $('.drag-and-drop-area').on('mouseover', function() {
        $(this).removeClass('drag-and-drop-area-out');
        $(this).addClass('drag-and-drop-area-over');
    });

    $('.drag-and-drop-area').on('mouseout', function() {
        $(this).removeClass('drag-and-drop-area-over');
        $(this).addClass('drag-and-drop-area-out');
    });

    $('.drag-and-drop-area').on('dragover', function() {
        $(this).removeClass('drag-and-drop-area-out');
        $(this).addClass('drag-and-drop-area-over');
    });

    $('.drag-and-drop-area').on('dragleave', function() {
        $(this).removeClass('drag-and-drop-area-over');
        $(this).addClass('drag-and-drop-area-out');
    });

    $('#icon_del').on('change', function() {
        let chk = $(this).prop('checked');
        if (chk) {
            $('#preview_db').fadeOut();
        } else {
            $('.preview_in').remove();
            $('#file').val('');
            $('#preview_db').fadeIn();
        }
    });

    $('.drag-and-drop-area').on('drop', function(e) {
        e.stopPropagation();
        e.preventDefault();
        document.getElementById('file').files = e.originalEvent.dataTransfer.files;
        $('#file').change();
    })

    $('#file').on('change', function(e) {
        let file = e.target.files[0];
        let reader = new FileReader();

        if (typeof file == 'undefined' || file.type.indexOf("image") < 0) {
            return false;
        }

        reader.onload = (function(file) {
            return function(e) {
                $('#icon_del').prop('checked', true);
                $('#preview_db').hide();

                $('.preview_in').remove();

                $('#preview').append($('<img>').attr({
                    src: e.target.result,
                    class: "icon-prev preview_in"
                })).hide().fadeIn(1000);
            };
        })(file);

        reader.readAsDataURL(file);
    });

    $(document).on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    $(document).on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    $(document).on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
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