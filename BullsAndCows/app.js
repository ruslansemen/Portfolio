// Быки и коровы
'use strict';

// Функция генерирующая 4 неповторяющихся числа
function generateNum() {
    let num;
    let arrNum = [];
    while (arrNum.length < 4) {
        num = Math.floor(Math.random() * 10);
        if (arrNum.indexOf(num) == -1) {
            arrNum.push(num);
        }
    }
    return arrNum;
}

// Функция преобразующая число  пользователя в массив
function convStrInNum(str) {
    let arrAnswer = str.split('');
    if (arrAnswer.length != 4) {
        alert('число должно быть 4 - значным');
        return false;
    } else {
        for (let i = 0; i < arrAnswer.length; i++) {
            arrAnswer[i] = parseInt(arrAnswer[i]);
        }
        return arrAnswer;
    }
}

// функция запроса числа у пользователя, возвращает числовой массив ответа пользователя 
function askAndGetNum() {
    let repeate;
    let userAnswNum;
    do {
        let userAnswStr = prompt('какое 4 значное число загадал компьютер?');
        userAnswNum = convStrInNum(userAnswStr);
        if (!userAnswNum) {
            repeate = true;
        } else {
            repeate = false;
            return userAnswNum;
        }
    } while (repeate);
}

// Игра:

//ПК генерирует массив чисел для угадывания 
let arrForGes = generateNum();
console.log(arrForGes);
alert(arrForGes);
let playContinue = true;
let countBulls, countCows;


while (playContinue) {
    let arrBulls = [];
    countBulls = 0;
    countCows = 0;
    // пользователь вводит свою отгадку
    let arrUserAnsw = askAndGetNum();
    // считаем быков
    for (let i = 0; i < arrForGes.length; i++) {
        if (arrForGes[i] == arrUserAnsw[i]) {
            countBulls++;
            arrBulls.push(i);
        }
    }

    // считаем коров
    for (let i = 0; i < arrUserAnsw.length; i++) {
        if (arrBulls.indexOf(i) == -1) {
            for (let j = 0; j < arrForGes.length; j++) {
                if ((arrUserAnsw[i] == arrForGes[j]) && (arrBulls.indexOf(j) == -1)) {
                    countCows++;
                }
            }
        }
    }


    alert("быки: " + countBulls + " " + "коровы: " + countCows);
    if (countBulls == 4) {
        playContinue = false;
        alert("Угадали!");
    } else {
        alert("Увы :(, попробуйте ещё раз");
    }
}
