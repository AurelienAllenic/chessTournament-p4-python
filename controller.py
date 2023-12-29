import model
import view
import uuid
import math
import json

def createTournament():
    filePath = 'data.json'
    model.initializeTournamentFile(filePath)

    existing_tournaments = model.list_tournaments(filePath)
    view.displayExistingTournaments(existing_tournaments)

    load_existing = view.askUserToLoadExistingTournament()
    if load_existing:
        tournamentId = view.askUserForTournamentId()
        numberOfPlayers = view.getNumberOfPlayers()
        numberOfRounds = view.getNumberOfRounds()
        tournament = model.load_tournament(tournamentId, filePath, numberOfPlayers, numberOfRounds)
        if tournament:
            if len(tournament.rounds) < numberOfRounds:
                # Appeler playRounds uniquement si le nombre de rounds joués est inférieur à numberOfRounds
                playRounds(tournament, numberOfRounds, filePath)
        else:
            print("Tournoi non trouvé. Création d'un nouveau tournoi.")
            tournament = createNewTournament(filePath)
    else:
        tournament = createNewTournament(filePath)

    finalizeTournament(tournament, filePath)

def createNewTournament(filePath):
    tournamentId = str(uuid.uuid4())
    tournament = model.Tournament("", "", "", tournamentId)

    tournament.name = view.getTournamentName()
    model.saveTournamentInfo(tournament, filePath)
    tournament.place = view.getTournamentPlace()
    model.saveTournamentInfo(tournament, filePath)
    tournament.date = view.getTournamentDate()
    model.saveTournamentInfo(tournament, filePath)

    numberOfPlayers = view.getNumberOfPlayers()
    for i in range(1, numberOfPlayers + 1):
        lastName, firstName, dateOfBirth, id = view.getPlayerDetails(i)
        player = model.Player(lastName, firstName, dateOfBirth, id)
        tournament.players.append(player)
        model.saveTournamentInfo(tournament, filePath)

    numberOfRounds = view.getNumberOfRounds()
    tournament.maxExemptions = math.ceil(numberOfRounds / len(tournament.players))
    
    model.saveTournamentInfo(tournament, filePath)
    playRounds(tournament, numberOfRounds, filePath)

    return tournament

def playRounds(tournament, numberOfRounds, filePath):
    print('es-tu appelé ?')
    for round_number in range(len(tournament.rounds) + 1, numberOfRounds + 1):
        view.displayRound(round_number)
        round = model.Round(tournament.players, tournament.playedMatches)
        round.generateMatches(tournament)
        round_results = round.playMatches(tournament)
        for match in round_results:
            tournament.playedMatches.add((match['player1'], match['player2']))
        model.saveTournamentResults(tournament, round_number, round_results, filePath)
        model.saveTournamentInfo(tournament, filePath)

def finalizeTournament(tournament, filePath):
    view.displayFinalRanking(tournament.players)
    
    # Charger les données du tournoi depuis le fichier JSON pour vérifier les recommandations du directeur
    tournament_data = load_tournament_data(filePath, tournament.tournamentId)
    if tournament_data and 'directorRecommendations' in tournament_data:
        director_recommendations = tournament_data['directorRecommendations']
    else:
        director_recommendations = ''

    print(director_recommendations)

    # Si les recommandations du directeur sont vides, les demander et les sauvegarder
    if director_recommendations == '':
        print('director recommendations ?')
        new_director_recommendations = view.getDirectorRecommendations()
        tournament.addDirectorRecommendations(new_director_recommendations)
        model.saveTournamentInfo(tournament, filePath)

def load_tournament_data(filePath, tournamentId):
    with open(filePath, 'r') as file:
        data = json.load(file)
        for t in data.get("tournaments", []):
            if t["tournamentId"] == tournamentId:
                return t
    return None


createTournament()
