$(function () {
      function fetch_latest () {
        var $sendMessage = $('.send-message');
        var userId = $('#conversation_user').val();

        $.ajax({
          url: '/messages/latest',
          cache: false,
          data: {
            'from_user': userId
          },
          success: function (data) {
            if (data.message) {
              $sendMessage.before("<li class='message'><img src='" + data.picture + "' class='picture'>" +
                                    "<div>" +
                                      "<h5>" +
                                        "<small class='pull-right'>" +
                                          data.date + 
                                        "</small>" +
                                        "<a href='#'>" +
                                          data.user + 
                                        "</a>" +
                                      "</h5>" +
                                        data.message +
                                    "</div></li>");
              $.ajax({
                url: '/messages/latest/',
                data: {
                  'from_user': userId,
                  'is_read': true,
                }
              });
            }
          },
          complete: function () {
            window.setTimeout(fetch_latest, 1000);
          }
        });
      }
      fetch_latest();
    });