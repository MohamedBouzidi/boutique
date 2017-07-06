$("document").ready(function () {
    $("#submit-button").on('click', function (e) {
        e.preventDefault();
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
        var $this = $(this);
        var categorieId = $this.attr("data-categorie-id");
        $.ajax({
            url: 'search',
            type: 'GET',
            dataType: 'json',
            data: {
                'categorie_id': categorieId,
                'price_min': 1,
                'price_max': 2,
                'type_id': 2
            },
            success: function (data) {
                console.log(data);
            }
        });
    });
});