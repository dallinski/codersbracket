from bs4 import BeautifulSoup
from datetime import date
import urllib2
import json
import argparse


MIN_YEAR = 2010 # The NCAA stats pages only go back to 2010
CURRENT_YEAR = date.today().year
STAT_MAPPINGS = {
	149: {'gm': 2, 'opp_fg': 3, 'opp_fga': 4, 'opp_fg_per': 5}, # defensive fg%
	518: {'gm': 2, 'opp_3p_fga': 3, 'opp_3p_fg': 4, 'opp_3p_fg_per': 5}, # def 3pt fg%
	931: {'gm': 2, 'opp_tot_to': 3, 'opp_topg': 4}, # turnovers forced
	519: {'gm': 2, 'opp_tot_to': 3, 'own_tot_to': 4, 'to_ratio': 5}, # turnover margin
	151: {'gm': 2, 'own_tot_reb': 3, 'own_rpg': 4, 'opp_tot_reb': 5, 'opp_rpg': 6, 'reb_margin': 7}, # rebound margin
	147: {'gm': 2, 'own_tot_pts': 3, 'own_ppg': 4, 'opp_tot_pts': 5, 'opp_ppg': 6, 'pts_margin': 7}, # scoring margin
	146: {'gm': 2, 'opp_tot_pts': 3, 'opp_ppg': 4}, # scoring defense
	286: {'gm': 2, 'tot_pf': 3, 'pfpg': 4, 'dq': 5} # fouls per game
}

def getUrl(year, statNum, pageNum):
	return 'http://www.ncaa.com/stats/basketball-men/d1/{}/team/{}/p{}'.format(year, statNum, pageNum)

def getHtml(url):
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	return urllib2.urlopen(req)

def getStats(year, statNum, teamMap, statMap):
	for pageNum in [1,2,3,4,5,6,7]:
		soup = BeautifulSoup(getHtml(getUrl(year, statNum, pageNum)), 'html.parser')
		teams = soup.find_all('tr')
		for teamHtml in teams:
			name = teamHtml.find_next('a').string
			if name in teamMap:
				team = teamMap[name]
			else:
				team = {}
			tds = teamHtml.find_all('td')
			if len(tds) > 0:
				for statName, index in statMap.iteritems():
					team[statName] = tds[index].string
				teamMap[name] = team

def year(year):
	year = int(year)
	if not MIN_YEAR <= year <= CURRENT_YEAR:
		raise argparse.ArgumentTypeError("Year specified must be between {} and {}".format(MIN_YEAR, CURRENT_YEAR))
	return year

def main():
	parser = argparse.ArgumentParser(description='Get defensive stats for a given year')
	parser.add_argument('-y', '--year', type=year, help='Year (between {} and {})'.format(MIN_YEAR, CURRENT_YEAR), default=CURRENT_YEAR)
	args = parser.parse_args()

	teamMap = dict()
	for statNum, statMap in STAT_MAPPINGS.iteritems():
		getStats(args.year, statNum, teamMap, statMap)
	print(json.dumps(teamMap))

if __name__ == "__main__":
	main()