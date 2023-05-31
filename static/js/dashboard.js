"use strict";

//selecting buttons
const dashboardButton = document.querySelector("#dashboard");
const classesButton = document.querySelector("#classes");
const activityButton = document.querySelector("#activity");
const profileButton = document.querySelector(".box-2");
const scheduleButton = document.querySelector("#schedule");
const scheduleBox = document.querySelector(".box-3");
const membershipButton = document.querySelector("#membership");
const manageAccButton = document.querySelector("#manageAccount");
// selecting containers
const dashContainer = document.querySelector("#dashboard-container");
const classesContainer = document.querySelector("#class-container");
const activityContainer = document.querySelector("#activity-container");
const profileContainer = document.querySelector(".profile-container");
const scheduleContainer = document.querySelector(".schedule-container");
const membershipContainer = document.querySelector(".membership-container");
const manageAccContainer = document.querySelector(".manage-container");

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

scheduleBox.addEventListener("click", () => {
  removeContainer();
  scheduleContainer.style.display = "block";
});

membershipButton.addEventListener("click", () => {
  removeContainer();
  membershipContainer.style.display = "block";
});

manageAccButton.addEventListener("click", () => {
  removeContainer();
  manageAccContainer.style.display = "block";
});

// removing every container
function removeContainer() {
  dashContainer.style.display = "none";
  classesContainer.style.display = "none";
  activityContainer.style.display = "none";
  profileContainer.style.display = "none";
  scheduleContainer.style.display = "none";
  membershipContainer.style.display = "none";
  manageAccContainer.style.display = "none";
}

// opening a preview

const openModalButton = document.querySelectorAll("[data-modal-target]"); // selecting every classContainer
const closeModalButton = document.querySelectorAll("[data-close-button]");

const overlay = document.querySelector("#overlay");

openModalButton.forEach((button) => {
  button.addEventListener("click", () => {
    const modal = document.querySelector(button.dataset.modalTarget);
    openModal(modal);
  });
});

overlay.addEventListener("click", () => {
  const modals = document.querySelectorAll(".preview-container.active");
  modals.forEach((modal) => {
    closeModal(modal);
  });
});

closeModalButton.forEach((button) => {
  button.addEventListener("click", () => {
    const modal = button.closest(".preview-container");
    closeModal(modal);
  });
});
function openModal(modal) {
  if (modal == null) return;
  modal.classList.add("active");
  overlay.classList.add("active");
}
function closeModal(modal) {
  if (modal == null) return;
  modal.classList.remove("active");
  overlay.classList.remove("active");
}
