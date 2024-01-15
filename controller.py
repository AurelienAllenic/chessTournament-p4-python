import model
import view
import uuid
import math
import os
import json


def play_rounds(tournament, numberOfRounds, fileP):
    for round_number in range(len(tournament.rounds) + 1, numberOfRounds + 1):
        view.displayRound(round_number)
        round = model.Round(tournament.players, tournament.playedMatches)
        round.generate_matches(tournament)
        results = round.play_matches(tournament)
        for match in results:
            player1 = match['player1']
            player2 = match['player2']
            tournament.playedMatches.add((player1, player2))
        model.save_tournament_results(tournament, round_number, results, fileP)
        model.save_tournament_info(tournament, fileP)


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
        new_player = model.Player(*player_details)
        tournament.players.append(new_player)

    model.save_tournament_info(tournament, 'data.json')


def playRound(tournament, round_num):
    view.displayRound(round_num)
    round = model.Round(tournament.players, tournament.playedMatches)
    round.generate_matches(tournament)
    round_results = round.play_matches(tournament)

    for match in round_results:
        tournament.playedMatches.add((match['player1'], match['player2']))

    # Enregistrer les résultats du round
    file_path = 'data.json'
    results = (tournament, round_num, round_results)
    model.save_tournament_results(*results, file_path)


def create_new_tournament(filePath):
    tournamentId = str(uuid.uuid4())
    tournament = model.Tournament("", "", "", tournamentId)

    tournament.name = view.getTournamentName()
    model.save_tournament_info(tournament, filePath)
    tournament.place = view.getTournamentPlace()
    model.save_tournament_info(tournament, filePath)
    tournament.date = view.getTournamentDate()
    model.save_tournament_info(tournament, filePath)

    numberOfPlayers = view.getNumberOfPlayers()
    for i in range(1, numberOfPlayers + 1):
        lastName, firstName, dateOfBirth, id = view.getPlayerDetails(i)
        player = model.Player(lastName, firstName, dateOfBirth, id)
        tournament.players.append(player)
        model.save_tournament_info(tournament, filePath)

    numberOfRounds = view.getNumberOfRounds()
    exemption_ratio = numberOfRounds / len(tournament.players)
    tournament.maxExemptions = math.ceil(exemption_ratio)

    model.save_tournament_info(tournament, filePath)
    play_rounds(tournament, numberOfRounds, filePath)

    return tournament


def finalize_tournament(tournament, filePath):
    view.displayFinalRanking(tournament.players)

    # Charger les données du tournoi depuis le fichier JSON
    tournament_id = tournament.tournamentId
    tournament_data = model.load_tournament_data(filePath, tournament_id)

    # Vérifier si les recommandations du directeur existent dans le JSON
    if tournament_data:
        existing_director = tournament_data.get('directorRecommendations')
    else:
        existing_director = ''

    # Si les recos sont présentes, les utiliser, sinon les demander
    if existing_director:
        view.manage_recommandations(existing_director)
    else:
        view.manage_recommandations('')
        new_director_recommendations = view.getDirectorRecommendations()
        tournament.add_director_recommendations(new_director_recommendations)

    # Sauvegarder les informations mises à jour du tournoi
    model.save_tournament_info(tournament, filePath)


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
    if tournament:
        # Compléter les infos manquantes et jouer les rounds manquants
        complete_tournament_info(tournament, numberOfPlayers)
        play_rounds(tournament, numberOfRnds, filePath)
    else:
        # Créer un nouveau tournoi si le tournoi spécifié n'existe pas
        tournament = create_new_tournament(filePath)

    return tournament


def load_tournament(tournamentId, filePath, numberOfPlayers, numberOfRounds):
    if not os.path.exists(filePath):
        return None

    with open(filePath, 'r') as file:
        data = json.load(file)
        for t in data.get("tournaments", []):
            if t.get("tournamentId") == tournamentId:
                tournament = model.Tournament.from_dict(t)
                conditions_not_met = (
                    not tournament.name
                    or not tournament.place
                    or not tournament.date
                    or len(tournament.players) < numberOfPlayers
                )

                if conditions_not_met:
                    complete_tournament_info(tournament, numberOfPlayers)
                return tournament
        view.tournament_not_found(tournamentId)
        return None


def createTournament():
    filePath = 'data.json'
    model.initialize_tournament_file(filePath)

    existing_tournaments = list_tournaments(filePath)
    view.displayExistingTournaments(existing_tournaments)

    load_existing = view.askUserToLoadExistingTournament()
    if load_existing:
        tournamentId = view.askUserForTournamentId()
        numberOfPlayers = view.getNumberOfPlayers()
        numberOfRounds = view.getNumberOfRounds()
        tournament = load_or_create_tournament(
            tournamentId, filePath, numberOfPlayers, numberOfRounds
        )

    else:
        tournament = create_new_tournament(filePath)

    finalize_tournament(tournament, filePath)


createTournament()
