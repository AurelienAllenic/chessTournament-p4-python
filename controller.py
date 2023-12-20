import model
import view
import uuid
import math


def createTournament():
    filePath = 'data.json'
    model.initializeTournamentFile(filePath)

    # Récupération des détails du tournoi
    tournamentName, tournamentPlace, tournamentDate = \
        view.getTournamentDetails()

    tournamentId = str(uuid.uuid4())

    # Création de la liste des joueurs
    players = []
    numberOfPlayers = view.getNumberOfPlayers()
    for i in range(1, numberOfPlayers + 1):
        lastName, firstName, dateOfBirth, id = view.getPlayerDetails(i)
        player = model.Player(lastName, firstName, dateOfBirth, id)
        players.append(player)

    # Détermination du nombre de rounds
    numberOfRounds = view.getNumberOfRounds()

    # Création de l'objet Tournament
    tournament = model.Tournament(
        tournamentName,
        tournamentPlace,
        tournamentDate,
        tournamentId,
        players
    )

    tournament.maxExemptions = math.ceil(numberOfRounds / len(players))

    # Enregistrement initial des informations du tournoi
    model.saveTournamentInfo(tournament, filePath)

    # Déroulement des rounds
    for round_number in range(1, numberOfRounds + 1):
        view.displayRound(round_number)
        round = model.Round(tournament.players, tournament.playedMatches)
        round.generateMatches(tournament)
        round_results = round.playMatches(tournament)

        # Enregistrement des résultats du round
        model.saveTournamentResults(
            tournament, round_number, round_results, filePath
        )

        # Mise à jour de l'état du tournoi
        for match in round_results:
            tournament.playedMatches.add((match['player1'], match['player2']))

    # Affichage du classement final
    view.displayFinalRanking(tournament.players)

    # Récupération et enregistrement des recommandations du directeur
    director_recommendations = view.getDirectorRecommendations()
    tournament.addDirectorRecommendations(director_recommendations)

    model.Tournament.updateDirectorRecommendations(tournament, filePath)


# Exécution du contrôleur
createTournament()
