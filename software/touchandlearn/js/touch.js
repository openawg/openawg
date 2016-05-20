$(document).ready(function(){
  $('.st21').click(function(){
    bootbox.dialog({
      animate: false,
      backdrop: false,
      title: "Video 1",
      message: '<iframe width="696" height="391" src="https://www.youtube.com/embed/y2-uaPiyoxc?autoplay=1" frameborder="0" allowfullscreen></iframe>'
    });
  });

  $('#ellipse1').click(function(){
    bootbox.dialog({
      title: "Video 1",
      message: '<iframe width="696" height="391" src="https://www.youtube.com/embed/y2-uaPiyoxc" frameborder="0" allowfullscreen></iframe>'
    });
  });

  $('#path1').click(function(){
    bootbox.dialog({
      title: "Video 1",
      message: '<iframe width="696" height="391" src="https://www.youtube.com/embed/y2-uaPiyoxc" frameborder="0" allowfullscreen></iframe>'
    });
  });
});