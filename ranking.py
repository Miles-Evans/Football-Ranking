valid_fbs_teams = {
    "Boston College", "CAL", "Clemson", "Duke", "Florida State", "Georgia Tech", "Louisville", "Miami", "NC State",
    "UNC", "PITT", "SMU", "Stanford", "Syracuse", "Virginia", "Virginia Tech", "Wake Forest", "ARMY", "Charlotte",
    "East Carolina", "FAU", "Memphis", "NAVY", "North Texas", "RICE", "South Florida", "Temple", "Tulane", "Tulsa",
    "UAB", "UTSA", "Arizona State", "Arizona", "BYU", "Baylor", "Cincinnati", "Colorado", "Houston", "Iowa State",
    "Kansas", "Kansas State", "Oklahoma State", "TCU", "Texas Tech", "UCF", "UTAH", "West Virginia", "UL Monroe",
    "Indiana", "Ohio State", "USC", "Oregon", "Michigan", "Northwestern", "Nebraska", "Washington", "Iowa", "Minnesota",
    "UCLA", "Illinois", "Maryland", "Michigan State", "Penn State", "Rutgers", "Purdue", "Wisconsin", "Delaware",
    "FIU", "JAX STATE", "Kennesaw State", "Liberty", "Louisiana Tech", "Middle Tennessee", "Missouri State",
    "New Mexico State", "Sam Houston", "UTEP", "Western Kentucky", "Notre Dame", "UConn", "Akron", "Ball State",
    "Bowling Green", "Buffalo", "Central Michigan", "Eastern Michigan", "Kent State", "UMass", "M-OH",
    "Northern Illinois", "Ohio", "Toledo", "Western Michigan", "Air Force", "Boise State", "Colorado State",
    "Fresno State", "Hawai'i", "Nevada", "New Mexico", "San Diego State", "San Jose State", "UNLV", "Utah State",
    "Wyoming", "Oregon State", "Washington State", "Alabama", "Arkansas", "Auburn", "Florida", "Georgia", "Kentucky",
    "LSU", "Mississippi State", "Missouri", "Oklahoma", "Ole Miss", "South Carolina", "Tennessee", "Texas A&M", "Texas",
    "Vanderbilt", "App State", "Arkansas State", "Coastal Carolina", "Georgia Southern", "Georgia State",
    "James Madison", "Louisiana", "Marshall", "Old Dominion", "South Alabama", "Southern Miss", "Texas State", "TROY"
}


def get_bonus(diff, league):
    """Get power score modifier to adjust for score of the game."""
    if diff <= 3:
        return -1
    elif diff <= 10:
        return 0
    elif diff <= 17:
        return 1
    elif diff <= 24:
        return 2
    elif league == 'NFL' or (league == 'FBS' and diff <= 31):
        return 3
    else:
        return 4


def team_rankings(teams, games, scores, min_add, max_loss, league):
    """Get power score of teams based on games played."""
    start_score = 100.0
    divisor = 10.0
    tie_divisor = 50.0
    new_scores = {team: start_score for team in teams}

    for team1, team2, result, bonus in games:
        if league == 'FBS':
            t1_valid = team1 in valid_fbs_teams
            t2_valid = team2 in valid_fbs_teams
        else:
            t1_valid = True
            t2_valid = True

        if not t1_valid and not t2_valid:
            continue

        s1 = scores.get(team1)
        s2 = scores.get(team2)

        if result == 0:  # team1 win
            if t1_valid and t2_valid:
                gain = max(min_add, s2 / divisor) + bonus
                loss = (start_score / max(max_loss, s1 / divisor)) + bonus
            elif t1_valid:
                # valid team beat an invalid team gives min score addition with a -1 bonus
                gain = min_add - 1
                loss = 0
            elif t2_valid:
                # valid team lost to invalid team gives max score loss with a +4 bonus
                gain = 0
                loss = start_score / max_loss + 4
            else:
                continue
            if t1_valid:
                new_scores[team1] += gain
            if t2_valid:
                new_scores[team2] -= loss

        elif result == 1:  # team2 win
            if t1_valid and t2_valid:
                gain = max(min_add, s1 / divisor) + bonus
                loss = (start_score / max(max_loss, s2 / divisor)) + bonus
            elif t2_valid:
                gain = min_add
                loss = 0
            elif t1_valid:
                gain = 0
                loss = start_score / max_loss
            else:
                continue
            if t2_valid:
                new_scores[team2] += gain
            if t1_valid:
                new_scores[team1] -= loss

        else:  # tie
            # 0 minimum so you can't lose points from a tie
            if t1_valid and t2_valid:
                new_scores[team1] += max(0, (s2 / tie_divisor))
                new_scores[team2] += max(0, (s1 / tie_divisor))
            else:
                continue

    return new_scores


def print_nfl_rankings(ranking, season_label):
    """Print the NFL team rankings."""
    print(season_label)
    rank = 0
    max_rank = len(ranking)
    print(f"{'Rank':>{len(str(max_rank))}}  {'Team':^21}  {'Power Score':^10}  {'Record':^11}")
    for team, score, wins, losses, ties in ranking:
        rank += 1
        if ties > 0:
            record_str = f"(W:{wins:>2} - L:{losses:>2} - T:{ties:>2})"
        else:
            record_str = f"(W:{wins:>2} - L:{losses:>2})"
        print(f"{rank:>{len(str(max_rank))}})  {team:<22}: {score:>{8}.2f}   {record_str}")


def print_fbs_rankings(ranking, season_label):
    """Print the FBS team rankings."""
    print(season_label)
    max_rank = len(ranking)
    print(f"{'Rank':>{len(str(max_rank))}}  {'Team':^20}  {'Power Score':^10}  {'Record':^11}")
    for rank, (team, score, wins, losses) in enumerate(ranking, start=1):
        record_str = f"(W:{wins:>2} - L:{losses:>2})"
        print(f"{rank:>{len(str(max_rank))}})  {team:<20}: {score:>{8}.2f}   {record_str}")


def print_top_25(ranking, season_label):
    """Print the top 25 teams according to the ME ranking system."""
    print(season_label)
    max_rank = 25
    print(f"{'Rank':>{len(str(max_rank))}}  {'Team':^20}  {'Power Score':^10}  {'Record':^11}")
    for rank, (team, score, wins, losses) in enumerate(ranking, start=1):
        record_str = f"(W:{wins:>2} - L:{losses:>2})"
        print(f"{rank:>{len(str(max_rank))}})  {team:<20}: {score:>{8}.2f}   {record_str}")
        if rank == 25:
            break
