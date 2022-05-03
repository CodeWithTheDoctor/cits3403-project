/**
 * EXAMPLE
 */
// const a = "03 213 33 435 63\n"+
// "30\n"+
// "326\n"+
// "34 52\n"+
// "\n"+
// "14";
const exampleLevel = "03 213 33 435 63\n" + "30\n" + "326\n" + "34 52\n" + "\n" + "14";

/**
 * Enums
 * These are the possible states for each cell of the grid.
 */
const EMPTY = 0;
const BULB = 1;
const BLACK = 3;
const ZERO = 4;
const ONE = 5;
const TWO = 6;
const THREE = 7;
const FOUR = 8;

/**
 * Grid - a 2D array that contains the initial state of the puzzle.
 */
let grid = [];

const initialiseEmptyGrid = () => {
  for (i = 0; i < 7; i++) {
    grid[i] = [];
    for (j = 0; j < 7; j++) {
      grid[i][j] = EMPTY;
    }
  }
};

initialiseEmptyGrid();

/**
 * Function for parsing a string from a text file containing the information of the puzzle level into the array called grid.
 * @param {string} puzzleString
 */
const parseGrid = puzzleString => {
  const coords = puzzleString.split("\n");
  const BLACK_CELLS = coords[0].split(" ");
  const ZERO_CELLS = coords[1].split(" ");
  const ONE_CELLS = coords[2].split(" ");
  const TWO_CELLS = coords[3].split(" ");
  const THREE_CELLS = coords[4].split(" ");
  const FOUR_CELLS = coords[5].split(" ");

  for (i = 0; i < 6; i++) {
    switch (i) {
      case 0:
        for (x of BLACK_CELLS) {
          for (k = 1; k < x.length; k++) {
            grid[x[0]][x[k]] = BLACK;
          }
        }
        break;
      case 1:
        for (x of ZERO_CELLS) {
          for (k = 1; k < x.length; k++) {
            grid[x[0]][x[k]] = ZERO;
          }
        }
        break;
      case 2:
        for (x of ONE_CELLS) {
          for (k = 1; k < x.length; k++) {
            grid[x[0]][x[k]] = ONE;
          }
        }
        break;
      case 3:
        for (x of TWO_CELLS) {
          for (k = 1; k < x.length; k++) {
            grid[x[0]][x[k]] = TWO;
          }
        }
        break;
      case 4:
        for (x of THREE_CELLS) {
          for (k = 1; k < x.length; k++) {
            grid[x[0]][x[k]] = THREE;
          }
        }
        break;
      case 5:
        for (x of FOUR_CELLS) {
          for (k = 1; k < x.length; k++) {
            grid[x[0]][x[k]] = FOUR;
          }
        }
        break;
      default:
        console.log("There was an error in the puzzle text file provided!");
    }
  }
};

/**
 * HANDLER FUNCTIONS
 */

const renderGrid = () => {
  for (i = 0; i < 7; i++) {
    for (j = 0; j < 7; j++) {
      renderCell(grid[j][i], `${j},${i}`);
    }
  }
};

const renderCell = (CELL_STATUS, id) => {
  const gridBox = document.getElementById("grid-box");
  let itemClass = "";
  let innerText = "";
  let cell = document.createElement("div");
  switch (CELL_STATUS) {
    case EMPTY:
      itemClass = "selectable";
      break;
    case BLACK:
      itemClass = "non-selectable black";
      break;
    case ZERO:
      itemClass = "non-selectable zero";
      innerText = "0";
      break;
    case ONE:
      itemClass = "non-selectable one";
      innerText = "1";
      break;
    case TWO:
      itemClass = "non-selectable two";
      innerText = "2";
      break;
    case THREE:
      itemClass = "non-selectable three";
      innerText = "3";
      break;
    case FOUR:
      itemClass = "non-selectable four";
      innerText = "4";
      break;
  }
  cell.appendChild(document.createTextNode(innerText));
  cell.className = itemClass;
  cell.id = `${id}`;
  cell.onclick = toggleCell;
  gridBox.appendChild(cell);
  // gridBox.innerHTML += `<div class="${itemClass}" id="${id}">${innerText}</div>`;
};

const toggleCell = e => {
  if (e.target.tagName == "IMG") {
    toggleSides(e.target.parentNode);
    if (e.target.parentNode.className.includes("selected")) {
      e.target.parentNode.className = e.target.parentNode.className.split("selected").join("").trim();
      e.target.remove();
    }
  } else {
    const coords = e.target.id.split(",").map(num => parseInt(num));
    if (isBlack(coords[0], coords[1])) 
      return;
    toggleSides(e.target);
    if (!e.target.className.includes("selected")) {
      e.target.className += " selected";
      e.target.innerHTML = "<img src='images/bulb.png'>";
    } else {
      e.target.className = e.target.parentNode.className.split("selected").join("").trim();
      e.target.innerHTML = "";
    }
  }
};

const toggleSides = node => {
  const coords = node.id.split(",").map(num => parseInt(num));

  // Traversal to the left
  for (x = coords[0] - 1; x >= 0; x--) {
    if (x < 0 || isBlack(x, coords[1])) 
      break;
    const id = x + "," + coords[1];
    let neighbourCell = document.getElementById(id);
    if (neighbourCell.className.includes("lit")) {
      neighbourCell.className = neighbourCell.className.split("lit").join("").trim();
    } else {
      neighbourCell.className += " lit";
    }
  }

  // Traversal to the right
  for (x = coords[0] + 1; x <= 6; x++) {
    if (x > 6 || isBlack(x, coords[1])) 
      break;
    const id = x + "," + coords[1];
    let neighbourCell = document.getElementById(id);
    if (neighbourCell.className.includes("lit")) {
      neighbourCell.className = neighbourCell.className.split("lit").join("").trim();
    } else {
      neighbourCell.className += " lit";
    }
  }

  // Traversal upwards
  for (y = coords[1] - 0; y >= 0; y--) {
    if (y < 0 || isBlack(coords[0], y)) 
      break;
    const id = coords[0] + "," + y;
    let neighbourCell = document.getElementById(id);
    if (neighbourCell.className.includes("lit")) {
      neighbourCell.className = neighbourCell.className.split("lit").join("").trim();
    } else {
      neighbourCell.className += " lit";
    }
  }

  // Traversal downwards
  for (y = coords[1] + 1; y <= 6; y++) {
    if (y > 6 || isBlack(coords[0], y)) 
      break;
    const id = coords[0] + "," + y;
    let neighbourCell = document.getElementById(id);
    if (neighbourCell.className.includes("lit")) {
      neighbourCell.className = neighbourCell.className.split("lit").join("").trim();
    } else {
      neighbourCell.className += " lit";
    }
  }
};

const isBlack = (x, y) => {
  return [
    BLACK,
    ZERO,
    ONE,
    TWO,
    THREE,
    FOUR
  ].includes(grid[x][y]);
};

const findLitClasses = classString => {
  const classStringArray = classString.split(" ");
  let count = 0;
  for (x of classStringArray) {
    if (x == "lit") 
      count++;
    }
  return count;
};

parseGrid(exampleLevel);
renderGrid();
