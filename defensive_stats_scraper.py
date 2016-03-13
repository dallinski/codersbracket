from bs4 import BeautifulSoup
from datetime import date
import urllib2
import json
import argparse


MIN_YEAR = 2010 # The NCAA stats pages only go back to 2010
CURRENT_YEAR = date.today().year
# define the columns given for a specific stat page on ncaa.com
STAT_PAGE_MAPPINGS = {
	149: {'opp_fg': 3, 'opp_fga': 4, 'opp_fg_per': 5}, # defensive fg%
	518: {'opp_3p_fga': 3, 'opp_3p_fg': 4, 'opp_3p_fg_per': 5}, # def 3pt fg%
	931: {'opp_tot_to': 3, 'opp_topg': 4}, # turnovers forced
	519: {'opp_tot_to': 3, 'to_ratio': 5}, # turnover margin
	151: {'opp_tot_reb': 5, 'opp_rpg': 6, 'reb_margin': 7}, # rebound margin
	147: {'own_tot_pts': 3, 'own_ppg': 4, 'opp_tot_pts': 5, 'opp_ppg': 6, 'pts_margin': 7}, # scoring margin
	146: {'opp_tot_pts': 3, 'opp_ppg': 4}, # scoring defense
	286: {'tot_pf': 3, 'pfpg': 4, 'dq': 5} # fouls per game
}
# The NCAA stat pages and CodersBracket.com use different names for some teams.
NCAA_MAPPINGS = {
#   NCAA name: CodersBracket name
	"Coastal Caro.": "Coastal Carolina",
	"North Carolina": "UNC",
	"North Carolina St.": "NC St.",
	"UNI": "Northern Iowa",
	"Albany (NY)": "Albany",
	"St. John's (NY)": "St. John's",
	"Eastern Wash.": "Eastern Washington"
}

def getUrl(year, stat_num, page_num):
	return 'http://www.ncaa.com/stats/basketball-men/d1/{}/team/{}/p{}'.format(year, stat_num, page_num)

def getHtml(url):
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	return urllib2.urlopen(req)

def getStats(year, stat_num, team_map, stat_map):
	for page_num in [1,2,3,4,5,6,7]:
		soup = BeautifulSoup(getHtml(getUrl(year, stat_num, page_num)), 'html.parser')
		teams = soup.find_all('tr')
		for teamHtml in teams:
			name = teamHtml.find_next('a').string
			if name in team_map:
				team = team_map[name]
			else:
				team = {}
			tds = teamHtml.find_all('td')
			if len(tds) > 0:
				for statName, index in stat_map.iteritems():
					team[statName] = tds[index].string
				team_map[name] = team

def year(year):
	year = int(year)
	if not MIN_YEAR <= year <= CURRENT_YEAR:
		raise argparse.ArgumentTypeError("Year specified must be between {} and {}".format(MIN_YEAR, CURRENT_YEAR))
	return year

def main():
	parser = argparse.ArgumentParser(description='Get defensive stats for a given year')
	parser.add_argument('-y', '--year', type=year, help='Year (between {} and {})'.format(MIN_YEAR, CURRENT_YEAR), default=CURRENT_YEAR)
	parser.add_argument('-t', '--teams', type=str, help='Path to text file containing list of teams to filter by (teams in the tourney)')
	args = parser.parse_args()

	team_map = dict()
	for stat_num, stat_map in STAT_PAGE_MAPPINGS.iteritems():
		getStats(args.year, stat_num, team_map, stat_map)

	for ncaa_name, codersbracket_name in NCAA_MAPPINGS.iteritems():
		team_map[codersbracket_name] = team_map[ncaa_name]
		del team_map[ncaa_name]

	teams_in_tourney = None
	if args.teams:
		with open(args.teams) as file:
			teams_in_tourney = [line.rstrip() for line in file]
	if teams_in_tourney:
		team_map = {teamname: team_map[teamname] for teamname in teams_in_tourney}
	
	print(json.dumps(team_map))

if __name__ == "__main__":
	main()