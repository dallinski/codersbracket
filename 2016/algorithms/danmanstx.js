// A blantant rip-off of a 2015 algorithm made by danmanstx
// Even though it wasn't the top bracket, I liked the results it gave.
function (game, team1, team2) {
  // fail fast because no 15 or 16 will win
  if (team2.seed > 14){
      team1.winsGame();
  }

  var rand1 = Math.random();
  var rand2 = Math.random();
  var log_t1_seed = Math.log((1-team1.rpi)+1);
  var log_t2_seed = Math.log((1-team2.rpi)+1);

  // arrays containing the seeds historic probability to win
  // since 1985 from http://www.collegehoopsnet.com/ncaa-tournament-odds-a-seed-advancing-166169
  // array is by round starting with 64,32,16,8,4,2 then seed 1 to 16
  var chanceToWin   = [[  100, 95.7, 83.7, 80.4, 69.6, 68.5, 64.1, 45.7, 54.3, 35.9, 31.5, 31.5, 19.6, 16.3, 4.3, 0.0],
                      [  87.0, 63.0, 47.8, 43.5,   37,   38, 19.6,  9.8,  3.3, 17.4, 12.0, 15.2,  4.3,  2.2, 0.0, 0.0],
                      [  70.7, 46.7, 22.8, 15.2,  5.4, 13.0,  6.5,  6.5,  1.1,  6.5,  4.3,  1.1,  0.0,  0.0, 0.0, 0.0],
                      [  41.3, 22.8, 13.0,  9.8,  4.3,  3.3,  0.0,  3.3,  0.0,  0.0,  2.2,  0.0,  0.0,  0.0, 0.0, 0.0],
                      [  22.8, 10.9,  8.7,  2.2,  2.2,  2.2,  0.0,  1.1,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0, 0.0],
                      [  14.1,  4.3,  3.3,  1.1,  0.0,  1.1,  0.0,  1.1,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0, 0.0]];

  // set teams historic chance to win as a base line at 35% chance to win
  var team1Chance = chanceToWin[5-game.round][team1.seed-1] * rand1 * .35 / 100;
  var team2Chance = chanceToWin[5-game.round][team2.seed-1] * rand2 * .35 / 100;

  // CALCULATE THE TEAMS POSSESSIONS
  var team1Possessions = (team1.field_goals_attempted - team1.off_reb + team1.turnovers + 0.475 * team1.free_throws_attempted );
  var team2Possessions = (team2.field_goals_attempted - team2.off_reb + team2.turnovers + 0.475 * team2.free_throws_attempted );

  // CALCULATE THE TEAMS TOTAL POINTS
  var team1Points = ( team1.field_goals_made * 2) + team1.threes_made + team1.free_throws_made;
  var team2Points = ( team2.field_goals_made * 2) + team2.threes_made + team2.free_throws_made;

  // CALCULATE POINTS PER 100 POSSESSION
  var team1PointsPerPossession = ( team1Points / team1Possessions ) * 100;
  var team2PointsPerPossession = ( team2Points / team2Possessions ) * 100;

  // CALCULATE THE TEAMS BIG FOUR
  // OFFENSE
  // set teams effective shooting percentage    counts for (30%)
  var team1effShootingPercentage = ( ( 0.5 * team1.threes_made + team1.field_goals_made ) / team1.field_goals_attempted );
  var team2effShootingPercentage = ( ( 0.5 * team2.threes_made + team2.field_goals_made ) / team2.field_goals_attempted );
  // set teams free throw made per possession   counts for (20%)
  // https://harvardsportsanalysis.wordpress.com/2011/02/21/re-examining-the-four-factors-the-case-for-free-throws-made-per-100-possessions/
  var team1FreeThrowRate = (team1.free_throws_made / team1Possessions);
  var team2FreeThrowRate = (team2.free_throws_made / team2Possessions);
  // set teams turnover rate                    counts for (35%)
  var team1TurnoverRate = (team1.turnovers / team1Possessions);
  var team2TurnoverRate = (team2.turnovers / team2Possessions);
  // set teams rebounding rate                  counts for (15%)
  var team1ReboundRate = (team1.off_reb / (team1.off_reb+team2.def_reb));
  var team2ReboundRate = (team2.off_reb / (team2.off_reb+team1.def_reb));

  // set four factors to be 25% of total
  var team1FourFactors = ( team1effShootingPercentage * .3 ) + ( team1FreeThrowRate * .2 ) + ( team1ReboundRate * .35 ) - ( team1TurnoverRate * .15 ) * .15;
  var team2FourFactors = ( team2effShootingPercentage * .3 ) + ( team2FreeThrowRate * .2 ) + ( team2ReboundRate * .35 ) - ( team2TurnoverRate * .15 ) * .15;

  // absolute value of the difference in points per possession for 25% for higher and 18.75% for fewer
  var offense = Math.abs( team1PointsPerPossession - team2PointsPerPossession ) / 30 * .25;

  // some odd defensive calculation with assist for 25%!
  var team1defense = ( ( team1.steals_per_game + team1.blocks_per_game + team1.assists_per_game - 2 ) / 20 ) * .25;
  var team2defense = ( ( team2.steals_per_game + team2.blocks_per_game + team2.assists_per_game - 2 ) / 20 ) * .25;

  team1Chance += team1FourFactors;
  team2Chance += team2FourFactors;


  if ( team1PointsPerPossession > team2PointsPerPossession){
     team1Chance += offense;
     team2Chance += offense * .75;
  }
  else {
    team2Chance += offense;
    team1Chance += offense * .75;
  }

  team1Chance += team1defense;
  team2Chance += team2defense;

  if(team1Chance >= team2Chance){
      team1.winsGame();
  }
  else{
      team2.winsGame();
  }

}