'use strict';

let view = {
    displayMessage: function (msg) {
        let messageArea = document.getElementById("messageArea");
        messageArea.innerHTML = msg;
    },
    displayHit: function (location) {
        let cell = document.getElementById(location);
        cell.setAttribute("class", "hit");
    },
    displayMiss: function (location) {
        let cell = document.getElementById(location);
        cell.setAttribute("class", "miss");
    }
}


let model = {
    boardSize: 7,
    numShips: 3,
    shipLength: 3,
    shipsSunk: 0,
    ships: [{
            locations: [0, 0, 0],
            hits: ["", "", ""]
        },
        {
            locations: [0, 0, 0],
            hits: ["", "", ""]
        },
        {
            locations: [0, 0, 0],
            hits: ["", "", ""]
        }
    ],
    fire: function (guess) {
        for (let i = 0; i < this.numShips; i++) {

            let ship = this.ships[i];
            let index = ship.locations.indexOf(guess);
            if (index >= 0) {
                // есть попадание
                ship.hits[index] = "hit";
                view.displayHit(guess);
                view.displayMessage("HIT! " + controller.guesses + " guesses");
                if (this.isSunk(ship)) {
                    view.displayMessage("You sank my battleship! " + controller.guesses + " guesses");
                    this.shipsSunk++;
                }
                return true;
            }
        }
        view.displayMiss(guess);
        view.displayMessage("You missed " + controller.guesses + " guesses");
        return false;
    },
    isSunk: function (ship) {
        for (let i = 0; i < this.shipLength; i++) {
            if (ship.hits[i] !== "hit") {
                return false;
            }
        }
        return true;
    },
    generateShipLocations: function () {
        let locations;
        for (let i = 0; i < this.numShips; i++) {
            do {
                locations = this.generateShip();
            } while (this.collision(locations));
            this.ships[i].locations = locations;
        }
    },
    generateShip: function () {

        let direction = Math.floor(Math.random() * 2);
        let row, col;

        if (direction === 1) {
            // сгенерировать начальную позицию горизонтального корабля
            row = Math.floor(Math.random() * this.boardSize);
            col = Math.floor(Math.random() * (this.boardSize - this.shipLength));
        } else {
            // сгенерировать начальную позицию вертикального корабля
            row = Math.floor(Math.random() * (this.boardSize - this.shipLength));
            col = Math.floor(Math.random() * this.boardSize);
        }

        let newShipLocations = [];
        for (let i = 0; i < this.shipLength; i++) {
            if (direction === 1) {
                // добавить массив для горизонтального корабля
                newShipLocations.push(row + "" + (col + i));
            } else {
                // добавить массив для вертикального корабля
                newShipLocations.push((row + i) + "" + col);
            }
        }
        return newShipLocations;
    },
    collision: function (locations) {
        // проверка на пересечение
        for (let i = 0; i < this.numShips; i++) {
            let ship = model.ships[i];
            for (let j = 0; j < locations.length; j++) {
                if (ship.locations.indexOf(locations[j]) >= 0) {
                    return true;
                }
            }
        }
        return false;
    }
};

// model.fire("53");

// model.fire("06");
// model.fire("16");
// model.fire("26");

// model.fire("34");
// model.fire("24");
// model.fire("44");

// model.fire("12");
// model.fire("11");
// model.fire("10");

// model.fire("66");
// model.fire("31");
// model.fire("43");

let controller = {
    playRun: true, // объявлено новое свойство, пока true  - игрок может делать выстрелы
    guesses: 0,
    processGuess: function (guess) {
        if (this.playRun) {
            let location = parseGuess(guess);
            if (location) {
                this.guesses++;
                let hit = model.fire(location);
                if (hit && model.shipsSunk === model.numShips) {
                    view.displayMessage("You sank all my battleships, in " + this.guesses + " guesses");
                    this.playRun = false; // ответ на мозговой штурм стр. 381 - игрок не сможет стрелять когда игра будет закончена
                }
            }
        } else {
            alert("Game over!");
        }

    }
};

function parseGuess(guess) {
    let alphabet = ["A", "B", "C", "D", "E", "F", "G"];

    if (guess === null || guess.length !== 2) {
        alert("Oops, please enter a letter and number on the board.");
    } else {
        let firstChar = guess.charAt(0);
        let row = alphabet.indexOf(firstChar);
        let column = guess.charAt(1);

        if (isNaN(row) || isNaN(column)) {
            alert("Oops, that isn't on the board.");
        } else if (row < 0 || row >= model.boardSize || column < 0 || column >= model.boardSize) {
            alert("Oops, that's off the board!");
        } else {
            return row + column;
        }
    }
    return null;
}

// console.log(parseGuess("A0"));
// console.log(parseGuess("B6"));
// console.log(parseGuess("G3"));
// console.log(parseGuess("H0"));
// console.log(parseGuess("A7"));

// controller.processGuess("A0");

// controller.processGuess("A6");
// controller.processGuess("B6");
// controller.processGuess("C6");

// controller.processGuess("C4");
// controller.processGuess("D4");
// controller.processGuess("E4");

// controller.processGuess("B0");
// controller.processGuess("B1");
// controller.processGuess("B2");

// controller.processGuess("A1");
// controller.processGuess("A2");

function init() {
    let fireButton = document.getElementById("fireButton");
    fireButton.onclick = handleFireButton;

    let guessInput = document.getElementById("guessInput");
    guessInput.onkeypress = handleKeyPress;

    let cellArr = document.getElementsByTagName("td");
    for (let i = 0; i < cellArr.length; i++) {
        cellArr[i].onclick = handleClickTd;
    }

    // Расставляем корабли случайным образом:
    model.generateShipLocations();
}

function handleClickTd(event) {
    let alphabet = ["A", "B", "C", "D", "E", "F", "G"];

    let arrOfClassElement = event.target.classList; // отладка
    console.log(arrOfClassElement); // отладка
    if (arrOfClassElement[0] !== "hit" && arrOfClassElement[0] !== "miss") {
        let guess = event.target.id;
        let firstSymbol = alphabet[guess[0]];
        let fullStr = firstSymbol + guess[1];
        controller.processGuess(fullStr);
    }
}

function handleFireButton() {
    let guessInput = document.getElementById("guessInput");
    let guess = guessInput.value.toUpperCase();

    let alphabet = ["A", "B", "C", "D", "E", "F", "G"];
    let firstSymbol = alphabet.indexOf(guess[0]);
    let fullStr = firstSymbol + guess[1];
    let arrOfClassElement = document.getElementById(fullStr).classList // отладка
    if (arrOfClassElement[0] !== "hit" && arrOfClassElement[0] !== "miss") {
        controller.processGuess(guess);
    }

    guessInput.value = "";
}

function handleKeyPress(e) {
    let fireButton = document.getElementById("fireButton");
    if (e.keyCode === 13) {
        fireButton.click();
        return false;
    }
}
window.onload = init;