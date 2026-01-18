function togglePassword() {
    const pwd = document.getElementById("password");
    pwd.type = pwd.type === "password" ? "text" : "password";
  }
  
  function validateLoginForm() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
  
    const usernameRegex = /^[a-zA-Z0-9_]{4,20}$/;
    const passwordRegex = /^[A-Za-z0-9!@#$%^&*()_+=\-]{6,}$/;
  
    if (!usernameRegex.test(username)) {
      alert("Invalid username. Must be 4-20 characters (letters, digits, underscore).");
      return false;
    }
  
    if (!passwordRegex.test(password)) {
      alert("Invalid password. Must be at least 6 characters with allowed symbols.");
      return false;
    }
  
    return true;
  }
  