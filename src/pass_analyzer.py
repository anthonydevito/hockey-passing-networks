import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import pandas as pd
from src.data_factory import get_enriched_tracking
from scipy.spatial.distance import euclidean

def plot_passing_lanes(frame_id, enriched_df, rink_image_path):
    # Filter for valid on-ice coordinates for the specific frame
    frame_data = enriched_df[
        (enriched_df['frame_id'] == frame_id) & 
        (enriched_df['x_ft'] > 0) & (enriched_df['x_ft'] < 200) &
        ~((enriched_df['x_ft'] == 100) & (enriched_df['y_ft'] == 42.5))
    ].copy()
    
    # Identify the puck and player positions
    puck_rows = frame_data[frame_data['jersey_number'] == 100]
    if puck_rows.empty:
        return 
    
    puck = puck_rows.iloc[0]
    players = frame_data[frame_data['jersey_number'] != 100].drop_duplicates(subset=['jersey_number', 'team_name'])

    # Determine puck carrier by proximity
    players['dist_to_puck'] = players.apply(lambda r: euclidean((r['x_ft'], r['y_ft']), (puck['x_ft'], puck['y_ft'])), axis=1)
    carrier = players.sort_values('dist_to_puck').iloc[0]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    if os.path.exists(rink_image_path):
        img = mpimg.imread(rink_image_path)
        ax.imshow(img, extent=[0, 200, 0, 85], origin='lower')

    # Analyze lanes to teammates based on defensive pressure
    teammates = players[players['team_name'] == carrier['team_name']]
    opponents = players[players['team_name'] != carrier['team_name']]
    
    for _, tm in teammates.iterrows():
        if tm['jersey_number'] == carrier['jersey_number']: 
            continue
        
        # Calculate distance to nearest opponent to determine lane status
        dist_to_opps = [euclidean((tm['x_ft'], tm['y_ft']), (opp['x_ft'], opp['y_ft'])) for _, opp in opponents.iterrows()]
        is_open = not dist_to_opps or min(dist_to_opps) > 7
        color = 'green' if is_open else 'red'
            
        ax.plot([carrier['x_ft'], tm['x_ft']], [carrier['y_ft'], tm['y_ft']], 
                color=color, linestyle='--', alpha=0.6)

    # Render players, puck, and metadata
    for team in players['team_name'].fillna("Opponent").unique():
        team_bits = players[players['team_name'].fillna("Opponent") == team]
        ax.scatter(team_bits['x_ft'], team_bits['y_ft'], s=150, edgecolors='black', label=team)

    ax.scatter(puck['x_ft'], puck['y_ft'], color='yellow', s=50, edgecolors='black', label='Puck', zorder=5)
    
    ax.set_title(f"Passing Lane Analysis - Frame {frame_id}")
    ax.set_axis_off()
    plt.legend(loc='lower left')
    plt.show()

if __name__ == "__main__":
    # Local configuration
    game_dir = "data/tracking/2022-02-08 Canada at USA/"
    t_path = os.path.join(game_dir, "2022-02-08 Canada at USA P1 PP1.csv")
    r_path = os.path.join(game_dir, "2022-02-08 Canada at USA roster.csv")
    rink_img = "data/tracking/iihf-rink.png"

    # Execution
    df = get_enriched_tracking(t_path, r_path)
    plot_passing_lanes(464, df, rink_img)
