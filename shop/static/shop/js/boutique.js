$(".delete").on('click', function (e) {
    e.preventDefault();
    var c = confirm("Are you sure?");
    if (c) {
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
        var productId = $this.attr("data-product-id");
        var boutiqueId = $this.attr("data-boutique-id");
        $.ajax({
            url: boutiqueId + "/products/" + productId + "/delete",
            type: "POST",
            success: function (data) {
                $this.parent().parent().parent().remove();
            }
        });                
    }
});

// $("#ajouter").on('click', function (e) {
//     e.preventDefault();
//     var $this = $(this);
//     var boutiqueId = $this.attr("data-boutique-id");
//     $.ajax({
//         url: boutiqueId + "/products/new",
//         type: "GET",
//         success: function (data) {
//             $("#content").html(data);
//         } 
//     })
// });