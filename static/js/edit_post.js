$(function () {
    $("#submit-button").click(function(e){
      e.preventDefault();
      flag = validateForm();
      if(flag){
        $("#blogform").submit();
      }
    });
    $('#title').val(data.post.title);
    $('#content').val(data.post.content);
});

//Check if entered title is unique
function validateForm() {
  //Clean Up
    $("#title").removeClass("is-invalid");
    $("#TitleLabel").removeClass("text-danger");
    $(".invalid-title").addClass("invisible");
    $("#content").removeClass("is-invalid");
    $("#ContentLabel").removeClass("text-danger");
    $(".invalid-content").addClass("invisible");

    var title = $("#title").val();
    flag = true
    if($("#content").val() == ""){
      flag = false;
      $("#content").addClass("is-invalid");
      $("#ContentLabel").addClass("text-danger");
      $(".invalid-content").removeClass("invisible");
    }
    if(title != data.post.title){
      $.ajax({
        type: 'GET',
        async:false,
        url: '/app/ajax/check_title/',
        data: {title:title, type:"blog"},
        success: function(data){
          if(data=="False"){
            flag = false;
            $("#title").addClass("is-invalid");
            $("#title").val("");
            $("#TitleLabel").addClass("text-danger");
            $(".invalid-title").removeClass("invisible");
          }
        }
      });
    }
    return flag;
}
