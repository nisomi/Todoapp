var emailMessage = document.getElementById('cemail');
var emailInput = document.getElementById('email');
var passwordInput = document.getElementById('password');
var nameInput = document.getElementById('username');

if (emailMessage.innerHTML !== '') {
    emailInput.classList.add('error_class');
    passwordInput.classList.add('error_class');
    nameInput.classList.add('error_class')
}