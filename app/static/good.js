
$(function(){
    var $good = $('.good-btn'),
                contentId;
    $good.on('click',function(e){
        e.stopPropagation();
        var $this = $(this);
        var data = JSON.stringify({"content_id":$this.data('content_id')});
        $.ajax({
            type: 'POST',
            url: '/good',
            data: data,
            contentType:'application/json'
        }).done(function(data){
            $this.next().text(data);
            $this.toggleClass('good-btn-active');
        }).fail(function(msg) {
            console.log('Ajax Error');
        });
    });
});

/*
$(window).load(init());

function init() {
  $(".good-btn").click(function() {
    $.ajax({
      type:'POST',
      url:'/postText',
      data:{'content_id': $(this).data('content_id')},
      contentType:'application/json',
      success:function(data) {
        $this.next().text(data);
        $this.toggleClass('good-btn-active');
      }
    });
    return false;
  });
}
*/