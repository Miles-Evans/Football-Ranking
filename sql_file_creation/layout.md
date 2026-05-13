# SQL Layout

## League
* ID (pk)
* League Name (string; either NFL or FBS)

## Team
* ID (pk)
* League ID (fk onto League)
* Name (string)

## Season
* ID (pk)
* League ID (fk onto League)
* Year (int)

## Games
* ID (pk)
* Season ID (fk onto Season)
* Week (int)
* Away Team ID (fk onto Team; can be NULL)
* Home Team ID (fk onto Team; can be NULL)
* Away Team Score (int)
* Home Team Score (int)
* Overtime (boolean)
* Home Raw Power Score Change (float)
* Away Raw Power Score Change (float)
* Bonus (int)

## Weekly Power Score
* ID (pk)
* Team ID (fk onto Team)
* Season ID (fk onto Season)
* Week (int)
* Power Score (float)
* Wins (int)
* Losses (int)
* Ties (int)
* Power Ranking (int)