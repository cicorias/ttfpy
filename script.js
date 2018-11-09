$(document).ready(function () {
  var searchFields = [
    "FamilyLinksFullName",
    "FullNameTransliterated",
    "FatherName",
    "MotherName",
  ];

  var searchExpression = null;
  var searchCriteria = [];

  function doIt (){
    var $search = $("#name-search");
    try {
      searchExpression = new RegExp($search.val(), "gi");
    } catch (e) {
      console.error(e);
      alert('error on search expression: %s', e);
    }

    searchCriteria = [];
    $("select").each(function() {
      var $select = $(this);
      searchCriteria.push({
        dimension: $select.attr("name"),
        term: $select.val(),
      });
    });

    console.log('running all filters...');
    $(".result").each(function () {
      var $result = $(this);
      
      var anyColumnMatches = getColumnMatches($result);
      
      var min = $("#confidence-min").val();
      var max = $("#confidence-max").val();
      var confidenceMatches = shouldApplyConfidence($result, min, max);

      var isDropDown = hasAllSearchTerms($result, searchCriteria);

      var ageOk = isAgeOk($result);

      console.log('anyColumnMatches %s  -  conf: %s  -  young: %s', anyColumnMatches, confidenceMatches, ageOk);
      if (anyColumnMatches && confidenceMatches && isDropDown && ageOk) {
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

  $("select").change(function() {
    console.log('selections changed');
    doIt();
  });

  $("#birthday-filter").change(function() {
    console.log('birthday changed');
    doIt();
  });

  function isInvalidDate(node) {
    var value = $(node).attr("data-DateOfBirth") || "";
    console.log('isInvalidDate check on value: %s', value);
    if ($("#birthday-filter").val() === "")
      return true;

    return !value || value === "NULL";
  }

  function isYoungerDate(node) {
    var value = $(node).attr("data-DateOfBirth") || "";
    var birthdate = parseDate($("#birthday-filter").val());
    console.log('isYoungerDate - dob: %s  -- birthdate: %s', value, birthdate)
    return parseDate(value) > birthdate;
  }

  function parseDate(date) {
    if (!date) return null;
    var parts = date.split(".");
    var day = parseInt(parts[0], 10);
    var month = parseInt(parts[1], 10);
    var year = parseInt(parts[2], 10);
    var date = new Date(year,month - 1, day, 0, 0, 0);
    return date;
  }

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

  function hasAllSearchTerms ($result, searchCriteria) {
    console.log('has all search terms');
    var hasAllSearchTerms = searchCriteria.every(function(search) {
      var $metadatas = $result.find("[data-" + search.dimension + "]");
      var hasSearchTerm = $metadatas.filter(function(i, metadata) {
        var value = $(metadata).attr("data-" + search.dimension) || "";
        return value.indexOf(search.term) !== -1;
      }).length > 0;
      return hasSearchTerm;
    });

    return hasAllSearchTerms;
  }

  function isAgeOk ($result){
    var $metadatas = $result.find("[data-DateOfBirth]");
    if (isInvalidDate($metadatas[0]) || isInvalidDate($metadatas[1])) {
      console.warn('invalid date passed');
      return true;
    }

    if (isYoungerDate($metadatas[0]) && isYoungerDate($metadatas[1])){
      console.log('isAgeOk - no');
      return false;
    }
    else 
      {
        console.log('isAgeOK -- YES');
        return true;
      }
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
