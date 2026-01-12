import pandas as pd

def process_tracking_file(filepath):
    # Load raw tracking data
    df = pd.read_csv(filepath)
    
    # Identify unique teams present in the dataset
    teams = df['team_name'].unique()
    if len(teams) >= 2:
        print(f"Data contains: {teams[0]} vs {teams[1]}")
    
    # Calculate total duration based on frame count
    total_frames = df['frame_id'].nunique()
    print(f"Total animation frames: {total_frames}")
    
    return df

if __name__ == "__main__":
    # Path configuration for validation
    test_file = 'data/tracking/2022-02-08 Canada at USA P1 PP1.csv'
    
    # Load and inspect the first several rows of data
    df = process_tracking_file(test_file)
    print("\nInitial Tracking Data Preview:")
    print(df.head(10))
