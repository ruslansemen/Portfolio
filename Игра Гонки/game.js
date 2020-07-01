var tm;
var cars;
var cx;
var gameBegin;

var summa = parseInt(prompt("Введите вашу сумму"));
var c = prompt("На какую машину (от 0 до 4) вы делаете ставку");
var stavka = parseInt(prompt("Сколько вы ставите на выигрыш"));

function go() {
  if (gameBegin == 1) {
    return;
  }
  gameBegin = 1;
  cars = [];
  for (var i = 0; i < 5; i++) {
    cars[i] = document.getElementById("p" + i);
    cars[i].style.border = "none";
  }

  cx = new Array();
  for (var i = 0; i < 5; i++) {
    cx[i] = 680;
  }

  tm = window.setInterval(timerGo, 50);
}


function timerGo() {
  for (var i = 0; i < 5; i++) {
    //случайный шаг перемещения для автомобиля
    cx[i] = cx[i] - Math.floor(Math.random() * 7 + 2);
    if (cx[i] <= 0) {
      window.clearInterval(tm);
      gameBegin = 0;
      if (i == c) {
        summa += stavka;
        alert("Вы победили! Ваша сумма = " + summa);
      } else {
        alert("Вы проиграли. До финиша доехала машина с номером " + i);
        summa -= stavka;
        alert("Ваша сумма = " + summa);

        if (summa <= 0) {
          alert("Вы проиграли все деньги! Для продолжения перезагрузите страницу.");
          gameBegin = 1;
        }
      }
      cars[i].style.border = "5px ridge yellow";
      return;
    }
    cars[i].style.left = cx[i] + "px";
  }
}