$(function () {
  function debounce(callback, duration) {
    var timer;
    return function () {
      clearTimeout(timer);
      timer = setTimeout(callback, duration);
    }
  }

  function updateProduct(product, data) {
    product.attr('data-product-id', data.id);
    product.attr('data-boutique-id', data.boutique.id);
    product.children('.image').attr('src', data.image);
    product.children('.image').attr('alt', data.name);
    product.children('.caption').children('.title').html(data.name);
    product.children('.caption').children('badge').html(data.price + ' DT');
    product.children('.caption').children('categorie').html(data.categorie.label);
  }

  var boutiqueId = $('.product-small').first().attr('data-boutique-id');

  $('#product-search').on('keyup', debounce(function () {
    $.ajax({
      url: '/boutique/' + boutiqueId + '/products/',
      type: 'GET',
      data: {
        query: $('#product-search').val()
      },
      cache: false,
      success: function (data) {
        $('.product-small').each(function (i) {
          updateProduct($(this), data[i]);
        });
      }
    });
  }, 500));  
});