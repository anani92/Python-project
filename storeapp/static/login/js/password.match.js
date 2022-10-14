$(document).ready(function () {
  $("#password").focusout(function () {
    var password = $("#password").val();
    var confirmPassword = $("#confirm_password").val();
    if (password != confirmPassword) {
      alert("the passwords didn't match!");
    }
  });
});
