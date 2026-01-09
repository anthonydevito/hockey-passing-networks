import pandas as pd

def process_tracking_file(filepath):
    df = pd.read_csv(filepath)
    
    # Identify teams involved
    teams = df['team_name'].unique()
    print(f"Analyzing {teams[0]} vs {teams[1]}")
    
    # Group by frame_id to see the "state" of the ice at a single moment
    total_frames = df['frame_id'].nunique()
    print(f"Total animation frames: {total_frames}")
    
    return df

if __name__ == "__main__":
    # Testing with one of the data files
    df = process_tracking_file('data/tracking/2022-02-08 Canada at USA P1 PP1.csv')
    print(df.head(10)) # This should show both Canada and Switzerland players for Frame 46