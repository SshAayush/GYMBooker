"use strict";

const firstName = document.querySelector("#fname");
const lastName = document.querySelector("#lname");
const username = document.querySelector("#username");
const form = document.querySelector("#form");
const errorElement = document.querySelector(".error");
const password = document.querySelector("#password");
const cPassword = document.querySelector("#c_password");
const email = document.querySelector("#email");

var mailformat = /^w+([.-]?w+)*@w+([.-]?w+)*(.w{2,3})+$/;

form.addEventListener("submit", (e) => {
  let messages = [];

  if (
    firstName.value === "" ||
    (firstName.value === null && lastName.value === "") ||
    lastName.value === null
  ) {
    messages.push("Name is required");
  }
  if (password.value.length < 8) {
    messages.push("Password must be of 8 characters");
  }
  if (username.value === null) {
    messages.push("Username Cannot be empty");
  }
  else if (username.value.length < 5) {
    messages.push("Username must be of 5 characters");
  }
  if (password.value !== cPassword.value) {
    messages.push("password not matched");
  }
  if (email.value.match(mailformat)) {
    messages.push("");
  } else {
    messages.push("invalid email address");
  }

  if (messages.length > 0) {
    e.preventDefault();
    errorElement.innerText = messages.join(", ");
  }
});