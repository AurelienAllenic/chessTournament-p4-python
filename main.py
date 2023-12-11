import json
import random
import uuid

# Player class
class Player:
    def __init__(self, lastName, firstName, dateOfBirth, id):
        self.lastName = lastName
        self.firstName = firstName
        self.dateOfBirth = dateOfBirth
        self.id = id
        self.points = 0

    def addPoints(self, points):
        self.points += points

    def __str__(self):
        return f"Player(ID: {self.id}, Last Name: {self.lastName}, First Name: {self.firstName}, Birth Date: {self.dateOfBirth})"

# Round class
class Round:
    def __init__(self, players, playedMatches):
        self.players = players
        self.matches = []
        self.playedMatches = playedMatches

    def generateMatches(self):
        random.shuffle(self.players)
        self.matches = []
        sorted_players = sorted(self.players, key=lambda x: x.points, reverse=True)

        for i in range(0, len(sorted_players), 2):
            if i + 1 < len(sorted_players):
                player1 = sorted_players[i]
                player2 = sorted_players[i + 1]
                self.matches.append((player1, player2))
                print(f'{player1.firstName} vs {player2.firstName}')

                matchPair = (player1.id, player2.id)
                self.playedMatches.add(matchPair)

    def playMatch(self, player1, player2):
        print(f"Match: {player1.firstName} vs {player2.firstName}")
        while True:
            result = input(f"Enter '1' if {player1.firstName} wins, '2' if {player2.firstName} wins, or 'd' for a draw: ").strip().lower()
            if result in ['1', '2', 'd']:
                break
            else:
                print("Invalid input. Please enter '1', '2', or 'd'.")

        match_result = {"player1": player1.id, "player2": player2.id, "winner": None, "draw": False}

        if result == '1':
            player1.addPoints(1)
            match_result["winner"] = player1.id
        elif result == '2':
            player2.addPoints(1)
            match_result["winner"] = player2.id
        elif result == 'd':
            player1.addPoints(0.5)
            player2.addPoints(0.5)
            match_result["draw"] = True

        return match_result

    def playMatches(self):
        self.generateMatches()
        round_results = []
        for match in self.matches:
            match_result = self.playMatch(match[0], match[1])
            round_results.append({
                "player1": match[0].id,
                "player2": match[1].id,
                "winner": match_result["winner"],
                "draw": match_result["draw"]
            })
        return round_results

# Tournament class
class Tournament:
    def __init__(self, name, place, date, tournamentId, players=[]):
        self.name = name
        self.place = place
        self.date = date
        self.tournamentId = tournamentId
        self.players = players
        self.playedMatches = set()

    def __str__(self):
        return f"Tournament(Name: {self.name}, Place: {self.place}, Date: {self.date}, ID: {self.tournamentId})"

# Function to save tournament results
def saveTournamentResults(tournament, roundNumber, roundResults, filePath):
    with open(filePath, 'r+') as file:
        data = json.load(file)
        if "rounds" not in data:
            data["rounds"] = {}
        data["rounds"][str(roundNumber)] = roundResults
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

def savePlayers(players, filePath):
    with open(filePath, 'r+') as file:
        data = json.load(file)
        data["players"] = [{
            "lastName": player.lastName,
            "firstName": player.firstName,
            "dateOfBirth": player.dateOfBirth,
            "id": player.id
        } for player in players]
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

def initializeTournamentFile(filePath):
    with open(filePath, 'w') as file:
        json.dump({"name": "", "place": "", "date": "", "id": "", "players": [], "rounds": {}}, file, indent=4)

def saveTournamentInfo(name, place, date, tournamentId, filePath):
    with open(filePath, 'r+') as file:
        data = json.load(file)
        data["name"] = name
        data["place"] = place
        data["date"] = date
        data["id"] = tournamentId
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

def displayRanking(players):
    sorted_players = sorted(players, key=lambda x: x.points, reverse=True)
    last_score = None
    last_rank = 0
    rank_increment = 1

    for player in sorted_players:
        if player.points != last_score:
            last_score = player.points
            last_rank += rank_increment
            rank_increment = 1
        else:
            rank_increment += 1

        print(f"{player.firstName} is at the {ordinal(last_rank)} place with {player.points} points")

def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[((n // 10 % 10 != 1) * (n % 10 < 4) * n % 10)::4])


# Initialize JSON file for new tournament
filePath = 'data.json'
initializeTournamentFile(filePath)

# Input tournament details
tournamentName = input("Enter the tournament name: ")
tournamentPlace = input("Enter the tournament place: ")
tournamentDate = input("Enter the tournament date (DD/MM/YYYY): ")
tournamentId = str(uuid.uuid4())

# Save tournament information to JSON
saveTournamentInfo(tournamentName, tournamentPlace, tournamentDate, tournamentId, filePath)

# Collect player information
players = []
numberOfPlayers = int(input("Enter number of players: "))
for i in range(1, numberOfPlayers + 1):
    print(f"Enter information for Player {i}:")
    lastName = input("Last Name: ")
    firstName = input("First Name: ")
    dateOfBirth = input("Date of Birth (DD/MM/YYYY): ")
    id = input("ID: ")

    player = Player(lastName, firstName, dateOfBirth, id)
    players.append(player)

# Save players to JSON
savePlayers(players, filePath)

# Create a Tournament instance
tournament = Tournament(tournamentName, tournamentPlace, tournamentDate, tournamentId, players)
print(tournament)

# Define the number of rounds to play
numberOfRounds = int(input("Enter number of rounds: "))

# Play multiple rounds in the tournament
for round_number in range(1, numberOfRounds + 1):
    print(f"Round {round_number}")
    round = Round(tournament.players, tournament.playedMatches)
    round_results = round.playMatches()
    saveTournamentResults(tournament, round_number, round_results, filePath)
    for player in tournament.players:
        print(f"{player.firstName} has {player.points} points")

# Display the final ranking
print("\nFinal Ranking:")
displayRanking(tournament.players)
