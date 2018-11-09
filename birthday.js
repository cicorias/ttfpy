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

    function isInvalid(node) {
      var value = $(node).attr("data-DateOfBirth") || "";
      return !value || value === "NULL";
    }

    function isYounger(node) {
      var value = $(node).attr("data-DateOfBirth") || "";
      return parseDate(value) > birthdate;
    }

    $(".result").each(function() {
      var $result = $(this);

      var $metadatas = $result.find("[data-DateOfBirth]");
      if (isInvalid($metadatas[0]) || isInvalid($metadatas[1])) {
        $result.show();
        return;
      }

      if (isYounger($metadatas[0]) && isYounger($metadatas[1])) {
        $result.hide();
      } else {
        $result.show();
      }
    });
  });
});
