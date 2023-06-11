var emailMessage = document.getElementById('cemail');
var passwordMessage = document.getElementById('cpassword');
var emailInput = document.getElementById('email');
var passwordInput = document.getElementById('password');
var nameInput = document.getElementById('username');

if ((emailMessage.innerHTML !== '') || (passwordMessage.innerHTML !== '')) {
    emailInput.classList.add('error_class');
    passwordInput.classList.add('error_class');
    nameInput.classList.add('error_class')
}
$('#updateBtn').click(function () {
    var passwordInput = document.getElementById("password");
    var passwordValue = passwordInput.value;
    console.log(passwordValue);
});