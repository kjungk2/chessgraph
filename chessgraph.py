user_name = "HighSilence"
file_name = "lichess_HighSilence_2020-12-09.txt"
file = open(file_name)

# Opens the PGN text file and puts into a list for easier use
full_list = []
for line in file:
	full_list.append(line)
file.close()


# each of these is a list of tournaments I played in for each time control. 
# Add to the lists any time I play another rated tournament.
classical_tournaments = []
rapid_tournaments = ["Under 1400 US Chess Online", "Hourly Rapid Arena", "<1700 Rapid Arena", "Daily Rapid Arena", "Reddit R Chess OCT Arena"]
blitz_tournaments = ["Forward Chess Arena", "Hourly Blitz Arena", "<1500 Blitz Arena"]
known_tournaments_all = classical_tournaments + rapid_tournaments + blitz_tournaments

# function that taks in a user-name, type of game, and a list of lists from the PGN download
# returns a re-ordered list of lists of game_details consisting of game number, date, and Elo post-game
def get_game_details(user_name, game_type, pgn_list, tournament_list):

	# a list of lists that will have key details of each game of game_type
	# [[game number, date, Elo], [game number, date, Elo], [etc]...]
	game_list = []
	game_number = 0
	line_counter = 0
	
	for line in pgn_list:
	
		# test to see if the current line references a tourney that is passed in
		is_rated_tournament_game = False
		for tourn in tournament_list:
			if tourn in line:
				is_rated_tournament_game = True
	
		# if passed in game_type exists in the current line OR tourn name was passed in AND the tourn name exists in current line
		if game_type in line or is_rated_tournament_game == True:

			game_number += 1
			game_date = pgn_list[line_counter + 6].split('"')[1]
			player_white = pgn_list[line_counter + 3]
			player_black = pgn_list[line_counter + 4]
			
			# check if user played white
			if user_name in player_white:
				rating_pre_game = pgn_list[line_counter+8].split('"')[1]
				rating_diff = pgn_list[line_counter+10].split('"')[1]
				
			# user played as black	
			else:
				rating_pre_game = pgn_list[line_counter+9].split('"')[1]
				rating_diff = pgn_list[line_counter+11].split('"')[1]
				
			# use rating before game and rating diff to calculate rating after the game
			rating_post_game = int(rating_pre_game) + int(rating_diff)
			
			game_detail = [game_number, game_date, rating_post_game]
			
			# append this list to the game list
			game_list.append(game_detail)
			
			line_counter += 1
			
		# add one to our line counter so we can keep track of everything
		else:
			line_counter += 1
	
	# done iterating through entire list but now we need to re-order the games
	# reverse lists so game number 1 is first game in my history, game 2 is second game, etc
	for game in game_list:
		
		#the zeroth index should be the game number, that is what we want to change
		game[0] = abs(game[0] - (len(game_list) + 1))
	
	return game_list

# writes each game list to the output text file, reversing order so game 1 is at top	
# returns None because its purpose is only to write to files
def write_data_to_txt(game_list,txt_output_file):
	with open(txt_output_file, "w") as filehandle:
		for game in reversed(game_list):
			for detail in game:
				filehandle.write('%s\n' % detail)
	filehandle.close()
	
	return None

# writes each game list to the output CSV file, reversing order so game 1 is at top	
# returns None because its purpose is only to write to files
def write_data_to_csv(game_list,csv_output_file):
	with open(csv_output_file, "w") as filehandle:
		filehandle.write('game,elo,date,\n')
		for game in reversed(game_list):
			# Write to the csv but put it in Game #, Elo, Date order
			filehandle.write('%s,%s,%s' % (game[0], game[2], game[1]))
			filehandle.write('\n')
	filehandle.close()
	
	return None

# This function will return a list of unique game types to print to command line
# This way, I can see if there are any special tournament event types I need to account for
def get_all_event_types(pgn_list):
		
	unique_events = []
	for line in pgn_list:
		if '[Event' in line:
			if line not in unique_events:
				unique_events.append(line)
	
	# clean up the list for easier handling, i.e. take out quotes and brackets
	clean_events = []
	for event in unique_events:
		clean_events.append(event.split('"')[1])
		
	return clean_events



# create the game lists
classical_list = get_game_details(user_name, "Rated Classical game", full_list, classical_tournaments)
rapid_list = get_game_details(user_name, "Rated Rapid game", full_list, rapid_tournaments)
blitz_list = get_game_details(user_name, "Rated Blitz game", full_list, blitz_tournaments)



# write data to csv
write_data_to_csv(classical_list,"output_classical.csv")
write_data_to_csv(rapid_list,"output_rapid.csv")
write_data_to_csv(blitz_list,"output_blitz.csv")



# Section for testing for new tournaments to add
print("\n* * * * * * * * * * * * * * *\nChecking for any new tournaments...\n")


#iterate through list of unique events from this latest PGN and if it's not in the "known" tournaments, then print to command window
events_list = get_all_event_types(full_list)
possible_new_tournament = []
for event in events_list:
	# we dont want single games, so we'll ignore those
	if "game" not in event:
		if event not in known_tournaments_all:
			possible_new_tournament.append(event)
	
if len(possible_new_tournament) > 0:
	print("Did you play in this/these new tournaments?\n")
	print("   " + str(possible_new_tournament))
	print("\nConsider adding them to the tournaments list variable for the corresponding time control and re-run")
	
if len(possible_new_tournament) == 0:
	print("No new tournaments found!")
	
print("* * * * * * * * * * * * * * *\n")
print("SUMMARY (rated games + rated tournament games):\n   Classical games: " + str(len(classical_list)))
print("   Rapid games: " + str(len(rapid_list)))
print("   Blitz games: " + str(len(blitz_list)))
