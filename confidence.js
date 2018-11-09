$(function () {
  var timeout;

  $("#slider-range").slider({
    orientation: "horizontal",
    max: 100,
    min: 50,
    range: true,
    values: [80, 100],
    slide: function (event, ui) {
      clearTimeout(timeout);
      timeout = setTimeout( () => { 
        console.log('wait 1/2 sec'); 
        setSlider() 
      }, 500);
    }
  });

  setSlider();

  function setSlider() {
    var newMin = $("#slider-range").slider("values", 0);
    var newMax = $("#slider-range").slider("values", 1)
    $("#amount").val(newMin + " - " + newMax);
    $("#confidence-min").val(newMin);
    $("#confidence-max").val(newMax);
    applyConfidence(newMin, newMax);
  }

  function applyConfidence(min, max) {
    console.log('apply min of %s and max of %s', min, max);
    $(".result").filter(function () {
      var level = $(this).attr("data-confidence");
      console.log('level is %s', level);
      if (min && max && (level > min / 100 && level < max / 100)) {
        console.log('showing this');
        $(this).show();
      }
      else {
        console.log('hiding this');
        $(this).hide();
      }
    });
  }
});
