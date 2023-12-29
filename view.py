# first details about tournament

def getTournamentName():
    name = input("Enter the tournament name: ")
    return name

def getTournamentPlace():
    place = input("Enter the tournament place: ")
    return place

def getTournamentDate():
    date = input("Enter the tournament date (DD/MM/YYYY): ")
    return date


# number of players
def getNumberOfPlayers():
    return int(input("Enter number of players: "))


# Enter the infos of each player
def getPlayerDetails(playerNumber):
    print(f"Enter details for Player {playerNumber}:")
    lastName = input("Last Name: ")
    firstName = input("First Name: ")
    dateOfBirth = input("Date of Birth (DD/MM/YYYY): ")
    id = input("ID: ")
    return lastName, firstName, dateOfBirth, id


# Choose the number of rounds
def getNumberOfRounds():
    return int(input("Enter number of rounds: "))


# Display the player after its creation
def displayPlayer(self):
    return (
        f"Player(ID: {self.id}, Last Name: {self.lastName}, "
        f"First Name: {self.firstName}, Birth Date: {self.dateOfBirth})"
    )


# Display the final ranking
def displayFinalRanking(players):
    sorted_players = sorted(players, key=lambda x: x.points, reverse=True)
    last_score = None
    last_rank = 0
    rank_increment = 1

    print("\nFinal Ranking:")
    for player in sorted_players:
        if player.points != last_score:
            last_score = player.points
            last_rank += rank_increment
            rank_increment = 1
        else:
            rank_increment += 1

        # Format points to remove trailing '.0' for whole numbers
        if player.points % 1:
            points_display = f"{player.points:.1f}".rstrip('0').rstrip('.')
        else:
            points_display = int(player.points)

        print(
            f"{player.firstName} {player.lastName} is at the "
            f"{ordinal(last_rank)} place with {points_display} points"
        )


# Choose the suffix for the ranking
def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


# Display the round number
def displayRound(roundNumber):
    print(f"Round {roundNumber}")


# Director's recommandations
def getDirectorRecommendations():
    return input("Director's recommandations: ")

def askUserToLoadExistingTournament():
    while True:
        response = input("Voulez-vous charger un tournoi existant ? (oui/non) : ").strip().lower()
        if response in ["oui", "non"]:
            return response == "oui"
        else:
            print("Réponse non valide. Veuillez répondre par 'oui' ou 'non'.")

def askUserForTournamentId():
    return input("Veuillez entrer l'ID du tournoi à charger : ").strip()

def displayExistingTournaments(tournaments):
    print("Tournois existants :")
    for t in tournaments:
        print(f"ID: {t['id']}, Nom: {t['name']}, Lieu: {t['place']}, Date: {t['date']}")

