"use strict";

const firstName = document.querySelector("#fname");
const lastName = document.querySelector("#lname");
const form = document.querySelector("#form");
const errorElement = document.querySelector(".error");

form.addEventListener("submit", (e) => {
  let messages = [];

  if (firstName.value === "" || firstName.value === null) {
    messages.push("name is required");
  }

  if (messages.length > 0) {
    e.preventDefault();
    errorElement.innerText = messages.join(", ");
  }
});
