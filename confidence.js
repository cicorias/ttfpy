$(document).ready(function () {
  $('#apply').on('click', function () {
    console.log('apply min max confidence levels')
    var min = $("#confidence-min").val();
    var max = $("#confidence-max").val();
    console.log('using a min max of %s - %s', min, max)
    $(".result").filter(function () {
      var level = $(this).attr("data-confidence");
      console.log('level is %s', level);
      if (min && max && (level > min && level < max)) {
        $(this).show();
      }
      else {
        $(this).hide();
      }
    });
  });
});
