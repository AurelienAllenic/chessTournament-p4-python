import model
import view
import uuid
import math

def createTournament():

    filePath = 'data.json'
    model.initializeTournamentFile(filePath)

   # Initialisation de l'objet Tournament avec un ID unique
    tournamentId = str(uuid.uuid4())
    tournament = model.Tournament("", "", "", tournamentId)

    # Mise à jour et sauvegarde du nom du tournoi
    tournament.name = view.getTournamentName()
    model.saveTournamentInfo(tournament, filePath)

    # Mise à jour et sauvegarde du lieu du tournoi
    tournament.place = view.getTournamentPlace()
    model.saveTournamentInfo(tournament, filePath)

    # Mise à jour et sauvegarde de la date du tournoi
    tournament.date = view.getTournamentDate()
    model.saveTournamentInfo(tournament, filePath)

    # Création de la liste des joueurs et sauvegarde après chaque ajout
    numberOfPlayers = view.getNumberOfPlayers()
    for i in range(1, numberOfPlayers + 1):
        lastName, firstName, dateOfBirth, id = view.getPlayerDetails(i)
        player = model.Player(lastName, firstName, dateOfBirth, id)
        tournament.players.append(player)
        model.saveTournamentInfo(tournament, filePath)  # Sauvegarde après ajout de chaque joueur

    # Détermination du nombre de rounds et sauvegarde
    numberOfRounds = view.getNumberOfRounds()
    tournament.maxExemptions = math.ceil(numberOfRounds / len(tournament.players))
    model.saveTournamentInfo(tournament, filePath)  # Sauvegarde après détermination des rounds

    # Déroulement des rounds
    for round_number in range(1, numberOfRounds + 1):
        view.displayRound(round_number)
        round = model.Round(tournament.players, tournament.playedMatches)
        round.generateMatches(tournament)
        round_results = round.playMatches(tournament)

        # Enregistrement des résultats du round et mise à jour du tournoi
        model.saveTournamentResults(tournament, round_number, round_results, filePath)
        for match in round_results:
            tournament.playedMatches.add((match['player1'], match['player2']))
        model.saveTournamentInfo(tournament, filePath)  # Sauvegarde après chaque round

    # Affichage du classement final
    view.displayFinalRanking(tournament.players)

    # Récupération et enregistrement des recommandations du directeur
    director_recommendations = view.getDirectorRecommendations()
    tournament.addDirectorRecommendations(director_recommendations)
    model.Tournament.updateDirectorRecommendations(tournament, filePath)  # Sauvegarde finale incluant les recommandations

# Exécution du contrôleur
createTournament()
