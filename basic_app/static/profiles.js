$(function () {
    var currUserId;

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-profile").modal("show");
            },
            success: function (data) {

            }
        });
    };

    var saveForm = function () {
        var form = $(".js-profile-create-form").serializeArray();
        $.ajax({
            url: '/profiles/create/',
            data: form,
            type: 'POST',
            dataType: 'json',
            // // headers:  {
            //     'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            // },
            success: function (data) {
                if (data.form_is_valid) {
                    $("#profile-table tbody").html(data.html_profile_list);
                    $("#modal-profile").modal("hide");
                    dt_table.ajax.reload();
                }
                else {
                    $("#modal-profile .modal-content").html(data.html_form);
                }
            },error: function () {

            }
        });
        return false;
    };


    var updateProfile = function () {
        var form = $(".js-profile-create-form").serializeArray();
        // form.push({id: currUserId});
        form.push({name: "id", value: currUserId});
        $.ajax({
            url: '/profiles/',
            data: form,
            type: "POST",
            dataType: 'json',
            headers:  {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            },
            success: function (data) {
                $("#modal-profile").modal("hide");
                dt_table.ajax.reload();
            },
            error: function (data) {
                alert(data.responseJSON);
            }
        });
    };

+
    /* Binding */

    // Create profile

    $(".js-create-profile").on('click', function () {
        $("#modal-profile").modal("show");
        $(".confirm-btn").attr({
            id: "create-profile"
        }).text('Add profile')
            .on('click', saveForm);
        $("#profile-modal-header").text("Add new profile");
        $('.js-profile-create-form')[0].reset();
    });


    // $("#modal-profile").on("submit", ".js-profile-create-form", saveForm);

    // Update profile

    $('#MyTable').on('click', '.js-update-profile', function () {
        currUserId = $(this).parent('span').data('id');

        $(".confirm-btn").attr({
            id: "update-profile"
        }).text('Save')
            .on("click", updateProfile);
        $("#profile-modal-header").text("Edit profile");
        $('.js-profile-create-form')[0].reset();


        $.ajax({
            url: '/profiles/',
            data: {
                'pk': currUserId
            },
            type: 'GET',
            dataType:'json',
            headers:  {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            },
            success: function (data) {
                $("#modal-profile").modal("show");
                $("#profile-modal-header").text("Edit profile");
                $("#profile-save-btn").text("Save edited profile");
                for (var key in data) {
                    $("#id_"+ key).val(data[key]);

                }
            },
            error: function (data) {
                alert('Error');
            }
        });
    });
});


$("#import_csv").on("click", function(){
    $("#import_form").submit();
});


function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
