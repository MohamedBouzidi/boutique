$(function () {
  function debounce(callback, duration) {
    var timer;
    return function () {
      clearTimeout(timer);
      timer = setTimeout(callback, duration);
    }
  }

  var $pager = $('.pager')
  var boutiqueId = $('.product-small').first().attr('data-boutique-id');

  function search(page) {
    $.ajax({
      url: '/boutique/' + boutiqueId + '/products/',
      type: 'GET',
      data: {
        query: $('#product-search').val(),
        page: page
      },
      cache: false,
      success: function (data) {
        $('.products').hide().html(data).fadeIn('slow');
        page = $(".page").val();
        $pager.attr('data-current-page', page);
      }
    });
  }

  $('#product-search').on('keyup', debounce(function () {
    var page = parseInt($pager.attr('data-current-page'));
    search(1)
  }, 500)); 
  $('#next').on('click', function () {
    var page = parseInt($pager.attr('data-current-page'));
    search(page+1);
  }); 
  $('#prev').on('click', function () {
    var page = parseInt($pager.attr('data-current-page'));
    search(page-1);
  }); 
});