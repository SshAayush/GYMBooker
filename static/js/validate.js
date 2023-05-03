"use strict";

const firstName = document.querySelector("#fname");
const lastName = document.querySelector("#lname");
const form = document.querySelector("#form");
const errorElement = document.querySelector(".error");
const password = document.querySelector("#password");
const cPassword = document.querySelector("#c_password");
const email = document.querySelector("#email");

var mailformat = "/^w+([.-]?w+)*@w+([.-]?w+)*(.w{2,3})+$/";

form.addEventListener("submit", (e) => {
  let messages = [];

  if (
    firstName.value === "" ||
    (firstName.value === null && lastName.value === "") ||
    lastName.value === null
  ) {
    messages.push("name is required");
  }
  if (password.value.length < 8) {
    messages.push("Password must be of 8 characters");
  }
  if (password.value !== cPassword.value) {
    messages.push("password not matched");
  }
  if (email.value.match(mailformat)) {
    messages.push("");
  } else {
    messages.push("invalid email address");
  }

  if (messages.length < 0) {
    e.preventDefault();
    errorElement.innerText = messages.join(", ");
  }
});
