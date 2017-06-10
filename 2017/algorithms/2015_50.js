function (game, team1, team2) {
	// updated to 2017 CONF_SOS stats
	var CONF_SOS = {
		"ACC": 1,
		"BIG12": 2,
		"BIGE": 3,
		"BIG10": 4,
		"SEC": 5,
		"PAC12": 6,
		"AAC": 7,
		"ATL10": 8,
		"WCC": 9,
		"MWC": 10,
		"COL": 11,
		"MVC": 12,
		"BELT": 13,
		"MIDAM": 14,
		"SOUTH": 15,
		"MAAC": 16,
		"HORIZ": 17,
		"SUMM": 18,
		"WAC": 19,
		"IVY": 20,
		"AEAST": 21,
		"PAT": 22,
		"USA": 23,
		"OVC": 24,
		"BSOU": 25,
		"ASUN": 26,
		"LAND": 27,
		"BSKY": 28,
		"BIGW": 29,
		"NEA": 30,
		"SWAC": 31,
		"MEAC": 32
	};

	var getValue = function(team) {
		var val = 0;

		val += (team.rpi/CONF_SOS[team.conf])/2.5;

		val += (team.field_goals_made/team.games_played)/70;

		if(team.field_goal_pct > 50) {
			val += (team.field_goal_pct - 50)/5;
		}
		if(team.free_throw_pct > 75) {
			val += (team.free_throw_pct - 75)/6;
		}
		if(team.three_point_pct > 40) {
			val += (team.three_point_pct - 40)/6;
		}

		val += (team.reb_per_game/45 + team.blocks_per_game/5 + team.steals_per_game/5)/(20 * CONF_SOS[team.conf] * team.win_pct);

		val -= (team.turnovers_per_game/10);

		val += team.rpi*team.win_pct;

		val += 5.5/Math.sqrt(team.official_rank+25);

		return val;
	}

	var team1Value = getValue(team1);
	var team2Value = getValue(team2);

	var seedDiff = Math.abs(team1.seed-team2.seed);
	if (seedDiff === 0) {
		seedDiff = 0.5;
	}
	// the closer the seeds, the more randomness matters
	if (team1Value > team2Value) {
		team2Value += Math.random() * 3 / seedDiff;
	} else {
		team1Value += Math.random() * 3 / seedDiff;
	}

	if (team1Value > team2Value) {
		team1.winsGame();
	} else {
		team2.winsGame();
	}
}