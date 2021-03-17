#!/usr/bin/env python3

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
RPI_TEAM_NAME_MAPPING = {
    # name on RPI website : name on NCAA website
    'Ohio State': 'Ohio St.',
    'W Virginia': 'West Virginia',
    'Florida St': 'Florida St.',
    'Loyola-Chi': 'Loyola Chicago',
    'San Diego St': 'San Diego St.',
    'USC': 'Southern California',
    'St Bonavent': 'St. Bonaventure',
    'Oklahoma St': 'Oklahoma St.',
    'Boise State': 'Boise St.',
    'Connecticut': 'UConn',
    'GA Tech': 'Georgia Tech',
    'N Carolina': 'North Carolina',
    'Colorado St': 'Colorado St.',
    'VA Tech': 'Virginia Tech',
    'Utah State': 'Utah St.',
    'UCSB': 'UC Santa Barbara',
    'Penn State': 'Penn St.',
    'S Methodist': 'SMU',
    'Mississippi': 'Ole Miss',
    'Wright State': 'Wright St.',
    'Wichita St': 'Wichita St.',
    'St Marys': 'Saint Mary\'s (CA)',
    'LA Tech': 'Louisiana Tech',
    'St Johns': 'St. John\'s (NY)',
    'W Kentucky': 'Western Ky.',
    'Michigan St': 'Michigan St.',
    'Miss State': 'Mississippi St.',
    'Abl Christian': 'Abilene Christian',
    'NC-Grnsboro': 'UNC Greensboro',
    'Missouri St': 'Missouri St.',
    'Kent State': 'Kent St.',
    'Loyola Mymt': 'LMU (CA)',
    'Wash State': 'Washington St.',
    'Weber State': 'Weber St.',
    'Central FL': 'UCF',
    'Arizona St': 'Arizona St.',
    'Oregon St': 'Oregon St.',
    'S Carolina': 'South Carolina',
    'E Washingtn': 'Eastern Wash.',
    'TX Christian': 'TCU',
    'San Fransco': 'San Francisco',
    'U Mass': 'Massachusetts',
    'S Dakota St': 'South Dakota St.',
    'Army': 'Army West Point',
    'Indiana St': 'Indiana St.',
    'Geo Mason': 'George Mason',
    'Bowling Grn': 'Bowling Green',
    'Maryland BC': 'UMBC',
    'James Mad': 'James Madison',
    'E Tenn St': 'ETSU',
    'Morehead St': 'Morehead St.',
    'Grd Canyon': 'Grand Canyon',
    'Georgia St': 'Georgia St.',
    'S Utah': 'Southern Utah',
    'Northeastrn': 'Northeastern',
    'VA Military': 'VMI',
    'Texas State': 'Texas St.',
    'Cleveland St': 'Cleveland St.',
    'Sam Hous St': 'Sam Houston',
    'E Kentucky': 'Eastern Ky.',
    'Jksnville St': 'Jacksonville St.',
    'Coastal Car': 'Coastal Carolina',
    'LA Lafayette': 'Lafayette',
    'S Alabama': 'South Alabama',
    'St Peters': 'Saint Peter\'s',
    'Morgan St': '',
    'TX Southern': 'Texas Southern',
    'CS Bakersfld': '',
    'Mt St Marys': 'Mount St. Mary\'s',
    'TX El Paso': '',
    'Nicholls St': '',
    'S Florida': '',
    'N Kentucky': '',
    'Norfolk St': 'Norfolk St.',
    'Ste F Austin': '',
    'E Carolina': '',
    'TX-San Ant': '',
    'Kansas St': '',
    'Sacred Hrt': '',
    'AR Lit Rock': '',
    'Ball State': '',
    'Citadel': '',
    'Fresno St': '',
    'TX-Arlington': '',
    'Jackson St': '',
    'Boston U': '',
    'N Iowa': '',
    'N Dakota St': '',
    'Detroit': '',
    'St Fran (NY)': '',
    'W Carolina': '',
    'Mass Lowell': '',
    'Montana St': '',
    'Coppin State': '',
    'WI-Milwkee': '',
    'S Illinois': '',
    'NC-Asheville': '',
    'Wm & Mary': '',
    'CS Fullerton': '',
    'Youngs St': '',
    'St Josephs': 'Saint Joseph\'s',
    'Fla Atlantic': '',
    'Gard-Webb': '',
    'Albany': '',
    'GA Southern': '',
    'Iowa State': '',
    'Murray St': '',
    'F Dickinson': '',
    'N Hampshire': '',
    'Utah Val St': '',
    'Cal St Nrdge': '',
    'NW State': '',
    'Sac State': '',
    'Grambling St': '',
    'Loyola-MD': '',
    'Arkansas St': '',
    'NC A&T': '',
    'TX-Pan Am': '',
    'St Fran (PA)': '',
    'SE Missouri': '',
    'Illinois St': '',
    'N Arizona': '',
    'Southern': '',
    'WI-Grn Bay': '',
    'Col Charlestn': '',
    'Geo Wshgtn': '',
    'SIU Edward': '',
    'N Florida': '',
    'Boston Col': '',
    'Cal Baptist': '',
    'N Alabama': '',
    'TN Martin': '',
    'Alcorn State': '',
    'Central Ark': '',
    'Central Conn': '',
    'W Michigan': '',
    'IPFW': '',
    'N Mex State': '',
    'NC-Wilmgton': '',
    'Fla Gulf Cst': '',
    'Tarleton State': '',
    'SC Upstate': '',
    'SE Louisiana': '',
    'UMKC': '',
    'IL-Chicago': '',
    'LA Monroe': '',
    'N Colorado': '',
    'E Illinois': '',
    'Alab A&M': '',
    'Lg Beach St': '',
    'TN Tech': '',
    'Dixie State': '',
    'Portland St': '',
    'S Mississippi': '',
    'Idaho State': '',
    'Middle Tenn': '',
    'San Jose St': '',
    'Seattle': '',
    'Lamar': '',
    'E Michigan': '',
    'Florida Intl': '',
    'Rob Morris': '',
    'Charl South': '',
    'Neb Omaha': '',
    'Houston Bap': '',
    'Central Mich': '',
    'W Illinois': '',
    'NC Central': '',
    'TN State': '',
    'Miss Val St': '',
    'Ark Pine Bl': '',
    'N Illinois': '',
    'Kennesaw St': '',
    'Incar Word': '',
    'Chicago St': '',
    'McNeese St': '',
    'Alabama St': '',
    'TX A&M-CC': '',
    'Delaware St': '',
    'S Car State': '',
    'Yale': '',
    'Cornell': '',
    'Columbia': '',
    'Brown': '',
    'Harvard': '',
    'Dartmouth': '',
    'Princeton': '',
    'U Penn': '',
    'Beth-Cook': '',
    'Maryland ES': ''
}
UNMATCHED_RPI_VALUES = []


def get_url(year, stat_num, page_num):
    if year == CURRENT_YEAR:
        year = 'current'
    return 'http://www.ncaa.com/stats/basketball-men/d1/{}/team/{}/p{}'.format(year, stat_num, page_num)


def get_html(url):
    req = Request(url, headers={'User-Agent': "Magic Browser"})
    return urlopen(req)


def get_stats(year, stat_num, team_map, stat_map, debug):
    for page_num in [1, 2, 3, 4, 5, 6, 7]:
        soup = BeautifulSoup(get_html(get_url(year, stat_num, page_num)), 'html.parser')
        teams = soup.find_all('tr')
        for teamHtml in teams:
            name = teamHtml.find_next('a').string
            if debug:
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


def get_ranking(team_map):
    soup = BeautifulSoup(get_html('http://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings'), 'html.parser')
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

def get_rpi(team_map):
    soup = BeautifulSoup(get_html('https://www.teamrankings.com/ncaa-basketball/rpi-ranking/rpi-rating-by-team'),
                         'html.parser')
    teams = soup.find_all('tr')
    for teamHtml in teams:
        all_columns = teamHtml.find_all('td')
        if len(all_columns) > 0:
            name = teamHtml.find_next('a').string
            try:
                rpi = teamHtml.find_next('td', class_='rank').string

                if name in team_map:
                    team = team_map[name]
                else:
                    team = {}

                if name in team_map:
                    team_map[name]['rpi'] = rpi
                elif name in RPI_TEAM_NAME_MAPPING:
                    if RPI_TEAM_NAME_MAPPING[name] in team_map:
                        team = team_map[RPI_TEAM_NAME_MAPPING[name]]
                    else:
                        team = {'name': RPI_TEAM_NAME_MAPPING[name]}
                        UNMATCHED_RPI_VALUES.append({'name': name, 'rpi': rpi})
                    team['rpi'] = rpi
                    team_map[RPI_TEAM_NAME_MAPPING[name]] = team
                else:
                    print('Cannot determine rpi for {}'.format(name))
                    # raise Exception('Cannot determine rpi for {}'.format(name))
            except:
                break


def manually_fill_rpi(team_map):
    print('unmatched rpi values ----------------------------------')
    for idx, unmatched_rpi in enumerate(UNMATCHED_RPI_VALUES):
        print('%d: %s' % (idx, unmatched_rpi))
    print('-------------------------------------------------------')
    for team_name in team_map:
        if not 'rpi' in team_map[team_name]:
            rpi_index = int(input('Which team is ' + team_name + '?\n'))
            team_map[team_name]['rpi'] = UNMATCHED_RPI_VALUES[rpi_index]['rpi']


def year_input(year):
    year = int(year)
    if not MIN_YEAR <= year <= CURRENT_YEAR:
        raise argparse.ArgumentTypeError("Year specified must be between {} and {}".format(MIN_YEAR, CURRENT_YEAR))
    return year


def main():
    parser = argparse.ArgumentParser(description='Get defensive stats for a given year')
    parser.add_argument('-y', '--year', type=year_input, help='Year (between {} and {})'.format(MIN_YEAR, CURRENT_YEAR),
                        default=CURRENT_YEAR)
    parser.add_argument('-t', '--teams', type=str,
                        help='Path to text file containing list of teams to filter by (teams in the tourney)')
    parser.add_argument('-d', '--debug', type=bool, help='Print debug logs')
    args = parser.parse_args()

    team_map = dict()

    if args.year == CURRENT_YEAR:
        get_ranking(team_map)
        get_rpi(team_map)

    for stat_num, stat_map in STAT_PAGE_MAPPINGS.items():
        get_stats(args.year, stat_num, team_map, stat_map, args.debug)

    teams_in_tourney = None
    if args.teams:
        with open(args.teams) as file:
            teams_in_tourney = [line.rstrip() for line in file]
    if teams_in_tourney:
        team_map = {teamname: team_map[teamname] for teamname in teams_in_tourney}
        if args.year == CURRENT_YEAR:
            manually_fill_rpi(team_map)

    print(json.dumps(team_map))


if __name__ == "__main__":
    main()
