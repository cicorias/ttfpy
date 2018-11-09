$(document).ready(function() {
  $("#name-search").change(function() {
    var searchFields = [
      "FamilyLinksFullName",
      "FullNameTransliterated",
      "FatherName",
      "MotherName",
    ];

    var $search = $(this);
    var searchExpression = null;
    try {
      searchExpression = new RegExp($search.val(), "gi");
    } catch (e) {
      alert(e);
      return;
    }

    $(".result").each(function() {
      var $result = $(this);

      var anyColumnMatches = searchFields.some(function(searchField) {
        var $metadatas = $result.find("[data-" + searchField + "]");
        var hasSearchTerm = $metadatas.filter(function(i, metadata) {
          var value = $(metadata).attr("data-" + searchField) || "";
          return value.match(searchExpression) != null;
        }).length > 0;
        return hasSearchTerm;
      });

      if (anyColumnMatches) {
        $result.show();
      } else {
        $result.hide();
      }
    });
  });
});
