import pandas as pd
import numpy as np
import os
from src.data_factory import get_enriched_tracking
from src.pass_detector import detect_passes

def generate_report(enriched_df, passes_df):
    print("\n" + "="*40)
    print("      HOCKEY ANALYTICS SCOUTING REPORT")
    print("="*40)
    
    # Calculate possession metrics based on puck proximity
    puck_df = enriched_df[enriched_df['jersey_number'] == 100].drop_duplicates(subset=['frame_id'])
    player_df = enriched_df[enriched_df['jersey_number'] != 100]
    
    merged = player_df.merge(puck_df[['frame_id', 'x_ft', 'y_ft']], on='frame_id', suffixes=('', '_puck'))
    merged['dist_to_puck'] = np.sqrt((merged['x_ft'] - merged['x_ft_puck'])**2 + (merged['y_ft'] - merged['y_ft_puck'])**2)
    
    # Filter for frames where a player is within control distance (7ft)
    possession_frames = merged[merged['dist_to_puck'] < 7.0]
    total_pos = possession_frames['frame_id'].nunique()
    
    # Calculate team-wise possession share
    team_share = possession_frames.groupby('team_display')['frame_id'].nunique() / total_pos * 100
    
    print(f"\n[POSSESSION SUMMARY]")
    for team, pct in team_share.items():
        print(f" - {team:10}: {pct:4.1f}% of possession")

    # Analyze passing volume and top combinations
    print(f"\n[BALL MOVEMENT]")
    if not passes_df.empty:
        playmakers = passes_df['pass_from'].value_counts()
        print(f" - Leading Playmaker: {playmakers.index[0]} ({playmakers.iloc[0]} passes)")
        
        top_conn = passes_df.groupby(['pass_from', 'pass_to']).size().idxmax()
        print(f" - Key Partnership  : {top_conn[0]} -> {top_conn[1]}")
    else:
        print(" - No completed passing sequences detected.")

    # Evaluate team positioning during puck control
    usa_possession = possession_frames[possession_frames['team_display'] == 'USA']
    print(f"\n[TACTICAL NOTES]")
    if not usa_possession.empty:
        usa_x_avg = usa_possession['x_ft'].mean()
        if usa_x_avg > 170:
            print(" - USA Defensive Focus: Positioning is heavily localized in the defensive zone.")
        else:
            print(" - USA Transition Play: Team is effectively moving through the neutral zone.")
    
    print("="*40 + "\n")

if __name__ == "__main__":
    # Path configuration
    game_dir = "data/tracking/2022-02-08 Canada at USA/"
    t_path = os.path.join(game_dir, "2022-02-08 Canada at USA P1 PP1.csv")
    r_path = os.path.join(game_dir, "2022-02-08 Canada at USA roster.csv")
    
    # Generate enriched dataset and detect events
    df = get_enriched_tracking(t_path, r_path)
    passes = detect_passes(df, distance_threshold=7.0)
    
    # Run analytics summary
    generate_report(df, passes)
