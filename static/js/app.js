'use strict';


const accordionItemsEl = document.querySelectorAll(".accordion__item");
const accordionItemsElc = document.getElementsByClassName("accordion__item");

function accordion() {
  console.log(accordionItemsEl);
  for (let item of accordionItemsElc) {
    let accHeader = item.firstElementChild;
    accHeader.addEventListener('click', ()=> {
      // this refers to accHeader, same thing
      let accDetails = accHeader.nextElementSibling;
      if (accDetails.style.maxHeight) {
        accDetails.style.maxHeight = null;
        accHeader.lastElementChild.innerHTML = "+";
      } else {
        accDetails.style.maxHeight = accDetails.scrollHeight + "px";  //scrollHeight
        accHeader.lastElementChild.innerHTML = "-";
      }
    });
  }

}


accordion();