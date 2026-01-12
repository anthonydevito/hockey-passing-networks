import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from src.data_factory import get_enriched_tracking
from src.pass_detector import detect_passes

def plot_passing_network(enriched_df, passes_df, team_name, rink_image_path):
    # Filter tracking and pass data for the selected team
    team_data = enriched_df[enriched_df['team_display'] == team_name].copy()
    team_passes = passes_df[passes_df['team'] == team_name].copy()
    
    # Filter for valid on-ice coordinates
    on_ice = team_data[
        (team_data['x_ft'] > 0) & (team_data['x_ft'] < 200) & 
        ~((team_data['x_ft'] == 100) & (team_data['y_ft'] == 42.5))
    ].copy()

    # Filter for active players (minimum 30% frame presence) to remove bench noise
    min_frames = on_ice['frame_id'].nunique() * 0.30
    player_counts = on_ice['player'].value_counts()
    active_players = player_counts[player_counts > min_frames].index
    on_ice = on_ice[on_ice['player'].isin(active_players)]

    # Calculate mean positions for nodes
    avg_pos = on_ice.groupby('player').agg({'x_ft': 'mean', 'y_ft': 'mean'}).reset_index()
    pos_dict = dict(zip(avg_pos['player'], zip(avg_pos['x_ft'], avg_pos['y_ft'])))

    # Aggregate total passes between player pairs for edge weights
    pass_counts = team_passes.groupby(['pass_from', 'pass_to']).size().reset_index(name='count')

    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Initialize rink background
    if os.path.exists(rink_image_path):
        img = mpimg.imread(rink_image_path)
        ax.imshow(img, extent=[0, 200, 0, 85], origin='lower', alpha=0.5)
    else:
        ax.set_xlim(0, 200); ax.set_ylim(0, 85)
        ax.plot([0, 200, 200, 0, 0], [0, 0, 85, 85, 0], color='black')

    # Plot passing edges with scaled line widths
    for _, row in pass_counts.iterrows():
        p1, p2 = row['pass_from'], row['pass_to']
        if p1 in pos_dict and p2 in pos_dict:
            start, end = pos_dict[p1], pos_dict[p2]
            width = row['count'] * 4 
            ax.annotate("", xy=end, xytext=start,
                        arrowprops=dict(arrowstyle="->", color="black", lw=width, alpha=0.3, 
                                        shrinkA=25, shrinkB=25, connectionstyle="arc3,rad=0.1"))

    # Plot player nodes and labels with collision avoidance
    color = '#002868' if team_name == 'USA' else '#ef3e42'
    avg_pos = avg_pos.sort_values('y_ft')
    
    for i, row in avg_pos.iterrows():
        name = row['player'].split()[-1]
        x, y = row['x_ft'], row['y_ft']
        
        ax.scatter(x, y, s=600, color=color, edgecolors='white', linewidth=2, zorder=5)

        # Apply vertical jitter to labels to prevent overlap
        y_offset = -5 if i % 2 == 0 else 5
        ax.text(x, y + y_offset, name, ha='center', va='center', 
                fontsize=9, fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.9, edgecolor=color, boxstyle='round,pad=0.2'),
                zorder=10)

    ax.set_title(f"{team_name} Passing Network Map", fontsize=20, pad=20)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # File configuration
    game_dir = "data/tracking/2022-02-08 Canada at USA/"
    tracking_file = os.path.join(game_dir, "2022-02-08 Canada at USA P1 PP1.csv")
    roster_file = os.path.join(game_dir, "2022-02-08 Canada at USA roster.csv")
    rink_img = "data/tracking/iihf-rink.png"

    # Execution pipeline
    df = get_enriched_tracking(tracking_file, roster_file)
    passes = detect_passes(df, distance_threshold=7.0)
    plot_passing_network(df, passes, 'USA', rink_img)
