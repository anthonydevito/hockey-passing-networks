import pandas as pd
import os

def test_data_alignment():
    game_dir = "data/tracking/2022-02-08 Canada at USA/"
    tracking_path = os.path.join(game_dir, "2022-02-08 Canada at USA P1 PP1.csv")
    roster_path = os.path.join(game_dir, "2022-02-08 Canada at USA roster.csv")

    # Load data
    tracking = pd.read_csv(tracking_path)
    roster = pd.read_csv(roster_path)

    # Join tracking data with roster names
    # Note: jersey_number 100 is the puck
    enriched = tracking.merge(roster, left_on='jersey_number', right_on='jn', how='left')

    print(f"Successfully merged data!")
    print(f"Sample of identified players in the tracking stream:")
    print(enriched[enriched['player'].notnull()][['frame_id', 'player', 'team_name']].head(10))

if __name__ == "__main__":
    test_data_alignment()