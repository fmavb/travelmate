   //We have a function, which for all elements of class .destination, adds autocomplete func

        $(document).ready(function () {
            $(".destination").autocomplete({
                //MaxResults is the number of results displayed when autocompleting
                maxResults: 10,
                //Source is the array of values we can suggest, inner function slices our parsed array
                source: function (request, response) {
                    var results = $.ui.autocomplete.filter(availableTags, request.term);
                    response(results.slice(0, this.options.maxResults));
                }
            });
        });

        //Check if entered destination is correct
        function validateForm() {
            var nameValue = document.getElementById("country").value;
            if (!availableTags.includes(nameValue)) {
                $(".destination").addClass("is-invalid");
                $(".destination").val("");
                $("#formGroupDestinationLabel").addClass("text-danger");
                $(".invalid-feedback").removeClass("invisible");
                return false;
            }
        }