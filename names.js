$(document).ready(function () {
  var searchFields = [
    "FamilyLinksFullName",
    "FullNameTransliterated",
    "FatherName",
    "MotherName",
  ];

  var searchExpression = null;

  $("#name-search").change(function () {
    var $search = $(this);
    try {
      searchExpression = new RegExp($search.val(), "gi");
    } catch (e) {
      alert(e);
      return;
    }

    $(".result").each(function () {
      var $result = $(this);
      var anyColumnMatches = getColumnMatches($result);

      if (anyColumnMatches) {
        $result.show();
      } else {
        $result.hide();
      }
    });
  });

  function getColumnMatches($result) {
    var anyColumnMatches = searchFields.some(function (searchField) {
      var $metadatas = $result.find("[data-" + searchField + "]");
      var hasSearchTerm = $metadatas.filter(function (i, metadata) {
        var value = $(metadata).attr("data-" + searchField) || "";
        return value.match(searchExpression) != null;
      }).length > 0;
      return hasSearchTerm;
    });

    return anyColumnMatches;
  }

  var timeout;

  $("#slider-range").slider({
    orientation: "horizontal",
    max: 100,
    min: 50,
    range: true,
    values: [80, 100],
    slide: function (event, ui) {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
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
      var shouldShow = shouldApplyConfidence($(this), min, max);
      if (shouldShow)
        $(this).show()
      else
        $(this).hide();
    });
  }

  function shouldApplyConfidence(item, min, max) {
    var level = item.attr("data-confidence");
    console.log('level is %s', level);
    return min && max && (level > min / 100 && level < max / 100);
  }
});
