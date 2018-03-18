        $(function () {
            //Sets star colouring, depending on which star is clicked
            var rating = 0;
            $('.fa-star').click(function () {
                rating = this.id;
                $('.fa-star').each(function () {
                    if (this.id <= rating) {
                        $(this).addClass('checked');
                    } else {
                        $(this).removeClass('checked');
                    }
                });
            });

            //If rating submisson, start AJAX GET to create a rating, and update trip score
            $('#rate').click(function () {
                if (rating != 0) {
                    var slug;
                    slug = $(this).attr("data-slug");
                    $.get('/app/ajax/like_trip/', {slug: slug, rating: rating}, function (data) {
                        $('#like_count').html("Overall score: " + data);
                        $('#success').html("You rated this Trip: " + rating);
                        $('.fa-star').each(function () {
                            $(this).hide();
                        });
                        $('#rate').hide();
                    });
                }
            });
        });