"use strict";

const firstName = document.querySelector("#fname");
const lastName = document.querySelector("#lname");
const username = document.querySelector("#username");
const form = document.querySelector("#form");
// const errorElement = document.querySelector(".error");
const password = document.querySelector("#password");
const cPassword = document.querySelector("#c_password");
const email = document.querySelector("#email");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  if(validate()) {  // if validata() returns the true value then only submit the form...
    form.submit();
  }
});

function setError(element, errorMsg) {
  const parent = element.parentElement;
  const errorDiv = parent.lastElementChild;
  errorDiv.textContent = errorMsg;
}

function removeError(element) {
  const parent = element.parentElement;
  const errorDiv = parent.lastElementChild;
  errorDiv.textContent = "";
}

function validate() {
  let isValid = true;

  isValid = isValid && validateFirstName();
  isValid = isValid && validateLastName();
  isValid = isValid && validateUsername();
  isValid = isValid && validateEmail();
  isValid = isValid && validatePassword();
  isValid = isValid && validateConfirmPassword();
  return isValid;
}

function validateFirstName() {
  if (firstName.value === "" || firstName.value == null) {
    setError(firstName, "Name cannot be empty");
    return false;
  } else if (/\d/.test(username.value)) {
    setError(firstName, "Name cannot contain number");
    return false;
  } else {
    removeError(firstName);
    return true;
  }
}
function validateLastName() {
  if (lastName.value === "" || lastName.value == null) {
    setError(lastName, "Name cannot be empty");
    return false;
  } else if (/\d/.test(username.value)) {
    setError(lastName, "Name cannot contain number");
    return false;
  } else {
    removeError(lastName);
    return true;
  }
}

function validateUsername() {
  if (username.value === "" || username.value == null) {
    setError(username, "Username cannot be empty");
    return false;
  } else {
    removeError(username);
    return true;
  }
}

function validateEmail() {
  const ePattern = /^[A-Za-z\._\-0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/;
  if (email.value === "") {
    setError(email, "email cannot be empty");
    return false;
  } else if (!email.value.match(ePattern)) {
    setError(email, "invalid email");
    return false;
  } else {
    removeError(email);
    return true;
  }
}

function validatePassword() {
  const pPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]/;

  if (password.value === "") {
    setError(password, "password cannot be empty");
    return false;
  } else if (password.value.length < 8) {
    setError(password, "password must be of at least 8 characters");
    return false;
  } else if (!password.value.match(pPattern)) {
    setError(password, "password must contain at least 1 letter and 1 number");
    return false;
  } else {
    removeError(password);
    return true;
  }
}

function validateConfirmPassword() {
  if (cPassword.value === "") {
    setError(cPassword, "password cannot be empty!");
    return false;
  } else if (cPassword.value != password.value) {
    setError(cPassword, "password not matched");
    setError(password, "password not matched");
    return false;
  } else {
    removeError(cPassword);
    return true;
  }
}
