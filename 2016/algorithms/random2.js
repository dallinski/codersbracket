// A blantant rip-off of a 2015 algorithm made by GriffinLovesSports (AVG Point Weighted Bracket)
// Even though it wasn't the top bracket, I liked the results it gave.
function (game, team1, team2) {  
  var log_t1_seed = (2*team1.free_throws_made+3*team1.threes_made)/team1.games_played;
  var log_t2_seed = (2*team2.free_throws_made+3*team2.threes_made)/team2.games_played;
  
  if (team1.seed > team2.seed + 4 && Math.random() < .9) {
    team2.winsGame();
  } else if (team2.seed > team1.seed + 4 && Math.random() < .9) {
    team1.winsGame();
  } else if (Math.random()*log_t1_seed < Math.random()*log_t2_seed) {
    team1.winsGame();
  } else {
    team2.winsGame();
  }      
}