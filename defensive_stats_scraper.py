#!/usr/bin/env python2

from bs4 import BeautifulSoup
from datetime import date
from urllib.request import urlopen, Request
import json
import argparse

MIN_YEAR = 2010  # The NCAA stats pages only go back to 2010
CURRENT_YEAR = date.today().year
# define the columns given for a specific stat page on ncaa.com
STAT_PAGE_MAPPINGS = {
    # Offensive statistics
    145: {'games_played': 2, 'total_points': 3, 'ppg': 4},
    148: {'field_goals_made': 3, 'field_goals_attempted': 4, 'field_goal_pct': 5},
    150: {'free_throws_made': 3, 'free_throws_attempted': 4, 'free_throw_pct': 5},
    152: {'threes_made': 3, 'threes_attempted': 4, 'three_point_pct': 5},
    168: {'wins': 2, 'losses': 3, 'win_pcts': 4},
    932: {'off_reb': 3, 'def_reb': 4, 'total_reb': 5, 'reb_per_game': 6},
    215: {'total_steals': 3, 'steals_per_game': 4},
    214: {'total_blocks': 3, 'blocks_per_game': 4},
    216: {'total_assists': 3, 'assists_per_game': 4},
    217: {'turnovers': 3, 'turnovers_per_game': 4},
    # end offensive statistics
    149: {'opp_fg': 3, 'opp_fga': 4, 'opp_fg_per': 5},  # defensive fg%
    518: {'opp_3p_fga': 3, 'opp_3p_fg': 4, 'opp_3p_fg_per': 5},  # def 3pt fg%
    931: {'opp_tot_to': 3, 'opp_topg': 4},  # turnovers forced
    519: {'opp_tot_to': 3, 'to_ratio': 5},  # turnover margin
    151: {'opp_tot_reb': 5, 'opp_rpg': 6, 'reb_margin': 7},  # rebound margin
    147: {'own_tot_pts': 3, 'own_ppg': 4, 'opp_tot_pts': 5, 'opp_ppg': 6, 'pts_margin': 7},  # scoring margin
    146: {'opp_tot_pts': 3, 'opp_ppg': 4},  # scoring defense
    286: {'tot_pf': 3, 'pfpg': 4, 'dq': 5}  # fouls per game
}
UNMATCHED_RPI_VALUES = []


def getUrl(year, stat_num, page_num):
    return 'http://www.ncaa.com/stats/basketball-men/d1/{}/team/{}/p{}'.format(year, stat_num, page_num)


def getHtml(url):
    req = Request(url, headers={'User-Agent': "Magic Browser"})
    return urlopen(req)


def getStats(year, stat_num, team_map, stat_map):
    for page_num in [1, 2, 3, 4, 5, 6, 7]:
        soup = BeautifulSoup(getHtml(getUrl(year, stat_num, page_num)), 'html.parser')
        teams = soup.find_all('tr')
        for teamHtml in teams:
            name = teamHtml.find_next('a').string
            print("Getting stats on page {} for {}".format(page_num, name))
            if name in team_map:
                team = team_map[name]
            else:
                team = {}
            tds = teamHtml.find_all('td')
            if len(tds) > 0:
                for statName, index in stat_map.items():
                    team[statName] = tds[index].string
                team_map[name] = team

def getRanking(team_map):
    soup = BeautifulSoup(getHtml('http://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings'), 'html.parser')
    teams = soup.find_all('tr')
    for teamHtml in teams:
        allColumns = teamHtml.find_all('td')
        if (len(allColumns) > 0):
            rank = allColumns[0].string
            name = allColumns[2].string
            conference = allColumns[3].string
            if name in team_map:
                team = team_map[name]
            else:
                team = {}
            team['name'] = name
            team['conf'] = conference
            team['official_rank'] = rank
            team_map[name] = team

def getRPI(team_map):
    soup = BeautifulSoup(getHtml('https://www.teamrankings.com/ncaa-basketball/rpi-ranking/rpi-rating-by-team'), 'html.parser')
    teams = soup.find_all('tr')
    for teamHtml in teams:
        allColumns = teamHtml.find_all('td')
        if (len(allColumns) > 0):
            name = teamHtml.find_next('a').string
            try:
                rpi = teamHtml.find_next('td', class_='rank').string
                if name in team_map:
                    team_map[name]['rpi'] = rpi
                else:
                    UNMATCHED_RPI_VALUES.append({'name': name, 'rpi': rpi})
            except:
                break

def manuallyFillRPI(team_map):
    print('unmatched rpi values ----------------------------------')
    for idx, unmatched_rpi in enumerate(UNMATCHED_RPI_VALUES):
        print('%d: %s' % (idx, unmatched_rpi))
    print('-------------------------------------------------------')
    for team_name in team_map:
        if not 'rpi' in team_map[team_name]:
            rpi_index = int(input('Which team is ' + team_name + '?\n'))
            team_map[team_name]['rpi'] = UNMATCHED_RPI_VALUES[rpi_index]['rpi']


def year(year):
    year = int(year)
    if not MIN_YEAR <= year <= CURRENT_YEAR:
        raise argparse.ArgumentTypeError("Year specified must be between {} and {}".format(MIN_YEAR, CURRENT_YEAR))
    return year


def main():
    parser = argparse.ArgumentParser(description='Get defensive stats for a given year')
    parser.add_argument('-y', '--year', type=year, help='Year (between {} and {})'.format(MIN_YEAR, CURRENT_YEAR),
                        default=CURRENT_YEAR)
    parser.add_argument('-t', '--teams', type=str,
                        help='Path to text file containing list of teams to filter by (teams in the tourney)')
    args = parser.parse_args()

    team_map = dict()

    if args.year == CURRENT_YEAR:
        getRanking(team_map)
        getRPI(team_map)

    for stat_num, stat_map in STAT_PAGE_MAPPINGS.items():
        getStats(args.year, stat_num, team_map, stat_map)

    teams_in_tourney = None
    if args.teams:
        with open(args.teams) as file:
            teams_in_tourney = [line.rstrip() for line in file]
    if teams_in_tourney:
        team_map = {teamname: team_map[teamname] for teamname in teams_in_tourney}
        if args.year == CURRENT_YEAR:
            manuallyFillRPI(team_map)

    print(json.dumps(team_map))


if __name__ == "__main__":
    main()
