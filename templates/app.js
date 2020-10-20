//cache elements
const progressBarEl = document.querySelector('.progress__inner');

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

lanuch(0, status);