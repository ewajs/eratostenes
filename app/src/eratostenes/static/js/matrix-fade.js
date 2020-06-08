function shuffle(a) {
  var j, x, i;
  for (i = a.length - 1; i > 0; i--) {
    j = Math.floor(Math.random() * (i + 1));
    x = a[i];
    a[i] = a[j];
    a[j] = x;
  }
  return a;
}

function fadePictureInOut(i) {
  var item = elementList[i];
  function fade() {
    $(item).fadeTo(6700, 0);
    $(item).fadeTo(6700, 1, fade);
  }
  return fade;
}

var elementList = document
  .getElementById("fadeMatrix")
  .getElementsByTagName("img");

var indexList = shuffle(Array.from(new Array(elementList.length), (x, i) => i));

for (var i = 0; i < elementList.length; i++) {
  var index = indexList.pop();
  (function (i) {
    var timeToStartFade = 1700 * i;
    setTimeout(fadePictureInOut(index), timeToStartFade);
  })(i);
}
