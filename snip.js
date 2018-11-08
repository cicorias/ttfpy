<script>
$(document).ready(function () {
  console.log('loaded');
  $("#confidence").change( function () {
    console.log('keyup');
    var value = $(this).val();
    $(".result").filter(function () {
      // $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      $(this).toggle($(this).attr("data-confidence") < value)
      console.log('doing it...')
    });
  });
});
</script>
<input id="confidence" type="text">

