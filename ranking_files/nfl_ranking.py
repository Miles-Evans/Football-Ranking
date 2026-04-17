from collections import defaultdict
from ranking_files.ranking import team_rankings, get_bonus

nfl_aliases = {
    'arizona cardinals': "Arizona Cardinals",
    'cardinals': 'Arizona Cardinals',
    'atlanta falcons': 'Atlanta Falcons',
    'falcons': 'Atlanta Falcons',
    'baltimore ravens': 'Baltimore Ravens',
    'ravens': 'Baltimore Ravens',
    'buffalo bills': 'Buffalo Bills',
    'bills': 'Buffalo Bills',
    'carolina panthers': 'Carolina Panthers',
    'panthers': 'Carolina Panthers',
    'chicago bears': 'Chicago Bears',
    'bears': 'Chicago Bears',
    'cincinnati bengals': 'Cincinnati Bengals',
    'bengals': 'Cincinnati Bengals',
    'cleveland browns': 'Cleveland Browns',
    'browns': 'Cleveland Browns',
    'dallas cowboys': 'Dallas Cowboys',
    'cowboys': 'Dallas Cowboys',
    'denver broncos': 'Denver Broncos',
    'broncos': 'Denver Broncos',
    'detroit lions': 'Detroit Lions',
    'lions': 'Detroit Lions',
    'green bay packers': 'Green Bay Packers',
    'packers': 'Green Bay Packers',
    'houston texans': 'Houston Texans',
    'texans': 'Houston Texans',
    'indianapolis colts': 'Indianapolis Colts',
    'colts': 'Indianapolis Colts',
    'jacksonville jaguars': 'Jacksonville Jaguars',
    'jaguars': 'Jacksonville Jaguars',
    'kansas city chiefs': 'Kansas City Chiefs',
    'chiefs': 'Kansas City Chiefs',
    'las vegas raiders': 'Las Vegas Raiders',
    'raiders': 'Las Vegas Raiders',
    'los angeles chargers': 'Los Angeles Chargers',
    'chargers': 'Los Angeles Chargers',
    'los angeles rams': 'Los Angeles Rams',
    'rams': 'Los Angeles Rams',
    'miami dolphins': 'Miami Dolphins',
    'dolphins': 'Miami Dolphins',
    'minnesota vikings': 'Minnesota Vikings',
    'vikings': 'Minnesota Vikings',
    'new england patriots': 'New England Patriots',
    'patriots': 'New England Patriots',
    'new orleans saints': 'New Orleans Saints',
    'saints': 'New Orleans Saints',
    'new york giants': 'New York Giants',
    'giants': 'New York Giants',
    'new york jets': 'New York Jets',
    'jets': 'New York Jets',
    'philadelphia eagles': 'Philadelphia Eagles',
    'eagles': 'Philadelphia Eagles',
    'pittsburgh steelers': 'Pittsburgh Steelers',
    'steelers': 'Pittsburgh Steelers',
    'san francisco 49ers': 'San Francisco 49ers',
    '49ers': 'San Francisco 49ers',
    'seattle seahawks': 'Seattle Seahawks',
    'seahawks': 'Seattle Seahawks',
    'tampa bay buccaneers': 'Tampa Bay Buccaneers',
    'buccaneers': 'Tampa Bay Buccaneers',
    'tennessee titans': 'Tennessee Titans',
    'titans': 'Tennessee Titans',
    'washington commanders': 'Washington Commanders',
    'commanders': 'Washington Commanders'
}


def normalize_team(name):
    return nfl_aliases.get(name.lower())


def rank_nfl_from_games(games, max_iterations=1000, tolerance=1e-3):
    """
    Rank NFL teams based on game results and opponent strength.

    games: list of tuples (team1, team2, team1_points, team2_points, week [, overtime])
      - team1_points > team2_points → team1 wins
      - team2_points > team1_points → team2 wins
      - tie if equal
      - optional 5th value (bool): True = game went to overtime
    """
    # Normalize and extract teams
    normalized = []
    for game in games:
        if len(game) == 6:
            team1, team2, pts1, pts2, week, overtime = game
        else:
            team1, team2, pts1, pts2, week = game
            overtime = False

        t1 = normalize_team(team1)
        t2 = normalize_team(team2)

        diff = abs(pts1 - pts2)
        bonus = -2 if overtime else get_bonus(diff, 'NFL')

        if pts1 > pts2:
            result = 0  # team1 win
        elif pts2 > pts1:
            result = 1  # team1 loss
        else:
            result = 2  # tie

        normalized.append((t1, t2, result, bonus))

    start_score = 100.0
    teams = set([t for g in normalized for t in g[:2]])
    scores = {team: start_score for team in teams}

    # Track record
    record = defaultdict(lambda: {"wins": 0, "losses": 0, "ties": 0})
    for team1, team2, result, _ in normalized:
        if result == 0:
            record[team1]["wins"] += 1
            record[team2]["losses"] += 1
        elif result == 1:
            record[team2]["wins"] += 1
            record[team1]["losses"] += 1
        else:
            record[team1]["ties"] += 1
            record[team2]["ties"] += 1

    # Iterative score adjustment
    for _ in range(max_iterations):
        new_scores = team_rankings(teams, normalized, scores, 6.0, 5.0, 'NFL')

        diffs = [abs(new_scores[t] - scores[t]) for t in scores]
        scores = new_scores
        if all(d < tolerance for d in diffs):
            break

    # Combine into ranking with records
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = [
        (team, score, record[team]["wins"], record[team]["losses"], record[team]["ties"])
        for team, score in ranked
    ]
    return results
