import random
import os
import json
import datetime


# Player class
class Player:
    def __init__(self, lastName, firstName, dateOfBirth, id):
        self.lastName = lastName
        self.firstName = firstName
        self.dateOfBirth = dateOfBirth
        self.id = id
        self.points = 0
        self.matchesPlayed = 0
        self.exemptions = 0

    def addPoints(self, points):
        self.points += points

    def getDetails(self):
        return {
            "id": self.id,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "dateOfBirth": self.dateOfBirth,
            "points": self.points
        }


# Round class
class Round:
    def __init__(self, players, playedMatches, exemptedPlayers=None):
        self.players = players.copy()
        self.matches = []
        self.playedMatches = playedMatches
        if exemptedPlayers is None:
            self.exemptedPlayers = set()

    def generateMatches(self, tournament):
        # Mélanger les joueurs au début du premier tour
        if len(tournament.rounds) == 0:
            random.shuffle(self.players)

        if len(self.players) % 2 == 1:
            print(f'maxException: {tournament.maxExemptions}')
            # select an eligible player to be exempted
            eligible_players = [
                p for p in self.players
                if p.exemptions < tournament.maxExemptions
            ]
            if eligible_players:
                exempted_player = random.choice(eligible_players)
                exempted_player.addPoints(0.5)
                exempted_player.exemptions += 1
                self.exemptedPlayers.add(exempted_player.id)
                print(
                    f"{exempted_player.firstName} is exempted from"
                    f"this round and gains 0.5 point."
                )
                self.players.remove(exempted_player)

        # Sort players by points to match them appropriately.
        sorted_players = sorted(
            self.players,
            key=lambda x: x.points,
            reverse=True
        )
        self.players = sorted_players  # Update the main player list.
        matched_players = set()

        while len(self.players) > 1:
            player1 = self.players.pop(0)
            potential_opponents = [
                p for p in self.players
                if p.id not in matched_players
            ]
            player2 = min(
                potential_opponents,
                key=lambda p: abs(p.points - player1.points)
            )
            self.players.remove(player2)
            match = (player1, player2)
            self.matches.append(match)
            matched_players.add(player1.id)
            matched_players.add(player2.id)

        if len(matched_players) < len(sorted_players) - 1:  # Check if odd
            print("Not all players could be matched.")

    def playMatch(self, player1, player2):
        start_time = datetime.datetime.now()
        print(f"Match: {player1.firstName} vs {player2.firstName}")
        while True:
            result_prompt = (
                f"Enter '1' if {player1.firstName} (ID: {player1.id}) wins, "
                f"'2' if {player2.firstName} (ID: {player2.id}) wins, "
                f"or 'd' for a draw: "
            )
            result = input(result_prompt).strip().lower()
            if result in ['1', '2', 'd']:
                break
            else:
                print("Invalid input. Please enter '1', '2', or 'd'.")
        end_time = datetime.datetime.now()
        match_result = {
            "player1": player1.id,
            "player2": player2.id,
            "winner": None,
            "draw": False
        }
        match_result["start_time"] = start_time.strftime("%Y-%m-%d %H:%M:%S")
        match_result["end_time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")

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

    def playMatches(self, tournament):
        self.generateMatches(tournament)
        round_results = []
        for match in self.matches:
            match_result = self.playMatch(match[0], match[1])
            round_results.append(match_result)
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
        self.rounds = []
        self.exemptedPlayers = set()
        # Calculer en fonction du ratio, nombre de joueurs/rounds.
        self.maxExemptions = 0
        self.directorRecommendations = ""

    def addRound(self, round):
        self.rounds.append(round)

    def getTournamentDetails(self):
        return {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "tournamentId": self.tournamentId,
            "players": [player.getDetails() for player in self.players]
        }

    def addDirectorRecommendations(self, recommendations):
        self.directorRecommendations += recommendations

    @staticmethod
    def updateDirectorRecommendations(tournament, filePath):
        with open(filePath, 'r+') as file:
            data = json.load(file)
            for t in data["tournaments"]:
                if t["id"] == tournament.tournamentId:
                    t["directorRecommendations"] = \
                        tournament.directorRecommendations
                    break
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=4)


# Functions for JSON file handling
def initializeTournamentFile(filePath):
    if not os.path.exists(filePath):
        with open(filePath, 'w') as file:
            json.dump({"tournaments": []}, file, indent=4)


def saveTournamentResults(tournament, roundNumber, roundResults, filePath):
    with open(filePath, 'r+') as file:
        data = json.load(file)
        for t in data["tournaments"]:
            if t["id"] == tournament.tournamentId:
                t["rounds"][str(roundNumber)] = roundResults
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)


def saveTournamentInfo(tournament, filePath):
    with open(filePath, 'r+') as file:
        data = json.load(file)
        tournament_data = {
            "name": tournament.name,
            "place": tournament.place,
            "date": tournament.date,
            "id": tournament.tournamentId,
            "players": [
                        {
                            "lastName": player.lastName,
                            "firstName": player.firstName,
                            "dateOfBirth": player.dateOfBirth,
                            "id": player.id
                        }
                        for player in tournament.players
                        ],
            "rounds": {},
            "directorRecommendations": tournament.directorRecommendations
        }
        data["tournaments"].append(tournament_data)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)
