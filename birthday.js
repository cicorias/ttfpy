$(document).ready(function() {
  function parseDate(date) {
    if (!date) return null;
    var parts = date.split(".");
    var day = parseInt(parts[0], 10);
    var month = parseInt(parts[1], 10);
    var year = parseInt(parts[2], 10);
    var date = new Date();
    date.setDate(day);
    date.setMonth(month - 1);
    date.setYear(year);
    return date;
  }

  $("#birthday-filter").change(function() {
    var birthdate = parseDate($(this).val());

    function isOlder(node) {
      var value = $(node).attr("data-DateOfBirth") || "";
      if (!value || value === "NULL") return true;
      return parseDate(value) > birthdate;
    }

    $(".result").each(function() {
      var $result = $(this);

      var $metadatas = $result.find("[data-DateOfBirth]");
      var isFirstOlder = isOlder($metadatas[0]);
      var isSecondOlder = isOlder($metadatas[1]);
      var areAllOlder = isFirstOlder || isSecondOlder;

      if (areAllOlder) {
        $result.show();
      } else {
        $result.hide();
      }
    });
  });
});
