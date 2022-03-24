var playerSymbol;
var enemySymbol;
var win;
var turn;
var row, column;
var cpuEnabled = true;
var suc;
var uid = "0";

$(document).ready(function() {
  $("#choose-x").on("click", function() {
    playerSymbol = "X";
    enemySymbol = "O";
    startGame();
  });
  $("#choose-o").on("click", function() {
    playerSymbol = "O";
    enemySymbol = "X";
    startGame();
  });
  
  $("#restart").on("click", function() {
    restartGame();
  });
  $(".cell").on("click", function() {
    if(!win && this.innerHTML === "") {
      if(turn%2 === 0) {
        insertSymbol(this, playerSymbol);
      }
      else {
        insertSymbol(this, enemySymbol);
      }
    }
  });
});


function insertSymbol(element, symbol) {
  element.innerHTML = symbol;

  if(turn%2 === 0)
    suc = $.getValues("/player_move/" + element.id + "/" + uid);
  
  if(symbol === enemySymbol)
    $("#" + element.id).addClass("player-two");
  $("#" + element.id).addClass("cannotuse");
  
  checkWinConditions(element);
  turn++;
  if(win || turn > 8) {
    $("#restart").addClass("btn-green");
    $(".cell").addClass("cannotuse");
  }
  else if(cpuEnabled && turn%2 !== 0) {
    cpuTurn();
  }
}

function startGame() {
  $("#intro-screen").fadeOut(300, showGameScreen);
  restartGame();
}
function showGameScreen() {
  $("#game-screen").fadeIn(300);
}
function showEnemyScreen() {
  $("#enemy-screen").fadeIn(300);
}

function restartGame() {
  turn = 0;
  win = false;

  suc = $.getValues("/delete_agent/" + uid);
  uid = $.getValues("/create_agent");
  uid = uid.data;

  $(".cell").text("");
  $(".cell").removeClass("wincell");
  $(".cell").removeClass("cannotuse");
  $(".cell").removeClass("player-two");
  $("#restart").removeClass("btn-green");
}

function checkWinConditions(element) {
  row = element.id[4];
  column = element.id[5];
  
  win = true;
  for(var i=0; i<3; i++) {
    if($("#cell" + i + column).text() !== element.innerHTML) {
      win = false;
    }
  }
  if(win) {
    for(var i=0; i<3; i++) {
      $("#cell" + i + column).addClass("wincell");
    }
    return;
  }
  
  
  win = true;
  for(var i=0; i<3; i++) {
    if($("#cell" + row + i).text() !== element.innerHTML) {
      win = false;
    }
  }
  if(win) {
    for(var i=0; i<3; i++) {
      $("#cell" + row + i).addClass("wincell");
    }
    return;
  }

  
  win = true;
  for(var i=0; i<3; i++) {
    if($("#cell" + i + i).text() !== element.innerHTML) {
      win = false;
    }
  }
  if(win) {
    for(var i=0; i<3; i++) {
      $("#cell" + i + i).addClass("wincell");
    }
    return;
  }

  
  win = false;
  if($("#cell02").text() === element.innerHTML) {
    if($("#cell11").text() === element.innerHTML) {
      if($("#cell20").text() === element.innerHTML) {
        win = true;
        $("#cell02").addClass("wincell");
        $("#cell11").addClass("wincell");
        $("#cell20").addClass("wincell");
      }
    }
  }
}


jQuery.extend({
  getValues: function(url) {
      var result = null;
      $.ajax({
          url: url,
          type: 'get',
          dataType: 'json',
          async: false,
          success: function(data) {
              result = data;
          }
      });
     return result;
  }
});

function cpuTurn() {
  var ok = false;
  var move;
  
  while(!ok) {

    move = $.getValues("/cpu_move/" + uid);

    if( $("#cell"+move.data).text() === "" ) {
      ok = true;
    }
  }

  
  $("#cell"+move.data).click();
}
