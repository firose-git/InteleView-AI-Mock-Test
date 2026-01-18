// static/users/js/register.js
function toggleRegisterPassword() {
    const pwd = document.getElementById("regPassword");
    pwd.type = pwd.type === "password" ? "text" : "password";
  }
  
  function validateRegisterForm() {
    const email = document.querySelector(".input-email").value;
    const password = document.querySelector(".input-password").value;
    const confirm = document.querySelector(".input-confirm-password").value;
  
    const pwdRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{6,}$/;
  
    if (!pwdRegex.test(password)) {
      alert("Password must be at least 6 characters and include letters and numbers.");
      return false;
    }
  
    if (password !== confirm) {
      alert("Passwords do not match.");
      return false;
    }
  
    return true;
  }
  