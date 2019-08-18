$(function() {
  var $site_search = $("#site-search");
  $site_search.on("change", function(e) {
    e.stopPropagation();
    var $this = $(this);
    var data = JSON.stringify({ search_text: $this.value });
    $.ajax({
      type: "POST",
      url: "/search_suggest",
      data: data,
      contentType: "application/json"
    })
      .done(function(suggest_list) {
        html_text = '<datalist id="search_suggest">';
        for (var data in suggest_list) {
          html_text += "<option value=" + data + "> </option>";
        }
        html_text += "</datalist>";
        $this.next().innerHTML = html_text;
      })
      .fail(function(msg) {
        console.log("Ajax Error");
      });
  });
});
