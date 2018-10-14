//These are used for checking if datepickers are empty
var startcheck = null;
var endcheck = null;
$(function () {
    var dateFormat = "mm/dd/yy",
        //Date Range start datepicker function, .on function sets minDate for all datepickers
        start = $(".start").datepicker({
            defaultDate: "0",
            changeMonth: true,
            changeYear: true,
        }).on("change", function () {
            startcheck = getDate(this);
            end.datepicker("option", "minDate", getDate(this));
        }),
        //Date Range end datepicker function, .on function sets maxDate for all datepickers
        end = $(".end").datepicker({
            defaultDate: "+1w",
            changeMonth: true,
            changeYear: true,
        }).on("change", function () {
            endcheck = getDate(this);
            start.datepicker("option", "maxDate", getDate(this));
        });

    $(".origin").autocomplete({
        maxResults: 10,

        source: function (request, response) {
            var results = $.ui.autocomplete.filter(availableTags, request.term);
            response(results.slice(0, this.options.maxResults));
        }
    }).val(home).data(availableTags);

    $(".destination").autocomplete({
        //MaxResults is the number of results displayed when autocompleting
        maxResults: 10,
        //Source is the array of values we can suggest, inner function slices our parsed array
        source: function (request, response) {
            var results = $.ui.autocomplete.filter(availableTags, request.term);
            response(results.slice(0, this.options.maxResults));
        }
    });
    $("#submit-button").click(function (e) {
        e.preventDefault();
        flag = validateForm();
        if (flag) {
            $("#tripform").submit();
        }
    });

    //Returns selected date in correct format from the element
    function getDate(element) {
        var date;
        try {
            date = $.datepicker.parseDate(dateFormat, element.value);
        } catch (error) {
            date = null;
        }
        return date;
    }
});

//Check if entered destination is correct
function validateForm() {
    //Clean Up
    $(".origin").removeClass("is-invalid");
    $(".destination").removeClass("is-invalid");
    $("#formGroupDestinationLabel").removeClass("text-danger");
    $(".invalid-feedback").addClass("invisible");
    $("#title").removeClass("is-invalid");
    $("#TitleLabel").removeClass("text-danger");
    $(".invalid-title").addClass("invisible");
    $(".start").removeClass("is-invalid");
    $("#StartLabel").removeClass("text-danger");
    $(".invalid-start").addClass("invisible");
    $(".end").removeClass("is-invalid");
    $("#EndLabel").removeClass("text-danger");
    $(".invalid-end").addClass("invisible");

    var origin = document.getElementById("origin").value;
    var destination = document.getElementById("destination").value;
    var title = $("#title").val();
    flag = true

    if (!availableTags.includes(origin)) {
        $(".origin").addClass("is-invalid");
        $(".origin").val("");
        $("#formGroupOriginLabel").addClass("text-danger");
        $(".invalid-feedback").removeClass("invisible");
        flag = false;
    }

    if (!availableTags.includes(destination)) {
        $(".destination").addClass("is-invalid");
        $(".destination").val("");
        $("#formGroupDestinationLabel").addClass("text-danger");
        $(".invalid-feedback").removeClass("invisible");
        flag = false;
    }
    if (startcheck == null) {
        flag = false;
        $(".start").addClass("is-invalid");
        $("#StartLabel").addClass("text-danger");
        $(".invalid-start").removeClass("invisible");
    }
    if (endcheck == null) {
        flag = false;
        $(".end").addClass("is-invalid");
        $("#EndLabel").addClass("text-danger");
        $(".invalid-end").removeClass("invisible");
    }
    if (title != "") {
        $.ajax({
            type: 'GET',
            async: false,
            url: '/app/ajax/check_title/',
            data: {title: title, type: "trip"},
            success: function (data) {
                if (data == "False") {
                    flag = false;
                    $("#title").addClass("is-invalid");
                    $("#title").val("");
                    $("#TitleLabel").addClass("text-danger");
                    $(".invalid-title").text("You already have a trip with that title!");
                    $(".invalid-title").removeClass("invisible");
                }
            }
        });
    } else {
        flag = false;
        $("#title").addClass("is-invalid");
        $("#title").val("");
        $("#TitleLabel").addClass("text-danger");
        $(".invalid-title").text("Please enter a title for your trip!");
        $(".invalid-title").removeClass("invisible");
    }

    return flag;
}
