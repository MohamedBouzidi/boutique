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

  $('.product-small').on('click', function () {
    var $this = $(this);
    var boutiqueId = $this.attr('data-boutique-id');
    var productId = $this.attr('data-product-id');
    $.ajax({
      url: '/messages/send/product/',
      type: 'POST',
      data: {
        'to': $('#conversation_user').val(),
        'product_id': $this.attr('data-product-id')
      },
      success: function (data) {
        $('.send-message')
        .before("<li class='message'><img src='" + data.user.picture + "' class='picture'>"+
                "<div>" +
                  "<h5>" +
                    "<small class='pull-right'>" +
                      data.date +
                    "</small>" +
                    "<a href='#'>" +
                      data.user.name + 
                    "</a>" +
                  "</h5>" +
                    "<a href='" + data.link + "'>" +
                      "<img src='" + data.picture + "' class='img-responsive-thumbnail'>" +
                      "<h4>" + data.name + "</h4>" + 
                    "</a>" +
                "</div></li>");
        $('#myModal').modal('toggle');
      }
    });
  });
});