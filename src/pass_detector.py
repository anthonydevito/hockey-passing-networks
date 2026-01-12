import pandas as pd
import numpy as np

def detect_passes(enriched_df, distance_threshold=7.0):
    # Isolate puck data (ID 100) and player data
    puck_df = enriched_df[enriched_df['jersey_number'] == 100].drop_duplicates(subset=['frame_id']).copy()
    player_df = enriched_df[enriched_df['jersey_number'] != 100].copy()

    # Align puck coordinates with player positions for each frame
    merged = player_df.merge(
        puck_df[['frame_id', 'x_ft', 'y_ft']], 
        on='frame_id', 
        suffixes=('', '_puck')
    )

    # Calculate Euclidean distance between players and the puck
    merged['dist_to_puck'] = np.sqrt(
        (merged['x_ft'] - merged['x_ft_puck'])**2 + 
        (merged['y_ft'] - merged['y_ft_puck'])**2
    )

    # Filter for proximity-based possession events
    possessions = merged[merged['dist_to_puck'] < distance_threshold].copy()
    possessions = possessions.sort_values('frame_id')

    # Detect possession transitions between different players
    possessions['player_changed'] = possessions['player'] != possessions['player'].shift(1)
    pass_events = possessions[possessions['player_changed']].copy()

    # Define pass origin and destination sequences
    pass_events['pass_from'] = pass_events['player'].shift(1)
    pass_events['pass_to'] = pass_events['player']
    pass_events['team'] = pass_events['team_display']

    # Filter for valid successful passes (same team, different players)
    successful_passes = pass_events[
        (pass_events['team'] == pass_events['team'].shift(1)) & 
        (pass_events['pass_from'] != pass_events['pass_to'])
    ].dropna(subset=['pass_from', 'pass_to'])

    return successful_passes

if __name__ == "__main__":
    from src.data_factory import get_enriched_tracking
    import os

    # Validation configuration
    game_dir = "data/tracking/2022-02-08 Canada at USA/"
    t_path = os.path.join(game_dir, "2022-02-08 Canada at USA P1 PP1.csv")
    r_path = os.path.join(game_dir, "2022-02-08 Canada at USA roster.csv")
    
    # Process tracking data and detect successful completions
    df = get_enriched_tracking(t_path, r_path)
    passes = detect_passes(df, distance_threshold=7.0)
    
    print(f"\n--- PASS DETECTION VALIDATION ---")
    print(f"Total passes detected: {len(passes)}")
    
    if not passes.empty:
        print("\nPrimary Passing Connections:")
        print(passes.groupby(['pass_from', 'pass_to']).size().sort_values(ascending=False))
