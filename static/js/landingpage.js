"use strict";

// BMI CALCULATION
const weight = document.querySelector("#weight");
const height = document.querySelector("#height");
const answer = document.querySelector(".ans");
const calculateBtn = document.querySelector(".calculate");

answer.style.display = "none";

calculateBtn.addEventListener("click", () => {
  const inpWeight = +weight?.value;
  const inpHeight = +height?.value;

  const BMI = Math.trunc((inpWeight / Math.pow(inpHeight, 2)) * 10000);

  answer.innerText = BMI;
  answer.style.display = "inline";
});
