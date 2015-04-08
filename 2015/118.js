function (game, team1, team2) {
	var CONF_SOS = {
    	"BIG12": 1,
    	"BIGE": 2,
    	"ACC": 3,
    	"BIG10": 4,
        "SEC": 5,
    	"PAC12": 6,
    	"ATL10": 7,
    	"AAC": 8,
    	"WCC": 9,
        "MIDAM": 10,
        "MWC": 11,
    	"MVC": 12,
    	"IND": 13,
    	"BIGW": 14,
    	"IVY": 15,
    	"HORIZ": 16,
    	"USA": 17,
    	"PAT": 18,
    	"COL": 19,
    	"BELT": 20,
    	"SUMM": 21,
    	"MAAC": 22,
    	"SOUTH": 23,
    	"OVC": 24,
    	"BSOU": 25,
    	"NEA": 26,
    	"BSKY": 27,
    	"LAND": 28,
    	"AEAST": 29,
    	"ASUN": 30,
    	"WAC": 31,
    	"MEAC": 32,
    	"SWAC": 33
    };

	var getValue = function(team) {
		var val = 0;

		val += (team.rpi/CONF_SOS[team.conf])/4;

		val += (team.field_goals_made/team.games_played)/70;

		val += (team.reb_per_game/45 + team.blocks_per_game/5 + team.steals_per_game/5)/(20 * CONF_SOS[team.conf] * team.win_pct);

		val -= (team.turnovers_per_game/10);

		val += team.rpi*team.win_pct;

		val += 5.5/Math.sqrt(team.official_rank+15);

		if(team.name === 'Ole Miss') {
			val *= team.rpi;
		}
		if(team.name === 'Kansas') {
		    val -= 0.5;
		}
		if(team.name === 'Louisville') {
		    val -= 0.5;
		}
		if(team.name === 'Georgetown') {
		    val -= 0.5;
		}
		if(team.name === 'Baylor') {
		    val -= 0.5;
		}
		if(team.name === 'Virginia') {
		    val += 0.25;
		}
		if(team.name === 'Kentucky') {
		    val += 2; // Kentucky bias
		}
		if(team.seed === 12) {
		    val += 0.2;
		}
		if(team.seed === 11) {
		    val += 0.1;
		}

		return val;
	}

	var team1Value = getValue(team1);
	var team2Value = getValue(team2);

	var seedDiff = Math.abs(team1.seed-team2.seed);
	if (seedDiff > 1) {
	    seedDiff -= 1.5;
	}
	if (seedDiff === 0) {
		seedDiff = 0.2;
	}
	// the closer the seeds, the more randomness matters
	if (team1Value > team2Value) {
		team2Value += Math.random() * 1.96 / seedDiff;
	} else {
		team1Value += Math.random() * 1.96 / seedDiff;
	}
	if (Math.random() > 0.5) {
	    team1Value += Math.random();
	} else {
	    team2Value += Math.random();
	}

  if (team1Value > team2Value) {
    team1.winsGame();
  } else {
    team2.winsGame();
  }
}