$(function () {
    var animationSpeed = 300;

    $('.reaction-slider').on('mouseenter', function () {
      var $this = $(this);
      var normal = $this.children('.normal');
      var smile = $this.children('.smile');
      var love = $this.children('.love');
      var wish = $this.children('.wish');
      normal.animate({left: 0}, animationSpeed);
      smile.animate({left: '20%'}, animationSpeed);
      love.animate({left: '40%'}, animationSpeed);
      wish.animate({left: '60%'}, animationSpeed);
    });

    $('.reaction-slider').on('mouseleave', function () {
      var $this = $(this);
      var normal = $this.children('.normal');
      var smile = $this.children('.smile');
      var love = $this.children('.love');
      var wish = $this.children('.wish');
      normal.animate({left: '80%'}, animationSpeed);
      smile.animate({left: '75%'}, animationSpeed);
      love.animate({left: '70%'}, animationSpeed);
      wish.animate({left: '65%'}, animationSpeed);
    });
    
    $('.reaction-button').on('click', function () {
      var $this = $(this);
      var type = $this.attr('data-reaction');
      var productId = $this.attr('data-product-id');
      $.ajax({
          url: '/boutique/react/' + productId,
          data: {
              'reaction': type
          },
          success: function (data) {
              if (data.count > 0) {
                  if (data.count > 1) {
                      $this.parent().siblings('.reactions').text(data.count + ' reactions');
                  } else {
                      $this.parent().siblings('.reactions').text(data.count + ' reaction');
                  }
              } else {
                  $this.parent().siblings('.reactions').text('');
              }
          }
      })
    });
});