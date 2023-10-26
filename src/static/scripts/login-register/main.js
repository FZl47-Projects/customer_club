  signupBtn = document.querySelector("#signup"),
  loginBtn = document.querySelector("#login"),
 loginform = document.querySelector(".login_form"),
 sign_upform = document.querySelector(".signup_form"),




pwShowHide = document.querySelectorAll(".pw_hide");
pwShowHide.forEach((icon) => {
  icon.addEventListener("click", () => {
    let getPwInput = icon.parentElement.querySelector("input");
    if (getPwInput.type === "password") {
      getPwInput.type = "text";
      icon.classList.replace("uil-eye-slash", "uil-eye");
    } else {
      getPwInput.type = "password";
      icon.classList.replace("uil-eye", "uil-eye-slash");
    }
  });
});



signupBtn.addEventListener("click", (e) => {
  e.preventDefault();
  sign_upform.classList.add("active");
  loginform.classList.remove("active");

});
loginBtn.addEventListener("click", (e) => {
  e.preventDefault();
  sign_upform.classList.remove("active");
  loginform.classList.add("active");
});




