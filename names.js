$(document).ready(function () {
  var searchFields = [
    "FamilyLinksFullName",
    "FullNameTransliterated",
    "FatherName",
    "MotherName",
  ];

  var searchExpression = null;

  function doIt (){

    var $search = $("#name-search");
    try {
      searchExpression = new RegExp($search.val(), "gi");
    } catch (e) {
      console.error(e);
      alert('error on search expression: %s', e);
    }    

    console.log('running all filters...');
    $(".result").each(function () {
      var $result = $(this);
      
      var anyColumnMatches = getColumnMatches($result);
      
      var min = $("#confidence-min").val();
      var max = $("#confidence-max").val();
      var confidenceMatches = shouldApplyConfidence($result, min, max);

      console.log('anyColumnMatches %s  -  %s', anyColumnMatches, confidenceMatches);
      if (anyColumnMatches && confidenceMatches) {
        console.log('showing');
        $result.show();
      } else {
        console.log('hiding');
        $result.hide();
      }
    });
  }

  
  function shouldApplyConfidence(item, min, max) {
    console.log('should Apply Confidence');
    var level = item.attr("data-confidence");
    console.log('level is %s', level);
    return min && max && (level > min / 100 && level < max / 100);
  }

  $("#name-search").change(function () {
    console.log('name search changed');
    doIt();
  });

  function getColumnMatches($result) {
    console.log('get column matches');
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

  function setSlider() {
    console.log('setting slider');
    var newMin = $("#slider-range").slider("values", 0);
    var newMax = $("#slider-range").slider("values", 1)
    $("#amount").val(newMin + " - " + newMax);
    $("#confidence-min").val(newMin);
    $("#confidence-max").val(newMax);
    doIt();
  }

  setSlider();
  doIt();
});
