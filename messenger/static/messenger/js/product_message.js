$(function() {
  $.ajaxSetup({ 
       beforeSend: function(xhr, settings) {
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
           if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
               // Only send the token to relative URLs i.e. locally.
               xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
           }
       } 
  });

  $('.products').on('click', '.product-small', function () {
    var $this = $(this);
    var boutiqueId = $this.attr('data-boutique-id');
    var productId = $this.attr('data-product-id');
    var $conversation = $('.conversation');

    $.ajax({
      url: '/messages/send/product/',
      type: 'POST',
      data: {
        'to': $('#conversation_user').val(),
        'product_id': $this.attr('data-product-id')
      },
      success: function (data) {
        $conversation.append(data);

        $conversation.stop().animate({
          scrollTop: document.getElementById('conversation').scrollHeight
        }, 800);

        $('#myModal').modal('toggle');
      }
    });
  });
});