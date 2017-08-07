var dt_table;


$(document).ready(function() {
    DrawColumnFilter();
    dt_table = $('.datatable').DataTable({
        dom: '<"top">rt<"bottom"lp><"clear">',
        language: dt_language,  // global variable defined in html
        order: [[ 0, "desc" ]],
        lengthMenu: [[10, 25, 50, 100, 200], [10, 25, 50, 100, 200]],
        columnDefs: [
            {
                orderable: true,
                searchable: true,
                className: "center",
                targets: [-1],
                "mRender": function(data, type, full) {

                    return '<span data-id="'+full[8]+'"><button type="button" class="btn btn-warning btn-sm js-update-profile">' + '<span class="glyphicon glyphicon-pencil"></span> Edit </button> / ' +
                        '<button type="button" class="btn btn-danger btn-sm js-delete-profile"><span class="glyphicon glyphicon-trash"></span> Delete </button></span>';
                }
            },
            {
                bSortable: false,
                aTargets: [ 0,1,2,3,4,5,6,8]
            }
        ],
        initComplete: function () {


        },
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        sAjaxSource: USERS_LIST_JSON_URL
    });
    $('#MyTable').on( 'draw.dt', function () {


        $('#MyTable thead th:nth-last-child(1)').removeClass('sorting');


    });
});
function DrawColumnFilter() {
    var selectedVal = {city: '', country: ''};
    $.ajax({
        url:'table_sort',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if (data.city) {
                var selectFilterByCity = $('#city_filter').on('change', function () {
                    selectedVal.city = $('#city_filter').val();
                    dt_table.columns([2]).search(selectedVal.city).draw();
                });

                selectFilterByCity.empty().append('<option value=""></option>');

                for(var index in data.city) {
                    if (data.city[index]){
                        selectFilterByCity.append('<option>' + data.city[index] + '</option>');
                    }
                }
            }

            if (data.country) {
                var selectFilterByCountry = $('#country_filter').on('change', function () {
                    dt_table.columns([3]).search($('#country_filter').val()).draw();
                });

                selectFilterByCountry.empty().append('<option value=""></option>');

                for(var index in data.country) {
                    if (data.country[index]){
                        selectFilterByCountry.append('<option>' + data.country[index] + '</option>');
                    }

                }
            }

        }
    })
}

