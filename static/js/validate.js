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
  validate();
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
  validateFirstName();
  validateLastName();
  validateUsername();
  validateEmail();
  validatePassword();
  validateConfirmPassword();
}

function validateFirstName() {
  if (firstName.value === "" || firstName.value == null) {
    setError(firstName, "Name cannot be empty");
  } else if (/\d/.test(username.value)) {
    setError(firstName, "Name cannot contain number");
  } else {
    removeError(firstName);
  }
}
function validateLastName() {
  if (lastName.value === "" || lastName.value == null) {
    setError(lastName, "Name cannot be empty");
  } else if (/\d/.test(username.value)) {
    setError(lastName, "Name cannot contain number");
  } else {
    removeError(lastName);
  }
}

function validateUsername() {
  if (username.value === "" || username.value == null) {
    setError(username, "Username cannot be empty");
  } else {
    removeError(username);
  }
}

function validateEmail() {
  const ePattern = /^[A-Za-z\._\-0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/;
  if (email.value === "") {
    setError(email, "email cannot be empty");
  } else if (!email.value.match(ePattern)) {
    setError(email, "invalid email");
  } else {
    removeError(email);
  }
}

function validatePassword() {
  const pPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]/;

  if (password.value === "") {
    setError(password, "password cannot be empty");
  } else if (password.value.length < 8) {
    setError(password, "password must be of at least 8 characters");
  } else if (!password.value.match(pPattern)) {
    setError(password, "password must contain at least 1 letter and 1 number");
  } else {
    removeError(password);
  }
}

function validateConfirmPassword() {
  if (cPassword.value === "") {
    setError(cPassword, "password cannot be empty!");
  } else if (cPassword.value != password.value) {
    setError(cPassword, "password not matched");
    setError(password, "password not matched");
  } else {
    removeError(cPassword);
  }
}
