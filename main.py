from ranking_files.nfl_ranking import rank_nfl_from_games
from nfl_games.nfl_2025 import results_nfl2025
from nfl_games.nfl_2024 import results_nfl2024
from ranking_files.fbs_ranking import rank_fbs_from_games
from fbs_games.fbs_2025 import results_fbs2025
from ranking_files.ranking import print_nfl_rankings, print_fbs_rankings, print_top_25


def main():
    nfl_ranking_2025 = rank_nfl_from_games(results_nfl2025)
    nfl_ranking_2024 = rank_nfl_from_games(results_nfl2024)
    college_ranking_2025 = rank_fbs_from_games(results_fbs2025)
    print_nfl_rankings(nfl_ranking_2024, "2024 NFL Rankings")
    print()
    print_nfl_rankings(nfl_ranking_2025, "2025 NFL Rankings")
    print()
    print_fbs_rankings(college_ranking_2025, "2025 College Rankings")
    print()
    print_top_25(college_ranking_2025, "2025 ME College Football Top 25")


if __name__ == '__main__':
    main()
