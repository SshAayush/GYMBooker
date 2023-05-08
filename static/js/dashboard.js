"use strict";

//selecting buttons
const dashboardButton = document.querySelector("#dashboard");
const classesButton = document.querySelector("#classes");
const activityButton = document.querySelector("#activity");

// selecting containers
const dashContainer = document.querySelector("#dashboard-container");
const classesContainer = document.querySelector("#class-container");
const activityContainer = document.querySelector("#activity-container");

// removing every container

dashboardButton.addEventListener("click", () => {
  removeContainer();
  dashContainer.style.display = "block";
});
classesButton.addEventListener("click", () => {
  removeContainer();
  classesContainer.style.display = "block";
});
activityButton.addEventListener("click", () => {
  removeContainer();
  activityContainer.style.display = "flex";
});

function removeContainer() {
  dashContainer.style.display = "none";
  classesContainer.style.display = "none";
  activityContainer.style.display = "none";
}
