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

const message = BMI < 18.5 ? "(UnderWeight)" : BMI < 25 ? "(Normal)" : BMI < 30 ? "(overWeight)" : "(obese)"

  answer.innerText = BMI + " " + message;
  answer.style.display = "inline";
});
