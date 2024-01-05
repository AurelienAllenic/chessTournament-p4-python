import json


def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_players_alphabetically(data, file):
    player_names = set()
    for tournament in data["tournaments"]:
        for player in tournament["players"]:
            full_name = f"{player['firstName']} {player['lastName']}"
            player_names.add(full_name)
    for name in sorted(player_names):
        file.write(name + '\n')


def write_tournaments(data, file):
    for tournament in data["tournaments"]:
        file.write(f"{tournament['name']} - Date: {tournament['date']}\n")


def write_tournament_details(data, tournament_id, file):
    for tournament in data["tournaments"]:
        if tournament['tournamentId'] == tournament_id:
            file.write(f"\nDetails for Tournament: {tournament['name']}\n")
            file.write(f"Date: {tournament['date']}\n")
            file.write(f"Place: {tournament['place']}\n")
            break


def write_players_in_tournament_alphabetically(data, tournament_id, file):
    for tournament in data["tournaments"]:
        if tournament['tournamentId'] == tournament_id:
            player_names = [
                f"{p['firstName']} {p['lastName']}"
                for p in tournament["players"]
            ]
            for name in sorted(player_names):
                file.write(name + '\n')
            break


def write_tournament_rounds_and_matches(data, tournament_id, file):
    for tournament in data["tournaments"]:
        if tournament['tournamentId'] == tournament_id:
            file.write(f"\nRounds and Matches for {tournament['name']}:\n")
            for round_number, matches in tournament["rounds"].items():
                file.write(f"  Round {round_number}:\n")
                for match in matches:
                    player1 = match['player1']
                    player2 = match['player2']
                    winner = match['winner']
                    match_info = f"{player1} vs {player2}, Winner: {winner}\n"
                    file.write(match_info)
            break


def generate_report(data, report_file_path):
    with open(report_file_path, 'w') as file:
        file.write("Player Names (Alphabetically):\n")
        write_players_alphabetically(data, file)

        file.write("\nTournament Names:\n")
        write_tournaments(data, file)

        tournament_id = '894500b1-8f65-4726-9a22-3deb37e599ac'  # Exemple d'ID
        write_tournament_details(data, tournament_id, file)

        file.write("\nPlayers in Tournament (Alphabetically):\n")
        write_players_in_tournament_alphabetically(data, tournament_id, file)

        file.write("\nTournament Rounds and Matches:\n")
        write_tournament_rounds_and_matches(data, tournament_id, file)


data = load_data('./data.json')
generate_report(data, './tournament_report.txt')
