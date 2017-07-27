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

  function check_notification_count() {
    $.ajax({
      url: '/messages/notification/count/',
      type: 'GET',
      dataType: 'json',
      cache: false,
      success: function (data) {
        if (data != "0")
          $(".notification-badge").html(data).show();
        else
          $(".notification-badge").hide();
      },
      complete: function () {
        window.setTimeout(check_notification_count, 60000);
      }
    });
  };
  check_notification_count();

  $("#notifications-dropdown").on('click', function (e) {
    e.preventDefault();
    $.ajax({
      url: '/messages/notification/count/',
      type: 'POST',
      success: function (data) {
        $(".notification-badge").hide().html("0");
      }
    });
  });
});