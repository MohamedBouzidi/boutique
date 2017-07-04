$("document").ready(function () {
    function debounce(callback, duration) {
      var timer;
      return function () {
        clearTimeout(timer);
        timer = setTimeout(callback, duration);
      }
    }

    $(document).ready(function () {
      $("#search-input").on("keyup", debounce(function() {
        var term = $("#search-input").val();

        $.ajax({
            url: "search",
            type: "GET",
            data: {
                'term': term
            },
            success: function (data) {
                console.log(data);
            }
        })
      }, 1000));
    });
});