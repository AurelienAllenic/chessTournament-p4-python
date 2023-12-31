import random
import os
import json
import datetime
import view
import math
import uuid


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

    def add_points(self, points):
        self.points += points

    def get_details(self):
        return {
            "id": self.id,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "dateOfBirth": self.dateOfBirth,
            "points": self.points
        }

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(data):
        player = Player(
            data['lastName'],
            data['firstName'],
            data['dateOfBirth'],
            data['id']
        )
        if 'points' in data:
            player.points = data['points']
        if 'matchesPlayed' in data:
            player.matchesPlayed = data['matchesPlayed']
        if 'exemptions' in data:
            player.exemptions = data['exemptions']
        return player


# Round class
class Round:
    def __init__(self, players, playedMatches, exemptedPlayers=None):
        self.players = players.copy()
        self.matches = []
        self.playedMatches = playedMatches
        if exemptedPlayers is None:
            self.exemptedPlayers = set()

    def to_dict(self):
        return {
            "matches": [(match[0].id, match[1].id) for match in self.matches]
        }

    @staticmethod
    def from_dict(data, all_players):
        round = Round(list(all_players.values()), set())
        return round

    def generate_matches(self, tournament):
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
                exempted_player.add_points(0.5)
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

    def play_match(self, player1, player2):
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
            player1.add_points(1)
            match_result["winner"] = player1.id
        elif result == '2':
            player2.add_points(1)
            match_result["winner"] = player2.id
        elif result == 'd':
            player1.add_points(0.5)
            player2.add_points(0.5)
            match_result["draw"] = True

        return match_result

    def play_matches(self, tournament):
        self.generate_matches(tournament)
        round_results = []
        for match in self.matches:
            match_result = self.play_match(match[0], match[1])
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

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "tournamentId": self.tournamentId,
            "players": [player.to_dict() for player in self.players],
            "rounds": [round.to_dict() for round in self.rounds],
            "directorRecommendations": self.directorRecommendations
        }

    @staticmethod
    def from_dict(data):
        tournament = Tournament(
            data['name'],
            data['place'],
            data['date'],
            data['tournamentId']
        )
        tournament.players = [Player.from_dict(p) for p in data['players']]
        all_players = {player.id: player for player in tournament.players}

        # Initialiser les points des joueurs à 0
        for player in tournament.players:
            player.points = 0

        # Parcourir les rounds et mettre à jour les points des joueurs
        for round_data in data.get('rounds', {}).values():
            for match in round_data:
                winner_id = match.get('winner')
                if winner_id:
                    all_players[winner_id].add_points(1)
                elif match.get('draw'):
                    all_players[match['player1']].add_points(0.5)
                    all_players[match['player2']].add_points(0.5)

        tournament.rounds = [
            Round.from_dict(round_data, all_players)
            for round_data in data.get('rounds', [])
        ]

        if 'directorRecommendations' in data:
            recommendations = data['directorRecommendations']
            tournament.directorRecommendations = recommendations

        return tournament

    def add_round(self, round):
        self.rounds.append(round)

    def get_tournament_details(self):
        return {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "tournamentId": self.tournamentId,
            "players": [player.get_details() for player in self.players]
        }

    def add_director_recommendations(self, recommendations):
        self.directorRecommendations += recommendations

    @staticmethod
    def update_director_recommendations(tournament, filePath):
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
def initialize_tournament_file(filePath):
    if not os.path.exists(filePath):
        with open(filePath, 'w') as file:
            json.dump({"tournaments": []}, file, indent=4)


def save_tournament_results(tournament, roundNumber, roundResults, filePath):
    with open(filePath, 'r+') as file:
        data = json.load(file)
        for t in data["tournaments"]:
            if t["tournamentId"] == tournament.tournamentId:
                t["rounds"][str(roundNumber)] = roundResults
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)


def save_tournament_info(tournament, filePath):
    with open(filePath, 'r+') as file:
        data = json.load(file)

        # Vérifier si le tournoi existe déjà
        tournament_gen = (
                t for t in data["tournaments"]
                if t["tournamentId"] == tournament.tournamentId
            )
        existing_tournament = next(tournament_gen, None)

        if existing_tournament is None:
            # Ajouter le nouveau tournoi si ce n'est pas un doublon
            tournament_data = {
                "name": tournament.name,
                "place": tournament.place,
                "date": tournament.date,
                "tournamentId": tournament.tournamentId,
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
        else:
            # Mettre à jour le tournoi existant
            existing_tournament.update({
                "name": tournament.name,
                "place": tournament.place,
                "date": tournament.date,
                "players": [
                    {
                        "lastName": player.lastName,
                        "firstName": player.firstName,
                        "dateOfBirth": player.dateOfBirth,
                        "id": player.id
                    }
                    for player in tournament.players
                ],
                "directorRecommendations": tournament.directorRecommendations
            })

        # Écrire les données mises à jour dans le fichier
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)


def save_tournament(tournament, filePath):
    with open(filePath, 'r+') as file:
        data = json.load(file)

        # Trouver le tournoi existant
        # Création du générateur
        tournament_gen = (
            t for t in data["tournaments"]
            if t["tournamentId"] == tournament.tournamentId
        )

        # Récupération du tournoi existant
        existing_tournament = next(tournament_gen, None)

        if existing_tournament:
            # Mettre à jour le tournoi existant
            existing_tournament.update(tournament.to_dict())
        else:
            # Ajouter un nouveau tournoi si ce n'est pas un doublon
            data["tournaments"].append(tournament.to_dict())

        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)


def load_tournament(tournamentId, filePath, numberOfPlayers, numberOfRounds):
    if not os.path.exists(filePath):
        return None

    with open(filePath, 'r') as file:
        data = json.load(file)
        for t in data.get("tournaments", []):
            if t.get("tournamentId") == tournamentId:
                tournament = Tournament.from_dict(t)
                conditions_not_met = (
                    not tournament.name
                    or not tournament.place
                    or not tournament.date
                    or len(tournament.players) < numberOfPlayers
                )

                if conditions_not_met:
                    complete_tournament_info(tournament, numberOfPlayers)
                return tournament

        print(f"Tournoi avec ID {tournamentId} non trouvé dans le fichier.")
        return None


def playRound(tournament, round_num):
    view.displayRound(round_num)
    round = Round(tournament.players, tournament.playedMatches)
    round.generate_matches(tournament)
    round_results = round.play_matches(tournament)

    for match in round_results:
        tournament.playedMatches.add((match['player1'], match['player2']))

    # Enregistrer les résultats du round
    save_tournament_results(tournament, round_num, round_results, 'data.json')


def complete_tournament_info(tournament, numberOfPlayers):
    # Compléter les informations manquantes du tournoi
    if not tournament.name:
        tournament.name = view.getTournamentName()
    if not tournament.place:
        tournament.place = view.getTournamentPlace()
    if not tournament.date:
        tournament.date = view.getTournamentDate()

    while len(tournament.players) < numberOfPlayers:
        player_details = view.getPlayerDetails(len(tournament.players) + 1)
        new_player = Player(*player_details)
        tournament.players.append(new_player)

    save_tournament_info(tournament, 'data.json')


def list_tournaments(filePath):
    if not os.path.exists(filePath):
        return []

    with open(filePath, 'r') as file:
        data = json.load(file)
        tournament_list = []

        for t in data.get("tournaments", []):
            tournament_info = {
                "id": t.get("tournamentId"),
                "name": t.get("name", "Nom inconnu"),
                "place": t.get("place", "Lieu inconnu"),
                "date": t.get("date", "Date inconnue")
            }
            tournament_list.append(tournament_info)

        return tournament_list


def load_or_create_tournament(id, filePath, numberOfPlayers, numberOfRnds):
    tournament = load_tournament(id, filePath, numberOfPlayers, numberOfRnds)
    print('director : ', tournament.directorRecommendations)
    if tournament:
        # Compléter les infos manquantes et jouer les rounds manquants
        complete_tournament_info(tournament, numberOfPlayers)
        play_rounds(tournament, numberOfRnds, filePath)
    else:
        # Créer un nouveau tournoi si le tournoi spécifié n'existe pas
        tournament = create_new_tournament(filePath)

    return tournament


def create_new_tournament(filePath):
    tournamentId = str(uuid.uuid4())
    tournament = Tournament("", "", "", tournamentId)

    tournament.name = view.getTournamentName()
    save_tournament_info(tournament, filePath)
    tournament.place = view.getTournamentPlace()
    save_tournament_info(tournament, filePath)
    tournament.date = view.getTournamentDate()
    save_tournament_info(tournament, filePath)

    numberOfPlayers = view.getNumberOfPlayers()
    for i in range(1, numberOfPlayers + 1):
        lastName, firstName, dateOfBirth, id = view.getPlayerDetails(i)
        player = Player(lastName, firstName, dateOfBirth, id)
        tournament.players.append(player)
        save_tournament_info(tournament, filePath)

    numberOfRounds = view.getNumberOfRounds()
    exemption_ratio = numberOfRounds / len(tournament.players)
    tournament.maxExemptions = math.ceil(exemption_ratio)

    save_tournament_info(tournament, filePath)
    play_rounds(tournament, numberOfRounds, filePath)

    return tournament


def play_rounds(tournament, numberOfRounds, fileP):
    for round_number in range(len(tournament.rounds) + 1, numberOfRounds + 1):
        view.displayRound(round_number)
        round = Round(tournament.players, tournament.playedMatches)
        round.generate_matches(tournament)
        round_results = round.play_matches(tournament)
        for match in round_results:
            tournament.playedMatches.add((match['player1'], match['player2']))
        save_tournament_results(tournament, round_number, round_results, fileP)
        save_tournament_info(tournament, fileP)


def finalize_tournament(tournament, filePath):
    view.displayFinalRanking(tournament.players)

    # Charger les données du tournoi depuis le fichier JSON
    tournament_data = load_tournament_data(filePath, tournament.tournamentId)

    # Vérifier si les recommandations du directeur existent dans le JSON
    if tournament_data:
        existing_director = tournament_data.get('directorRecommendations')
    else:
        existing_director = ''

    # Si les recos sont présentes, les utiliser, sinon les demander
    if existing_director:
        print(f"Current director recommendations: {existing_director}")
    else:
        print('Director recommendations needed.')
        new_director_recommendations = view.getDirectorRecommendations()
        tournament.add_director_recommendations(new_director_recommendations)

    # Sauvegarder les informations mises à jour du tournoi
    save_tournament_info(tournament, filePath)


def load_tournament_data(filePath, tournamentId):
    with open(filePath, 'r') as file:
        data = json.load(file)
        for t in data.get("tournaments", []):
            if t["tournamentId"] == tournamentId:
                return t
    return None
