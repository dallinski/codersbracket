import argparse
import json


def compare_stat(stat_name, stat_value, all_teams):
	results = {"higher than": 0, "lower than": 0, "equal to": 0}
	for team, stats in all_teams.iteritems():
		comparison_stat = float(stats[stat_name])
		if comparison_stat > stat_value:
			results["lower than"] = results["lower than"] + 1
		elif comparison_stat < stat_value:
			results["higher than"] = results["higher than"] + 1
		else:
			results["equal to"] = results["equal to"] + 1
	print("Stat: {} - {}".format(stat_name, stat_value))
	print("{} is higher than {} teams in the tourney".format(stat_value, results["higher than"]))
	print("{} is lower than {} teams in the tourney".format(stat_value, results["lower than"]))
	if results["equal to"] is not 1:
		print("{} is the same as {} other teams in the tourney".format(stat_value, results["equal to"] - 1))


def main():
	parser = argparse.ArgumentParser(description='Analyze all of the defensive statistical categories for a given team against all the other teams in the tourney')
	parser.add_argument('-t', '--team', type=str, help='Team to analyze', required=True)
	parser.add_argument('-y', '--year', type=str, help='Year to analyze', required=True)
	args = parser.parse_args()

	results = {"higher than": 0, "lower than": 0, "equal to": 0}

	json_data=open("{}/{}.json".format(args.year, args.year)).read()
	all_teams = json.loads(json_data)
	for stat_name, stat_value in all_teams[args.team].iteritems():
		compare_stat(stat_name, float(stat_value), all_teams)

if __name__ == "__main__":
	main()