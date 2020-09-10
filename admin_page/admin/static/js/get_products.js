function get_pr() {
    var getProducts = new XMLHttpRequest();
    $("#dataTable").change(function () {
        $.ajax({
            type: "GET",
            url: "{{url_for('dataLoad')}}",
            data: {
                table: $("#dataTable").val(),
            },
            success: function (data) {
                $("dataTable").html(data);
            },
        });
    });
}