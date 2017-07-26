$(function () {
      function fetch_latest () {
        var $conversation = $('.conversation');
        var userId = $('#conversation_user').val();

        $.ajax({
          url: '/messages/latest',
          cache: false,
          data: {
            'from_user': userId
          },
          success: function (data) {
            var message_recieved = false;
            if (data) {
              $conversation.append(data);

              $conversation.stop().animate({
                scrollTop: document.getElementById('conversation').scrollHeight
              }, 800);
              
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