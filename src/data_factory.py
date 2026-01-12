import pandas as pd
import os

def get_enriched_tracking(tracking_path, roster_path):
    tracking = pd.read_csv(tracking_path)
    roster = pd.read_csv(roster_path)

    # Map tracking team names to roster labels
    team_map = {'USA': 'home', 'Canada': 'away'}
    tracking['roster_team_label'] = tracking['team_name'].map(team_map)

    # Perform initial join on jersey number and team label
    enriched = tracking.merge(
        roster, 
        left_on=['jersey_number', 'roster_team_label'], 
        right_on=['jn', 'team'], 
        how='left'
    )

    # Identification recovery: Use unique jersey numbers to fill missing player names
    jn_counts = roster['jn'].value_counts()
    unique_jns = jn_counts[jn_counts == 1].index
    unique_roster = roster[roster['jn'].isin(unique_jns)]
    
    backup_name_map = dict(zip(unique_roster['jn'], unique_roster['player']))
    backup_team_map = dict(zip(unique_roster['jn'], unique_roster['team']))

    # Target rows where player name is missing (excluding the puck)
    missing_mask = enriched['player'].isna() & (enriched['jersey_number'] != 100)
    
    enriched.loc[missing_mask, 'player'] = enriched.loc[missing_mask, 'jersey_number'].map(backup_name_map)
    enriched.loc[missing_mask, 'team'] = enriched.loc[missing_mask, 'jersey_number'].map(backup_team_map)

    # Generate consistent team names for visualization
    reverse_map = {v: k for k, v in team_map.items()}
    enriched['team_display'] = enriched['team'].map(reverse_map).fillna(enriched['team_name'])

    return enriched

if __name__ == "__main__":
    # Local paths for data validation
    game_dir = "data/tracking/2022-02-08 Canada at USA/"
    t_path = os.path.join(game_dir, "2022-02-08 Canada at USA P1 PP1.csv")
    r_path = os.path.join(game_dir, "2022-02-08 Canada at USA roster.csv")
    
    # Process data and verify specific frame mapping
    df = get_enriched_tracking(t_path, r_path)
    check = df[(df['frame_id'] == 464) & (df['x_ft'] > 0) & (df['x_ft'] < 200)]
    
    print("\n--- DATA ENRICHMENT VERIFICATION (Frame 464) ---")
    print(check[['team_display', 'jersey_number', 'player']].dropna().sort_values('team_display'))