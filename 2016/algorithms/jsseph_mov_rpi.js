// A blantant rip-off of a 2015 algorithm made by jsseph (5:1 MOV:RPI)
// Even though it wasn't the top bracket, I liked the results it gave.
function (game, team1, team2) {
	var poss_pg1 = team1.field_goals_attempted/team1.games_played + team1.turnovers_per_game +team1.free_throws_attempted/2;
	var poss_pg2 = team2.field_goals_attempted/team2.games_played + team2.turnovers_per_game +team2.free_throws_attempted/2;

	var norm_possessions = (poss_pg1 + poss_pg2)/2;

	var fga_pg1 = team1.field_goals_attempted/team1.games_played;
	var fga_pg2 = team2.field_goals_attempted/team2.games_played;

	var shotvalue1 = ((team1.field_goals_made-team1.threes_made)*2 + team1.threes_made*3)*team1.field_goals_made;
	var shotvalue2 = ((team2.field_goals_made-team2.threes_made)*2 + team2.threes_made*3)*team2.field_goals_made;

	var shots_base1 = (fga_pg1 + norm_possessions*fga_pg1/poss_pg1);
	var shots_base2 = (fga_pg2 + norm_possessions*fga_pg2/poss_pg2);

	var oreb_pg1 = team1.off_reb/team1.games_played;
	var oreb_pg2 = team2.off_reb/team2.games_played;

	var oreb_norm1 = (oreb_pg1 + norm_possessions*oreb_pg1/poss_pg1)/2;
	var oreb_norm2 = (oreb_pg2 + norm_possessions*oreb_pg2/poss_pg2)/2;

	var dreb_pg1 = team1.def_reb/team1.games_played;
	var dreb_pg2 = team2.def_reb/team2.games_played;

	var dreb_norm1 = (dreb_pg1 + norm_possessions*dreb_pg1/poss_pg1)/2;
	var dreb_norm2 = (dreb_pg2 + norm_possessions*dreb_pg2/poss_pg2)/2;

	var orebpct1 = oreb_norm1/(oreb_norm1 + dreb_norm2);
	var orebpct2 = oreb_norm2/(oreb_norm2 + dreb_norm1);

	var shots_missed_base1 = shots_base1*team1.field_goal_pct;
	var shots_missed_base2 = shots_base2*team2.field_goal_pct;

	var oreb_bonus1 = orebpct1*shots_missed_base1;
	var oreb_bonus2 = orebpct2*shots_missed_base2;

	var to_pg1 = team1.turnovers_per_game;
	var to_pg2 = team2.turnovers_per_game;

	var to_norm1 = (to_pg1 + norm_possessions*to_pg1/poss_pg1)/2;
	var to_norm2 = (to_pg2 + norm_possessions*to_pg2/poss_pg2)/2;

	var to_pen1 = to_norm1*-1;
	var to_pen2 = to_norm2*-1;

	var blk_pg1 = team1.blocks_per_game;
	var blk_pg2 = team2.blocks_per_game;

	var blk_norm1 = (blk_pg1 + norm_possessions*blk_pg1/poss_pg1)/2;
	var blk_norm2 = (blk_pg2 + norm_possessions*blk_pg2/poss_pg2)/2;

	var blk_bonus1 = blk_norm1*0.75;
	var blk_bonus2 = blk_norm2*0.75;


	var steal_pg1 = team1.steals_per_game;
	var steal_pg2 = team2.steals_per_game;

	var steal_norm1 = (steal_pg1 + norm_possessions*steal_pg1/poss_pg1)/2;
	var steal_norm2 = (steal_pg2 + norm_possessions*steal_pg2/poss_pg2)/2;

	var steal_bonus1 = steal_norm1*0.75;
	var steal_bonus2 = steal_norm2*0.75;

	var shots_adj1 = (shots_base1 + oreb_bonus1 + to_pen1 + blk_bonus1 + steal_bonus1);
	var shots_adj2 = (shots_base2 + oreb_bonus2 + to_pen2 + blk_bonus2 + steal_bonus2);

	var free_throw_pg1 = team1.free_throws_attempted/team1.games_played;
	var free_throw_pg2 = team2.free_throws_attempted/team2.games_played;

	var free_throw_norm1 = (free_throw_pg1 + norm_possessions*free_throw_pg1/poss_pg1)/2;
	var free_throw_norm2 = (free_throw_pg2 + norm_possessions*free_throw_pg2/poss_pg2)/2;

	var free_throw_bonus1 = free_throw_norm1*team1.free_throw_pct;
	var free_throw_bonus2 = free_throw_norm2*team2.free_throw_pct;

	var rpi_log1 = Math.log(team1.rpi)
	var rpi_log2 = Math.log(team2.rpi)

	var total = (shots_adj1*shotvalue1*team1.field_goal_pct + free_throw_bonus1)*team1.rpi + (shots_adj2*shotvalue2*team2.field_goal_pct + free_throw_bonus2)*team2.rpi

	var score1 = (shots_adj1*shotvalue1*team1.field_goal_pct + free_throw_bonus1)/total + 5*(shots_adj1*shotvalue1*team1.field_goal_pct + free_throw_bonus1)*team1.rpi/(shots_adj1*shotvalue1*team1.field_goal_pct + free_throw_bonus1);
	var score2 = (shots_adj2*shotvalue2*team2.field_goal_pct + free_throw_bonus2)/total + 5*(shots_adj2*shotvalue2*team2.field_goal_pct + free_throw_bonus2)*team2.rpi/(shots_adj2*shotvalue2*team2.field_goal_pct + free_throw_bonus2);

	if (score1 > score2){
		team1.winsGame();
	} else {
		team2.winsGame();
	}
       
}