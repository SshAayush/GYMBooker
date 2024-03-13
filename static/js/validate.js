"use strict";


function setError(element, errorMsg) {
  const parent = element.parentElement;
  const errorDiv = parent.querySelector(".error");
  errorDiv.textContent = errorMsg;
}

function removeError(element) {
  const parent = element.parentElement;
  const errorDiv = parent.querySelector(".error");
  errorDiv.textContent = "";
}

let isValid = true;

function validateFirstName() {
  const firstName = document.querySelector("#fname");
  if (firstName.value === "" || firstName.value == null) {
    setError(firstName, "Name cannot be empty");
    return false;
  } else if (/\d/.test(firstName.value)) {
    setError(firstName, "Name cannot contain numbers");
    return false;
  } else {
    removeError(firstName);
    return true;
  }
}

function validateLastName() {
  const lastName = document.querySelector("#lname");
  if (lastName.value === "" || lastName.value == null) {
    setError(lastName, "Name cannot be empty");
    return false;
  } else if (/\d/.test(lastName.value)) {
    setError(lastName, "Name cannot contain numbers");
    return false;
  } else {
    removeError(lastName);
    return true;
  }
}

function validateUsername() {
  const username = document.querySelector("#username");
  if (username.value === "" || username.value == null) {
    setError(username, "Username cannot be empty");
    return false;
  } else {
    removeError(username);
    return true;
  }
}

function validateEmail() {
  const email = document.querySelector("#email");
  const emailPattern = /^[A-Za-z\._\-0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/;
  if (email.value === "") {
    setError(email, "Email cannot be empty");
    return false;
  } else if (!email.value.match(emailPattern)) {
    setError(email, "Invalid email");
    return false;
  } else {
    removeError(email);
    return true;
  }
}

function validatePassword() {
  const password = document.querySelector("#password");
  const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]/;
  if (password.value === "") {
    setError(password, "Password cannot be empty");
    return false;
  } else if (password.value.length < 8) {
    setError(password, "Password must be at least 8 characters");
    return false;
  } else if (!password.value.match(passwordPattern)) {
    setError(
      password,
      "Password must contain at least 1 letter and 1 number"
    );
    return false;
  } else {
    removeError(password);
    return true;
  }
}

function validateConfirmPassword() {
  const cPassword = document.querySelector("#c_password");
  const password = document.querySelector("#password");
  if (cPassword.value === "") {
    setError(cPassword, "Password cannot be empty");
    return false;
  } else if (cPassword.value !== password.value) {
    setError(cPassword, "Passwords do not match");
    setError(password, "Passwords do not match");
    return false;
  } else {
    removeError(cPassword);
    return true;
  }
}

function validate() {
  isValid = true;
  isValid = validateFirstName() && isValid;
  isValid = validateLastName() && isValid;
  isValid = validateUsername() && isValid;
  isValid = validateEmail() && isValid;
  isValid = validatePassword() && isValid;
  isValid = validateConfirmPassword() && isValid;
  return isValid;
}

const form = document.querySelector("#form");
form.addEventListener("submit", (e) => {
  if (!validate()) {
    e.preventDefault();
  }
});

// for show password

const password = document.querySelectorAll(".password");
const showPassword = document.querySelector(".fa-eye");

console.log(showPassword);


  showPassword.addEventListener("click", () => {
    togglePassword();
  });




function togglePassword(){
  [...password].map((passwords) => passwords.type === "text" ? passwords.type = "password" :
  passwords.type = "text"
)}






