$(function () {
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

  $('.reaction').on('click', function () {
    var $this = $(this);
    var id = $this.attr('data-id');
    var reaction = $this.attr('data-reaction');
    $.ajax({
      url: '/boutique/react/' + id,
      type: 'GET',
      data: {
        reaction: reaction,
      },
      success: function (likes) {
        if (likes.count > 0) {
          $this.siblings('.likes').html(likes.count +  ' like(s)');
          $this.text(likes.message);
        } else {
          $this.siblings('.likes').html('');
          $this.text('Like');
        }
      }
    });
  });
});