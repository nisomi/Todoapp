$(document).ready(function () {
    var menu = document.getElementById('myModalMenu');
    function handleResize() {
        var windowWidth = window.innerWidth;

        if (windowWidth < 850) {
            menu.style.left = windowWidth - 450 + 'px';
        } else {
            menu.style.left = 640 + 'px';
        }
    }

    window.addEventListener('resize', handleResize);
    window.addEventListener('load', handleResize);

    $("#staticBackdrop").on('show.bs.modal', function (event) {
    })

    $('.my_check span').click(function () {

        $('#myEditTask').modal("show");
        var id = $(this).data('source');
        var task = $(this).data('content');
        var day = $(this).data('day');
        $('#textInputEdit').val(task);
        $('#daySelectEdit').val(day);
        $('#textInputEdit').attr('taskID', id)
        console.log(id);
        console.log(task);
        console.log(day)
    });
    $('.my_check input[type="checkbox"]').on('click', function () {
        var spanElement = $(this).siblings('span');
        const tID = $(this).data('source');
        console.log(tID)
        let new_state
        if ($(this).is(':checked')) {
            new_state = 1
            spanElement.addClass('completed');
        } else {
            new_state = 0
            spanElement.removeClass('completed');
        }
        console.log(new_state)
        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    $('#saveBtn').click(function () {
        $.ajax({
            type: 'POST',
            url: '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'description': $('#textInput').val(),
                'day': $('#daySelect').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    $('#editBtn').click(function () {
        const tID = $('#textInputEdit').attr('taskID');
        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'description': $('#textInputEdit').val(),
                'day': $('#daySelectEdit').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    $('#deleteBtn').click(function () {
        const remove = $('#textInputEdit').attr('taskID');
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove,
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

})