$(function() {
  var $site_search = $("#site-search");
  $site_search.on("change", function(e) {
    e.stopPropagation();
    var $this = $(this);
    var search_text = $this[0].value;
    var data = JSON.stringify({ search_text: search_text });
    $.ajax({
      type: "POST",
      url: "/search_suggest",
      data: data,
      contentType: "application/json"
    })
      .done(function(suggest_list) {
        html_text = '';
        for (var i=0;i<suggest_list.length;i++) {
            var data = suggest_list[i];
          html_text += "<option value=" + data.word + "> </option>";
        }
        $("#search_suggest").html(html_text);
      })
      .fail(function(msg) {
        console.log("Ajax Error");
      });
  });
});
