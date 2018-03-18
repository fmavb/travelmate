$(function () {
            // getCookie function is used to get csrf token for post, from the cookies
            function getCookie(c_name) {
                if (document.cookie.length > 0) {
                    c_start = document.cookie.indexOf(c_name + "=");
                    if (c_start != -1) {
                        c_start = c_start + c_name.length + 1;
                        c_end = document.cookie.indexOf(";", c_start);
                        if (c_end == -1) c_end = document.cookie.length;
                        return unescape(document.cookie.substring(c_start, c_end));
                    }
                }
                return "";
            }

            //Comment submit onclick listener
            $('#commentsubmit').click(function () {
                var comment = $('#comment').val();
                var slug = $('#commentsubmit').attr("data-slug");
                if ($('#comment').val() != "") {

                    //Set up header with csrf token
                    $.ajaxSetup({
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
                    });

                    //use AJAX POST to submit the comemnt
                    $.ajax({
                        type: "POST",
                        url: "/app/ajax/comment/",
                        data: {
                            'comment': comment,
                            'slug': slug,
                        },
                        success: function (response) {
                            if ($('#nocomments').length) {
                                $('#nocomments').hide();
                            }
                            commentstring = "<p>" + response.user + " on " + response.date + " said: <br>" +
                                response.content + "</p>";
                            $('#commentsection').append(commentstring);
                        }
                    });

                }
            });
        });