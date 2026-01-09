import pandas as pd

def get_enriched_tracking(tracking_path, roster_path):
    # Load data
    tracking_df = pd.read_csv(tracking_path)
    roster_df = pd.read_csv(roster_path)
    
    # In this dataset, we join on jersey_number (tracking) and jn (roster)
    # Note: tracking jersey_number 100 I think is the puck?  so might have to handle that later
    enriched_df = tracking_df.merge(
        roster_df[['player', 'jn', 'position']], 
        left_on='jersey_number', 
        right_on='jn', 
        how='left'
    )
    
    return enriched_df

if __name__ == "__main__":
    # Test join
    game_folder = "data/TrackingData/2022-02-08 ROC at Finland/"
    tracking_file = game_folder + "2022-02-08 ROC at Finland P1 PP1.csv"
    roster_file = game_folder + "2022-02-08 ROC at Finland roster.csv"
    
    df = get_enriched_tracking(tracking_file, roster_file)
    print(df[['frame_id', 'player', 'x_ft', 'y_ft']].head(10))