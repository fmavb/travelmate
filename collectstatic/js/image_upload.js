// Attach jQuery file uploader to certain class
        $(function () {
            $(".js-upload-photos").click(function () {
                $("#fileupload").click();
            });

            $("#fileupload").fileupload({
                // Save uploaded file data in json
                dataType: 'json',
                //When we are done, and have successfully uploaded our images, add the image data to our JSON
                done: function (e, data) {
                    if (data.result.is_valid) {
                        deletestring = deletestring + data.result.name + '/"></a></td>';
                        $("#gallery tbody").prepend(
                            "<tr>" +
                            "<td><a href='" + data.result.url + "'>" + data.result.name + "</a></td>" +
                            deletestring +
                            "</tr>"
                        )
                    }
                }
            });
        });