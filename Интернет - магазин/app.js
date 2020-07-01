// создадим массив объектов - описаний товаров
var goods = [
  {
    name: "Компьютер",
    price: 500,
    source: "OOO",
    classIdent: "ident_1",
  },
  {
    name: "Мышка",
    price: 10,
    source: "OOO",
    classIdent: "ident_2",
  },
  {
    name: "Камера",
    price: 50,
    source: "OOO",
    classIdent: "ident_3",
  },
  {
    name: "Коврик",
    price: 5,
    source: "OOO",
    classIdent: "ident_4",
  },
];

// создадим функцию, генерирующую разметку для отдельного товара, в качестве аргумента получает объект товара - элемент из массива goods
function renderItem(good) {
  let container = document.getElementById("container");
  let div_block = document.createElement("div");
  div_block.setAttribute("class", "block_of_item");
  let idForBlock = good.classIdent;
  div_block.setAttribute("id", idForBlock);

  let div_p_name = document.createElement("p");
  let div_p_price = document.createElement("p");
  let button = document.createElement("button");

  button.setAttribute("class", "btn");
  button.innerHTML = "Купить";
  button.onclick = hendler; // назначим обработчик события клика на кнопке
  div_p_name.innerHTML = good.name;
  div_p_price.innerHTML = good.price;
  div_block.appendChild(div_p_name);
  div_block.appendChild(div_p_price);
  div_block.appendChild(button);
  container.appendChild(div_block);
}

// функция - обработчик события клика на кнопке "Купить"
function hendler(e) {
  let parent = e.target.parentElement; // получаем родительский элемент
  // console.log(parent);
  let ident = parent.id + "_inBasket"; // делаем строку для id
  //console.log(ident);
  let childs = parent.getElementsByTagName("p");

  if (document.getElementById(ident)) {
    // если такой товар уже есть в корзине, мы увеличиваем только количество штук
    let itemInBasket = document.getElementById(ident);
    let quant = itemInBasket.querySelector("span").innerHTML.split(" ")[5];
    console.log(quant);
    quant = parseInt(quant) + 1;
    itemInBasket.querySelector("span").innerHTML =
      "name: " +
      childs[0].innerHTML +
      ", price: " +
      childs[1].innerHTML +
      " quantity: " +
      quant +
      " pc";
  } else {
    // иначе, создаём новую позицию в корзине с количеством 1 шт.
    let str =
      "name: " +
      childs[0].innerHTML +
      ", price: " +
      childs[1].innerHTML +
      " quantity: 1 pc";
    // console.log(str);
    addToBasket(str, ident); // функция добавления товара в корзину
  }
  sumInBasket();
}

// функция добавления товара в корзину, будет колл-бек функцией в функции hendler
function addToBasket(str, ident) {
  let item = document.getElementById("basket");
  let oneItem = document.createElement("div");
  oneItem.setAttribute("id", ident);
  let oneItemStr = document.createElement("span");
  let oneItemBtn = document.createElement("button");
  oneItemBtn.onclick = deliteItem;

  oneItemStr.innerHTML = str + "   ";
  oneItemBtn.innerHTML = "удалить";

  oneItem.appendChild(oneItemStr);
  oneItem.appendChild(oneItemBtn);
  item.appendChild(oneItem);
}

// функция удаления товара из корзины по 1 шт.

function deliteItem(e) {
  let blockItem = e.target.parentElement;
  let arrIdChild = blockItem.id.split("_");
  let idChild = arrIdChild[0] + "_" + arrIdChild[1];
  let childs = document.getElementById(idChild).querySelectorAll("p");

  let quant = blockItem.querySelector("span").innerHTML.split(" ")[5];
  quant = parseInt(quant) - 1;
  blockItem.querySelector("span").innerHTML =
    "name: " +
    childs[0].innerHTML +
    ", price: " +
    childs[1].innerHTML +
    " quantity: " +
    quant +
    " pc";

  if (quant == 0) {
    blockItem.remove();
  }
  sumInBasket();
}

// функция очистки корзины
function cleanBasket() {
  document.getElementById("basket").innerHTML = "";
  sumInBasket();
}

// функция подсчёта стоимости товаров в корзине. Вызываем её в конце функций покупки, удаления товара, очистки корзины, т.е. каждый раз как происходит изменения в корзине, мы пересчитываем сумму заново
function sumInBasket() {
  let itemsInBasket = document.getElementById("basket").querySelectorAll("div"); //массив из элементов корзины
  let sum = 0;
  itemsInBasket.forEach((item) => {
    let arrItem = item.querySelector("span").innerHTML.split(" ");
    let priceItem = parseInt(arrItem[3]) * parseInt(arrItem[5]);
    sum += priceItem;
  });
  console.log(sum);
  document.getElementById("totalPrice").innerHTML = sum;
}

// назначим кнопке "Очистить корзину" обработчик клика - функции очистки корзины
document.getElementById("clean_basket").onclick = cleanBasket;

// сгенерируем разметку для каждого товара - элемента массива goods
goods.forEach((good) => {
  renderItem(good);
});

// сделать функцию удаления товара из корзины по 1 шт, эта функция будет
// назначена
// обработчиком клика кнопки "удалить" в корзине. Так же сделать кнопку
// очистить корзину.
