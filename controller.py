import model
import view


def createTournament():
    filePath = 'data.json'
    model.initialize_tournament_file(filePath)

    existing_tournaments = model.list_tournaments(filePath)
    view.displayExistingTournaments(existing_tournaments)

    load_existing = view.askUserToLoadExistingTournament()
    if load_existing:
        tournamentId = view.askUserForTournamentId()
        numberOfPlayers = view.getNumberOfPlayers()
        numberOfRounds = view.getNumberOfRounds()
        tournament = model.load_or_create_tournament(
            tournamentId, filePath, numberOfPlayers, numberOfRounds
        )

    else:
        tournament = model.create_new_tournament(filePath)

    model.finalize_tournament(tournament, filePath)


createTournament()
