var emailMessage = document.getElementById('cemail');
var emailInput = document.getElementById('email');
var passwordInput = document.getElementById('password');
if (emailMessage.innerHTML !== '') {
    emailInput.classList.add('error_class');
    passwordInput.classList.add('error_class');
}