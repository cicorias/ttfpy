$(document).ready(function() {
  $("select").change(function() {
    var searchCriteria = [];
    $("select").each(function() {
      var $select = $(this);
      searchCriteria.push({
        dimension: $select.attr("name"),
        term: $select.val(),
      });
    });

    $(".result").each(function() {
      var $result = $(this);

      var hasAllSearchTerms = searchCriteria.every(function(search) {
        var $metadatas = $result.find("[data-" + search.dimension + "]");
        var hasSearchTerm = $metadatas.filter(function(i, metadata) {
          var value = $(metadata).attr("data-" + search.dimension) || "";
          return value.indexOf(search.term) !== -1;
        }).length > 0;
        return hasSearchTerm;
      });

      if (hasAllSearchTerms) {
        $result.show();
      } else {
        $result.hide();
      }
    });
  });
});
