$(function () {
  $("#messages-container").on('submit', '#send', function () {
    
    var data = new FormData(this);
    var $conversation = $('.conversation');

    $.ajax({
      url: '/messages/send/',
      data: data,
      cache: false,
      type: 'POST',
      contentType: false,
      processData: false,
      success: function (data) {
        $conversation.append(data);

        $conversation.stop().animate({
          scrollTop: document.getElementById('conversation').scrollHeight
        }, 800);
        
        $("input[name='attachement']").val('');
        $("#attach-frame").attr("src", "");
        $("input[name='message']").val('');
        $("input[name='message']").focus();
      }
    });
    return false;
  });
});