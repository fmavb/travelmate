//Parse the available places from JSON
var data = JSON.parse('{{ json_data | escapejs }}');
var availableTags = data.names;
//$ sign is shortcut for jQuery, and getElementById(), function that sets up start and end datepickers
$( function() {
    var dateFormat = "mm/dd/yy",
        //Date Range start datepicker function, .on function sets minDate for all datepickers
        start = $( ".start" ).datepicker({
            defaultDate: "0",
            changeMonth: true,
            changeYear: true,
        }).on( "change", function() {
            end.datepicker( "option", "minDate", getDate( this ) );
        }),
        //Date Range end datepicker function, .on function sets maxDate for all datepickers
        end = $( ".end" ).datepicker({
            defaultDate: "+1w",
            changeMonth: true,
            changeYear: true,
        }).on( "change", function() {
            start.datepicker( "option", "maxDate", getDate( this ) );
        });

    //Returns selected date in correct format from the element
    function getDate( element ) {
        var date;
        try {
            date = $.datepicker.parseDate( dateFormat, element.value );
        } catch( error ) {
            date = null;
        }
        return date;
    }
});

$( function() {
$( ".destination" ).autocomplete({
    //MaxResults is the number of results displayed when autocompleting
    maxResults: 10,
        //Source is the array of values we can suggest, inner function slices our parsed array
    source: function(request, response) {
        var results = $.ui.autocomplete.filter(availableTags, request.term);
        response(results.slice(0, this.options.maxResults));
    }
});
});

function validateForm() {
  var nameValue = document.getElementById("country").value;
  if (!availableTags.includes(nameValue)) {
      $( ".destination" ).addClass("is-invalid");
      $( ".destination" ).val("");
      $( "#formGroupDestinationLabel" ).addClass("text-danger");
      $( ".invalid-feedback" ).removeClass("invisible");
      return false;
  }
}