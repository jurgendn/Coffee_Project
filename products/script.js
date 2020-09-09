function get_id(click_id) {
  return click_id;
}

var prd_id = get_id(click_id);

$(document).ready(function () {
  $("#{0}".replace("{0}", prd_id)).click(function () {
    var prd = $("#word").val();
    $.ajax({
      url: "/asb",
      type: "post",
      success: function (response) {
        $("#wordResult").html(response.html);
      },
      error: function (xhr) {
        //Do Something to handle error
      },
    });
  });
});
