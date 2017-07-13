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

$(".delete").on('click', function (e) {
    e.preventDefault();
    var c = confirm("Are you sure?");
    if (c) {
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

$(".state").on('click', function (e) {
    var $this = $(this);
    var boutiqueId = $this.attr("data-boutique-id");
    var productId =  $this.attr("data-product-id");

    $.ajax({
        url: boutiqueId + '/products/' + productId + '/state',
        type: 'POST',
        dataType: 'json'
    });
});

$("#delete-user").on('click', function (e) {
    e.preventDefault();
    var c = confirm("Are you sure?");
    if (c) {
        $.ajax({
            url: 'account/delete',
            type: "POST",
            success: function (data) {
                window.location.href = '/boutique';
            }
        });                
    }
});

$(".dublicate").on('click', function (e) {
    e.preventDefault();
    var $this = $(this);
    var productId = $this.attr("data-product-id");
    var boutiqueId = $this.attr("data-boutique-id");

    var state_template = '<tr><td><div class="togglebutton"><label><input type="checkbox" name="active" data-boutique-id="{{ boutique_id }}" data-product-id="{{ id }}" class="state"></label></div></td>';
    var state_template_checked = '<tr><td><div class="togglebutton"><label><input type="checkbox" name="active" data-boutique-id="{{ boutique_id }}" data-product-id="{{ id }}" class="state" checked></label></div></td>';
    var links_template = '<td><div class="btn-group" role="group">' +
        '<a href="/boutique/{{ boutique_id }}/products/{{ id }}" class="btn btn-default btn-sm" id="detail-url">Detail</a>' +
        '<a href="/boutique/{{ boutique_id }}/products/{{ id }}/edit" class="btn btn-default btn-sm" id="edit-url">Edit</a>' +
        '<a href="/boutique/{{ boutique_id }}/products/{{ id }}/delete" class="btn btn-default btn-sm delete" data-boutique-id="{{ boutique_id }}" data-product-id="{{ id }}" id="delete-url">Delete</a>' +
        '<a href="/boutique/{{ boutique_id }}/products/{{ id }}/dublicate" class="btn btn-default btn-sm dublicate" data-boutique-id="{{ boutique_id }}" data-product-id="{{ id }}" id="dublicate-url">Detail</a>' +
        '</div></td></tr>';

    var image_template = '<td class="image">' + $this.closest('td').siblings('td.image').html() + '</td>';
    var quantite_template = '<td class="quantite">' + $this.closest('td').siblings('td.quantite').html() + '</td>';
    var price_template = '<td class="price">' + $this.closest('td').siblings('td.price').html() + '</td>';

    $.ajax({
        url: boutiqueId + "/products/" + productId + "/dublicate",
        type: "POST",
        success: function (data) {
            var data = JSON.parse(data);
            var template = image_template + quantite_template + price_template + links_template;
            if (data.active) {
                template = state_template_checked + template;
            } else {
                template = state_template + template;
            }

            $this.closest("tbody").append(Mustache.render(template, data));
        } 
    });
});