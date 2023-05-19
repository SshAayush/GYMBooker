"use strict";

//selecting buttons
const dashboardButton = document.querySelector("#dashboard");
const classesButton = document.querySelector("#classes");
const activityButton = document.querySelector("#activity");
const profileButton = document.querySelector(".box-2");
const scheduleButton = document.querySelector("#schedule");
console.log(scheduleButton);
console.log(activityButton);
// selecting containers
const dashContainer = document.querySelector("#dashboard-container");
const classesContainer = document.querySelector("#class-container");
const activityContainer = document.querySelector("#activity-container");
const profileContainer = document.querySelector(".profile-container");
const scheduleContainer = document.querySelector(".schedule-container");

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

profileButton.addEventListener("click", () => {
  removeContainer();
  profileContainer.style.display = "block";
});

scheduleButton.addEventListener("click", () => {
  removeContainer();
  scheduleContainer.style.display = "block";
});

// removing every container
function removeContainer() {
  dashContainer.style.display = "none";
  classesContainer.style.display = "none";
  activityContainer.style.display = "none";
  profileContainer.style.display = "none";
  scheduleContainer.style.display = "none";
}
