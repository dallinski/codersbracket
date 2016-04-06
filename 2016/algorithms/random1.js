function (game, team1, team2) {
  if (Math.random() * Math.log(team1.seed+1) < Math.random() * Math.log(team2.seed+1)) {
    team1.winsGame();
  } else {
    team2.winsGame();
  }
}