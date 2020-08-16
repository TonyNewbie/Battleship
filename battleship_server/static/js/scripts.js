function getStartBattlefields(){
    let request = new XMLHttpRequest();
    request.open('GET', 'api/startgame/');
    request.responseType = 'json';
    request.send();
    request.onload = function() {
        let response = request.response;
        let player_field = response['player_field']
        drawBattlefield(player_field);
    }
}

function drawBattlefield(field){
    for (let i = 0; i < 10; i++){
        $("#player").append('<tr id="player_row_' + String(i) + '"></tr>');
        $("#computer").append('<tr id="computer_row_' + String(i) + '"></tr>');
        for (let j = 0; j< 10; j++) {
            $('#computer_row_' + String(i)).append('<td id="' + String(i) + String(j) + '"></td>');
            $('#' + String(i) + String(j)).one('click', function (){
                playerShoot(this.id)
            });
            if (field[i][j] === 1){
                $('#player_row_' + String(i)).append('<td class="ship" id="' + String(i) + String(j) + '"></td>')
            }
            else {
                $('#player_row_' + String(i)).append('<td class="empty" id="' + String(i) + String(j) + '"></td>')
            }
        }
    }
}

function playerShoot(coord){
    let request = new XMLHttpRequest();
    request.open('GET', 'api/playershoot/' + coord + '/');
    request.responseType = 'json';
    request.send();
    request.onload = function() {
        let response = request.response;
        drawChanges(response['fields']);
    }
}

function drawChanges(changes){
    let gameStatus = changes['game_status'];
    let playerChanges = changes['player_changes'];
    let computerChanges = changes['computer_changes']
    for (let coord in playerChanges){
        if (playerChanges[coord] === 1){
            $('#player').find('#' + coord).attr('class', 'hit');
        } else {
            $('#player').find('#' + coord).attr('class', 'miss');
        }
    }
    for (let coord in computerChanges){
        if (computerChanges[coord] === 1){
            $('#computer').find('#' + coord).attr('class', 'hit');
        } else {
            $('#computer').find('#' + coord).attr('class', 'miss');
        }
    }
    if (gameStatus !== 'continue') {
        alert(gameStatus);
    }
}

$(document).ready(function (){
    getStartBattlefields();
});