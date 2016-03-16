// Predict Cinderella teams using principles outlined at http://www.ncaa.com/news/basketball-men/article/2016-01-30/march-madness-4-essential-ingredients-cinderella-run
// Normal logic applies for 1-8 seeds. Cinderllas must be a 9 seed or worse.
function (game, team1, team2) {
  // Have an elite offense (top 40 in adjusted offensive efficiency)
  // from kenpom.com
  var top40AdjustedOffTeams = [
    "Kentucky",
    "Michigan St.",
    "Iowa St.",
    "UNC",
    "Oregon",
    "Duke",
    "Indiana",
    "Kansas",
    "Virginia",
    "Notre Dame",
    "Villanova",
    "Miami (Fla.)",
    "Baylor",
    "Saint Mary's",
    "SMU",
    "Houston",
    "Arizona",
    "Xavier",
    "Butler",
    "Oklahoma",
    "Purdue",
    "Oakland",
    "West Virginia",
    "Gonzaga",
    "Iowa",
    "Maryland",
    "Utah",
    "Texas Tech",
    "Davidson",
    "St. Bonaventure",
    "St. Joseph's",
    "Vanderbilt",
    "Pittsburgh",
    "North Carolina St.",
    "Michigan",
    "Texas A&M",
    "Southern California",
    "William & Mary",
    "North Florida",
    "Clemson"
  ];

  // Shoot the 3 (top 20 in 3-point attempts per game)
  // from espn.com
  var top20ThreeTeams = [
    "The Citadel",
    "Akron",
    "Marshall",
    "North Florida",
    "Lipscomb",
    "Hartford",
    "Colorado State",
    "UT-Arlington",
    "Belmont",
    "Elon",
    "Central Michigan",
    "Eastern Washington",
    "Iona",
    "Davidson",
    "Wyoming",
    "Michigan",
    "Villanova",
    "Army",
    "Milwaukee",
    "IPFW"
  ];

  // Be at least average on defense (top 84 in adjusted defensive efficiency)
  // from kenpom.com
  var top84AdjustedDefTeams = [
    "Wichita St.",
    "San Diego St.",
    "Louisville",
    "Virginia",
    "Kansas",
    "West Virginia",
    "Villanova",
    "Cincinnati",
    "College of Charleston",
    "Valparaiso",
    "Oklahoma",
    "Texas A&M",
    "Connecticut",
    "Dayton",
    "California",
    "UNC",
    "Seton Hall",
    "Purdue",
    "Michigan St.",
    "Florida",
    "Yale",
    "VCU",
    "South Carolina",
    "Wisconsin",
    "Cal St. Bakersfield",
    "Colorado",
    "Stephen F. Austin",
    "Providence",
    "Nevada",
    "Kansas St.",
    "Iowa",
    "Texas",
    "New Mexico St.",
    "Vanderbilt",
    "Little Rock",
    "Xavier",
    "Maryland",
    "Syracuse",
    "Ohio St",
    "Arizona",
    "Hawaii",
    "Georgia",
    "SMU",
    "Miami (Fla.)",
    "Northern Iowa",
    "Evansville",
    "Creighton",
    "Alabama",
    "Monmouth",
    "Oregon",
    "Utah",
    "Temple",
    "TCU",
    "Memphis",
    "Gonzaga",
    "Washington",
    "Oklahoma St.",
    "UC Irvine",
    "Wright St.",
    "UNC-Asheville",
    "Stony Brook",
    "Oregon St.",
    "UC Davis",
    "James Madison",
    "Illinois St.",
    "Indiana",
    "Rhode Island",
    "North Dakota St.",
    "UC Santa Barbara",
    "Kentucky",
    "Middle Tennessee",
    "Baylor",
    "UNLV",
    "St. Joseph's",
    "UT Arlington",
    "BYU",
    "Chattanooga",
    "Virginia Tech",
    "Northwestern",
    "Mississippi St.",
    "Long Beach St.",
    "Indiana St.",
    "Mount St. Mary's",
    "Tulsa"
  ];

  // Rebound well (top 40 in rebounds per game)
  // from espn.com
  var top40ReboundTeams = [
    "UT Arlington",
    "Quinnipiac",
    "George Mason",
    "Colorado",
    "Valparaiso",
    "Michigan St.",
    "Hampton",
    "Louisiana Lafayette",
    "New Mexico State",
    "Purdue",
    "UIC",
    "BYU",
    "Xavier",
    "North Carolina",
    "South Carolina",
    "Nevada",
    "Memphis",
    "Army",
    "Siena",
    "Yale",
    "Arizona",
    "Florida Gulf Coast",
    "Wagner",
    "Florida",
    "Mercer",
    "Arkansas State",
    "Seton Hall",
    "Colorado State",
    "Jackson State",
    "California",
    "Washington",
    "Oakland",
    "Gonzaga",
    "UCLA",
    "NC State",
    "Stony Brook",
    "Southern California",
    "SMU",
    "Cincinnati",
    "San Francisco"
  ];


  var team1CinderellaPoints = 0;
  if (top40AdjustedOffTeams.indexOf(team1.name) > -1) {
    team1CinderellaPoints += 1;
  }

  if (top20ThreeTeams.indexOf(team1.name) > -1) {
    team1CinderellaPoints += 1;
  }

  if (top84AdjustedDefTeams.indexOf(team1.name) > -1) {
    team1CinderellaPoints += 1;
  }

  if (top40ReboundTeams.indexOf(team1.name) > -1) {
    team1CinderellaPoints += 1;
  }

  var team2CinderellaPoints = 0;
  if (top40AdjustedOffTeams.indexOf(team2.name) > -1) {
    team2CinderellaPoints += 1;
  }

  if (top20ThreeTeams.indexOf(team2.name) > -1) {
    team2CinderellaPoints += 1;
  }

  if (top84AdjustedDefTeams.indexOf(team2.name) > -1) {
    team2CinderellaPoints += 1;
  }

  if (top40ReboundTeams.indexOf(team2.name) > -1) {
    team2CinderellaPoints += 1;
  }

  var team1Odds = Math.random() * Math.log(team1.seed+1);
  var team2Odds = Math.random() * Math.log(team2.seed+1);

  if (team1.seed > 8 && team1CinderellaPoints > 1) {
    team1Odds -= Math.log(team1CinderellaPoints)/2;
  }
  if (team2.seed > 8 && team2CinderellaPoints > 1) {
    team2Odds -= Math.log(team2CinderellaPoints)/2;
  }

  if (team1Odds < team2Odds) {
    team1.winsGame();
  } else {
    team2.winsGame();
  }
}