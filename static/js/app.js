//cache elements
const progressBarEl = document.querySelector('.progress__inner');
const resultEl = document.querySelector('#result');
const inputEl = document.querySelector('.keywords__text');


const lanuch = (start, end) => {
  let statusBar = setInterval(() => {
    if(start === end) {
      clearInterval(statusBar);
    } else {
      start++;
      progressBarEl.style.width = `${start}%`;
    }
  }, 20);
}

const status = 55;

// inputEl.value 
// resultEl.value = 3;

// setInterval(() => {
//   if(inputEl.value) {
//     console.log(inputEl.value);
//   }
// }, 50);

// console.log(document.getElementById("myVar").value);
console.log('hi');
lanuch(0, status);