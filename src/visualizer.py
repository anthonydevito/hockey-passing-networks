import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from src.data_factory import get_enriched_tracking 

def plot_frame(frame_id, enriched_df, rink_image_path):
    # Filter for specific frame and remove bench/off-ice coordinates
    frame_data = enriched_df[
        (enriched_df['frame_id'] == frame_id) & 
        (enriched_df['x_ft'] > 0) & (enriched_df['x_ft'] < 200) & 
        ~((enriched_df['x_ft'] == 100) & (enriched_df['y_ft'] == 42.5))
    ].copy()

    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Load and render rink background
    if os.path.exists(rink_image_path):
        img = mpimg.imread(rink_image_path)
        ax.imshow(img, extent=[0, 200, 0, 85], origin='lower', alpha=0.8)

    # Standardized team colors
    team_colors = {'Canada': '#ef3e42', 'USA': '#002868'}
    
    # Isolate player data and remove duplicate jersey entries
    players = frame_data[frame_data['jersey_number'] != 100].drop_duplicates(subset=['jersey_number'])

    # Plot players grouped by team
    for team in players['team_display'].unique():
        team_bits = players[players['team_display'] == team]
        color = team_colors.get(team, 'gray')
        
        ax.scatter(team_bits['x_ft'], team_bits['y_ft'], s=250, 
                   color=color, edgecolors='white', linewidth=2, label=team, zorder=3)

        # Annotate players with name or jersey number
        for _, row in team_bits.iterrows():
            name = row['player'] if pd.notnull(row['player']) else f"#{int(row['jersey_number'])}"
            ax.annotate(name, (row['x_ft'], row['y_ft']), xytext=(5, 5), 
                        textcoords='offset points', fontsize=9, fontweight='bold',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    # Plot puck position (ID 100)
    puck_df = frame_data[frame_data['jersey_number'] == 100]
    if not puck_df.empty:
        ax.scatter(puck_df['x_ft'].iloc[0], puck_df['y_ft'].iloc[0], color='#ffff00', 
                   s=100, edgecolors='black', label='Puck', zorder=10)

    ax.set_title(f"Game State Visualization | Frame {frame_id}", fontsize=14)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Local paths for testing
    game_dir = "data/tracking/2022-02-08 Canada at USA/"
    tracking_csv = os.path.join(game_dir, "2022-02-08 Canada at USA P1 PP1.csv")
    roster_csv = os.path.join(game_dir, "2022-02-08 Canada at USA roster.csv")
    rink_img = "data/tracking/iihf-rink.png"

    # Process and visualize specific frame
    df = get_enriched_tracking(tracking_csv, roster_csv)
    plot_frame(500, df, rink_img)
