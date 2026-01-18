// static/users/js/login.js
function togglePassword() {
  const pwd = document.getElementById("passwordField");
  const eye = document.getElementById("eyeIcon");

  if (pwd.type === "password") {
    pwd.type = "text";
    eye.classList.remove("fa-eye");
    eye.classList.add("fa-eye-slash");
  } else {
    pwd.type = "password";
    eye.classList.remove("fa-eye-slash");
    eye.classList.add("fa-eye");
  }
}

  
  function validateLoginForm() {
    const email = document.querySelector(".input-email").value;
    const password = document.querySelector(".input-password").value;
    const regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{6,}$/;
  
    if (!regex.test(password)) {
      alert("Password must be at least 6 characters long and include letters and numbers.");
      return false;
    }
  
    return true;
  }
  