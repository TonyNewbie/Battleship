/**
 * Получение стартового поля игрока с сервера и вызов отрисовки.
 */
function getStartBattlefields() {
  const request = new XMLHttpRequest();
  request.open('GET', 'api/startgame/');
  request.send();
  request.onload = function() {
    if (request.status !== 200) {
      $.notify(request.status + ': ' + request.statusText,
          {position: 'top center',
            className: 'error'}
      );
    } else {
      const response = JSON.parse(request.responseText);
      const playerField = response['player_field'];
      drawBattlefield(playerField);
    }
  };
}
/**
 * Отрисовка полей игрока и компьютера.
 * @param {Object} field
 */
function drawBattlefield(field) {
  const letters = ['', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К'];
  const playerTable = $('#player');
  const computerTable = $('#computer');
  playerTable.append('<tr id="player_navigation_row"></tr>');
  computerTable.append('<tr id="computer_navigation_row"></tr>');
  for (let i = 0; i < 11; i++) {
    $('#player_navigation_row')
        .append('<td class="navigation">' + letters[i] + '</td>');
    $('#computer_navigation_row')
        .append('<td class="navigation">' + letters[i] + '</td>');
  }
  for (let i = 0; i < 10; i++) {
    playerTable.append('<tr id="player_row_' + String(i) + '"></tr>');
    computerTable.append('<tr id="computer_row_' + String(i) + '"></tr>');
    for (let j = 0; j < 11; j++) {
      if (j === 0) {
        $('#computer_row_' + String(i))
            .append('<td class="navigation">' + String(i + 1) + '</td>');
        $('#player_row_' + String(i))
            .append('<td class="navigation">' + String(i + 1) + '</td>');
      } else {
        $('#computer_row_' + String(i))
            .append('<td class="unknown" id="' +
              String(i) + String(j - 1) + '"></td>');
        $('#' + String(i) + String(j - 1)).one('click', function() {
          playerShoot(String(i) + String(j - 1));
        });
        if (field[i][j - 1] === 1) {
          $('#player_row_' + String(i))
              .append('<td class="ship" id="' +
                String(i) + String(j - 1) + '"></td>');
        } else {
          $('#player_row_' + String(i))
              .append('<td class="empty" id="' +
                String(i) + String(j - 1) + '"></td>');
        }
      }
    }
  }
}
/**
 * Отправка запроса на сервер с координатами выстрела игрока.
 * @param {string} coord
 */
function playerShoot(coord) {
  const request = new XMLHttpRequest();
  request.open('GET', 'api/playershoot/' + coord + '/');
  request.send();
  request.onload = function() {
    if (request.status !== 200) {
      $.notify(request.status + ': ' + request.statusText,
          {position: 'top center',
            className: 'error'}
      );
    } else {
      const response = JSON.parse(request.responseText);
      drawChanges(response['fields']);
    }
  };
}
/**
 * Отрисовка изменений игры после ответа от сервера.
 * @param {Object} changes
 */
function drawChanges(changes) {
  const gameStatus = changes['game_status'];
  const playerChanges = changes['player_changes'];
  const computerChanges = changes['computer_changes'];
  for (const coord in playerChanges) {
    if (playerChanges.hasOwnProperty(coord) && playerChanges[coord] === 1) {
      $('#player').find('#' + coord).attr('class', 'hit');
    } else {
      $('#player').find('#' + coord).attr('class', 'miss');
    }
  }
  for (const coord in computerChanges) {
    if (computerChanges.hasOwnProperty(coord) && computerChanges[coord] === 1) {
      $('#computer').find('#' + coord).attr('class', 'hit');
    } else {
      $('#computer').find('#' + coord).attr('class', 'miss').unbind('click');
    }
  }
  if (gameStatus !== 'continue') {
    let message;
    if (gameStatus === 'player win') {
      message = 'Игрок победил!';
    } else {
      message = 'Компьютер победил!:(';
    }
    $.notify(message,
        {position: 'top center',
          className: 'success'});
    $('#computer').find('td').unbind('click');
  }
}
/**
 * Начало игры при загрузке страницы.
 */
$(document).ready(function() {
  getStartBattlefields();
});
