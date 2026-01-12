import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

def calculate_player_distances(frame_data):
    # Filter for tracked players and extract coordinates
    players = frame_data[frame_data['player'].notnull()].copy()
    player_names = players['player'].tolist()
    coords = players[['x_ft', 'y_ft']].values
    
    dist_matrix = {}
    
    # Generate distance matrix between all players
    for i, name_a in enumerate(player_names):
        dist_matrix[name_a] = {}
        for j, name_b in enumerate(player_names):
            dist_matrix[name_a][name_b] = euclidean(coords[i], coords[j])
            
    return pd.DataFrame(dist_matrix)

def get_closest_defender(puck_carrier_name, frame_data):
    # Get carrier team to identify opponents
    carrier = frame_data[frame_data['player'] == puck_carrier_name].iloc[0]
    carrier_team = carrier['team_name']
    
    # Calculate distance to all players on the opposing team
    opponents = frame_data[(frame_data['team_name'] != carrier_team) & (frame_data['player'].notnull())]
    
    distances = []
    for _, opp in opponents.iterrows():
        dist = euclidean((carrier['x_ft'], carrier['y_ft']), (opp['x_ft'], opp['y_ft']))
        distances.append((opp['player'], dist))
    
    # Sort by proximity and return the nearest defender
    distances.sort(key=lambda x: x[1])
    return distances[0] 

if __name__ == "__main__":
    from src.data_factory import get_enriched_tracking
    
    # Configuration for local testing
    game_dir = "data/tracking/2022-02-08 Canada at USA/"
    t_path = game_dir + "2022-02-08 Canada at USA P1 PP1.csv"
    r_path = game_dir + "2022-02-08 Canada at USA roster.csv"
    
    # Load data and run example calculation
    df = get_enriched_tracking(t_path, r_path)
    frame_301 = df[df['frame_id'] == 301]
    
    name, dist = get_closest_defender("Rebecca Johnston", frame_301)
    print(f"Closest defender to Rebecca Johnston is {name} at {dist:.2f} feet.")