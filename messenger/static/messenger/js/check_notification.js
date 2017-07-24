$(function () {
  function check_notification() {
    $.ajax({
      url: '/messages/notification/',
      type: 'GET',
      cache: false,
      success: function (data) {
        $("#notifications").html(data);
      },
      complete: function () {
        window.setTimeout(check_notification, 60000);
      }
    });
  };
  check_notification();
});