$(function () {
  $("#send").submit(function () {
    
    var data = new FormData(this);

    $.ajax({
      url: '/messages/send/',
      data: data,
      cache: false,
      type: 'POST',
      contentType: false,
      processData: false,
      success: function (data) {
        $(".send-message").before(data);
        $("input[name='message']").val('');
        $("input[name='message']").focus();
      }
    });
    return false;
  });
});