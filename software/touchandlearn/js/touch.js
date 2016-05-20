$(document).ready(function(){
  $('.ro').click(function(){
    bootbox.dialog({
      animate: false,
      backdrop: false,
      title: "How does Reverse Osmosis Work?",
      message: '<iframe width="100%" height="600" src="https://www.youtube.com/embed/aVdWqbpbv_Y?autoplay=1" frameborder="0" allowfullscreen></iframe>'
    });
  });

  $('.electrostatic').click(function(){
    bootbox.dialog({
      title: "What are electrostatic air filters?",
      message: '<iframe width="100%" height="600" src="https://www.youtube.com/embed/0GTAhLL_IV4?autoplay=1" frameborder="0" allowfullscreen></iframe>'
    });
  });

  $('.evaporation').click(function(){
    bootbox.dialog({
      title: "What is evaporation?",
      message: '<iframe width="100%" height="600" src="https://www.youtube.com/embed/r8M7mah_QaY?list=PLKbu9ieLIl_cd60FiPhiBrgRgnvnb44eI?autoplay=1" frameborder="0" allowfullscreen></iframe>'
    });
  });


  $('.ozone-generator').click(function(){
    bootbox.dialog({
      title: "What are ozone generators?",
      message: '<iframe width="100%" height="600" src="https://www.youtube.com/embed/iWpdO55uFFA?autoplay=1" frameborder="0" allowfullscreen></iframe>'
    });
  });

  $('.condenser').click(function(){
    bootbox.dialog({
      title: "How do condensers and the refrigeration process work?",
      message: '<iframe width="100%" height="600" src="https://www.youtube.com/embed/h5wQoA15OnQ?autoplay=1" frameborder="0" allowfullscreen></iframe>'
    });
  });

  $('.compressor').click(function(){
    bootbox.dialog({
      title: "How do compressors work?",
      message: '<iframe width="100%" height="600" src="https://www.youtube.com/embed/S08sj8pfJJs?autoplay=1" frameborder="0" allowfullscreen></iframe>'
    });
  });

});