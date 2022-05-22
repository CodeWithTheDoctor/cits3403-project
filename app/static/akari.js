/**
 * EXAMPLE
 */
// const a = "03 213 33 435 63\n"+
// "30\n"+
// "326\n"+
// "34 52\n"+
// "\n"+
// "14";

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
  const coords = puzzleString.split("z");
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

/**
 * Function for rendering the grid to the page by adding nodes for each cell to the grid-wrapper div container.
 */
const renderGrid = () => {
  for (i = 0; i < 7; i++) {
    for (j = 0; j < 7; j++) {
      renderCell(grid[j][i], `${j},${i}`);
    }
  }
};

/**
 * Function for adding a node for a cell to the page
 * @param {number} CELL_STATUS The state of the cell (eg. Empty, Black, Zero, One, etc.)
 * @param {string} id The id of the cell, which is also the coordinate of the cell on the grid, in the form "x,y".
 */
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
};

/**
 * Function for adding/removing a lightbulb from a cell.
 * @param {Event} e
 */
const toggleCell = e => {
  if (e.target.tagName == "IMG") {
    removeSides(e.target.parentNode);
    e.target.parentNode.className = e.target.parentNode.className.split("selected").join("").trim();
    e.target.remove();
  } else {
    const coords = e.target.id.split(",").map(num => parseInt(num));
    if (isBlack(coords[0], coords[1])) 
      return;
    if (!e.target.className.includes("selected")) {
      addSides(e.target);
      e.target.className += " selected";
      e.target.innerHTML = "<img src='static/images/bulb.png'>";
    } else {
      removeSides(e.target);
      e.target.className = e.target.parentNode.className.split("selected").join("").trim();
      e.target.innerHTML = "";
    }
  }
};

/**
 * Lights up the cells neighbouring the cell that a light-bulb has been added to
 * @param {Node} node instance of a DOM node
 */
const addSides = node => {
  const coords = node.id.split(",").map(num => parseInt(num));

  // Traversal to the left
  for (x = coords[0] - 1; x >= 0; x--) {
    if (x < 0 || isBlack(x, coords[1])) 
      break;
    const id = x + "," + coords[1];
    let neighbourCell = document.getElementById(id);
    neighbourCell.className += " lit";
  }

  // Traversal to the right
  for (x = coords[0] + 1; x <= 6; x++) {
    if (x > 6 || isBlack(x, coords[1])) 
      break;
    const id = x + "," + coords[1];
    let neighbourCell = document.getElementById(id);
    neighbourCell.className += " lit";
  }

  // Traversal upwards
  for (y = coords[1] - 0; y >= 0; y--) {
    if (y < 0 || isBlack(coords[0], y)) 
      break;
    const id = coords[0] + "," + y;
    let neighbourCell = document.getElementById(id);
    neighbourCell.className += " lit";
  }

  // Traversal downwards
  for (y = coords[1] + 1; y <= 6; y++) {
    if (y > 6 || isBlack(coords[0], y)) 
      break;
    const id = coords[0] + "," + y;
    let neighbourCell = document.getElementById(id);
    neighbourCell.className += " lit";
  }
};

/**
 * Removes a string of 'lit' class from neighbouring cells when a light bulb is removed from the cell.
 * @param {Node} node instance of a DOM node
 */
const removeSides = node => {
  const coords = node.id.split(",").map(num => parseInt(num));

  // Traversal to the left
  for (x = coords[0] - 1; x >= 0; x--) {
    if (x < 0 || isBlack(x, coords[1])) {
      break;
    }
    const id = x + "," + coords[1];
    let neighbourCell = document.getElementById(id);
    unlightCell(neighbourCell);
  }

  // Traversal to the right
  for (x = coords[0] + 1; x <= 6; x++) {
    if (x > 6 || isBlack(x, coords[1])) 
      break;
    const id = x + "," + coords[1];
    let neighbourCell = document.getElementById(id);
    unlightCell(neighbourCell);
  }

  // Traversal upwards
  for (y = coords[1] - 0; y >= 0; y--) {
    if (y < 0 || isBlack(coords[0], y)) 
      break;
    const id = coords[0] + "," + y;
    let neighbourCell = document.getElementById(id);
    unlightCell(neighbourCell);
  }

  // Traversal downwards
  for (y = coords[1] + 1; y <= 6; y++) {
    if (y > 6 || isBlack(coords[0], y)) 
      break;
    const id = coords[0] + "," + y;
    let neighbourCell = document.getElementById(id);
    unlightCell(neighbourCell);
  }
};

/**
 * Checks whether the grid cell is a black square or not
 * @param {number} x
 * @param {number} y
 * @returns {boolean} true | false
 */
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

/**
 * Remove a 'lit' substring from the classes of the provided element.
 * @param {Node} neighbourCell instance of a DOM node of a neighbouring cell
 */
const unlightCell = neighbourCell => {
  let numLits = findLitClasses(neighbourCell.className);
  let litStr = "";
  for (i = 0; i < numLits - 1; i++) 
    litStr += " lit";
  neighbourCell.className = neighbourCell.className.split("lit").join("") + litStr;
};

/**
 * Retreives the number of 'lit' strings present in the class field of the provided element.
 * @param {string} classString
 * @returns {number} number of 'lit' strings in the class field of the provided element
 */
const findLitClasses = classString => {
  const classStringArray = classString.split(" ");
  let count = 0;
  for (i = 0; i < classStringArray.length; i++) {
    if (classStringArray[i] == "lit") {
      count++;
    }
  }
  return count;
};

/**
 * Checks if the puzzle has been solved or not
 * @returns True if puzzle has been solved correcly
 */
const isSolved = () => {
  for (y = 0; y < 7; y++) {
    for (x = 0; x < 7; x++) {
      const id = x + "," + y;
      if (isBlack(x, y)) {
        if (grid[x][y] == BLACK) {
          continue;
        }
        let numBulbsRequired = grid[x][y] - ZERO;
        if (getNumBulbs(x, y) != numBulbsRequired) {
          return false;
        }
        continue;
      }
      const cell = document.getElementById(id);
      if (cell.className.includes("selected")) {
        if (canSeeBulb(x, y)) 
          return false;
        }
      else if (!cell.className.includes("lit")) {
        return false;
      }
    }
  }

  return true;
};

/**
 * Checks if there is another bulb in the line of sight to the specified cell
 * @param {number} x
 * @param {number} y
 * @returns true if there is a bulb in the line of sight, else false
 */
const canSeeBulb = (x, y) => {
  // Traversal to the left
  for (i = x - 1; i >= 0; i--) {
    if (i < 0 || isBlack(i, y)) {
      break;
    }
    const id = i + "," + y;
    let neighbourCell = document.getElementById(id);
    if (neighbourCell.className.includes("selected")) 
      return true;
    }
  
  // Traversal to the right
  for (i = x + 1; i <= 6; i++) {
    if (i > 6 || isBlack(i, y)) 
      break;
    const id = i + "," + y;
    let neighbourCell = document.getElementById(id);
    if (neighbourCell.className.includes("selected")) 
      return true;
    }
  
  // Traversal upwards
  for (j = y - 1; j >= 0; j--) {
    if (j < 0 || isBlack(x, j)) 
      break;
    const id = x + "," + j;
    let neighbourCell = document.getElementById(id);
    if (neighbourCell.className.includes("selected")) 
      return true;
    }
  
  // Traversal downwards
  for (j = y + 1; j <= 6; j++) {
    if (j > 6 || isBlack(x, j)) 
      break;
    const id = x + "," + j;
    let neighbourCell = document.getElementById(id);
    if (neighbourCell.className.includes("selected")) 
      return true;
    }
  
  return false;
};

/**
 * Function to retrieve the number of bulbs around a cell
 * @param {number} x
 * @param {number} y
 * @returns the number of bulbs surrounding a cell.
 */
const getNumBulbs = (x, y) => {
  let count = 0;
  if (x == 0) {
    if (y == 0) {
      let cell = document.getElementById(x + 1 + "," + y);
      if (cell.className.includes("selected")) 
        count++;
      cell = document.getElementById(x + "," + (
      y + 1));
      if (cell.className.includes("selected")) 
        count++;
      }
    else if (y == 6) {
      let cell = document.getElementById(x + "," + (
      y - 1));
      if (cell.className.includes("selected")) 
        count++;
      cell = document.getElementById(x + 1 + "," + y);
      if (cell.className.includes("selected")) 
        count++;
      }
    else {
      let cell = document.getElementById(x + 1 + "," + y);
      if (cell.className.includes("selected")) 
        count++;
      cell = document.getElementById(x + "," + (
      y + 1));
      if (cell.className.includes("selected")) 
        count++;
      cell = document.getElementById(x + "," + (
      y - 1));
      if (cell.className.includes("selected")) 
        count++;
      }
    } else if (x == 6) {
    if (y == 0) {
      let cell = document.getElementById(x - 1 + "," + y);
      if (cell.className.includes("selected")) 
        count++;
      cell = document.getElementById(x + "," + (
      y + 1));
      if (cell.className.includes("selected")) 
        count++;
      }
    else if (y == 6) {
      let cell = document.getElementById(x + "," + (
      y - 1));
      if (cell.className.includes("selected")) 
        count++;
      cell = document.getElementById(x - 1 + "," + y);
      if (cell.className.includes("selected")) 
        count++;
      }
    else {
      let cell = document.getElementById(x - 1 + "," + y);
      if (cell.className.includes("selected")) 
        count++;
      cell = document.getElementById(x + "," + (
      y + 1));
      if (cell.className.includes("selected")) 
        count++;
      cell = document.getElementById(x + "," + (
      y - 1));
      if (cell.className.includes("selected")) 
        count++;
      }
    } else if (y == 0) {
    let cell = document.getElementById(x - 1 + "," + y);
    if (cell.className.includes("selected")) 
      count++;
    cell = document.getElementById(x + "," + (
    y + 1));
    if (cell.className.includes("selected")) 
      count++;
    cell = document.getElementById(x + 1 + "," + y);
    if (cell.className.includes("selected")) 
      count++;
    }
  else if (y == 6) {
    let cell = document.getElementById(x - 1 + "," + y);
    if (cell.className.includes("selected")) 
      count++;
    cell = document.getElementById(x + "," + (
    y - 1));
    if (cell.className.includes("selected")) 
      count++;
    cell = document.getElementById(x + 1 + "," + y);
    if (cell.className.includes("selected")) 
      count++;
    }
  else {
    let cell = document.getElementById(x - 1 + "," + y);
    if (cell.className.includes("selected")) 
      count++;
    cell = document.getElementById(x + "," + (
    y - 1));
    if (cell.className.includes("selected")) 
      count++;
    cell = document.getElementById(x + 1 + "," + y);
    if (cell.className.includes("selected")) 
      count++;
    cell = document.getElementById(x + "," + (
    y + 1));
    if (cell.className.includes("selected")) 
      count++;
    }
  return count;
};
