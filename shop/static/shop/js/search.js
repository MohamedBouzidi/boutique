function debounce(callback, duration) {
  var timer;
  return function () {
    clearTimeout(timer);
    timer = setTimeout(callback, duration);
  }
}

$(document).ready(function () {
  $("#search-input").on("keyup", debounce(function() {
    var term = $(this).val().trim();

    $.ajax({
      url: '/ajax/search',
    })
  }, 1000));
});