# Hockey Passing Network Analysis

A Python-based sports analytics pipeline that transforms raw coordinate tracking data into tactical insights. This project uses IIHF Olympic tracking data to visualize player positioning, detect successful passing sequences, and generate automated scouting reports.



## 🚀 Features

* **Data Enrichment:** Automatically merges raw tracking coordinates with team rosters.
* **Pass Detection Engine:** A proximity-based algorithm that identifies puck possession and successful pass completions.
* **Tactical Visualizers:**
    * **Passing Networks:** Maps the volume and direction of movement.
    * **Lane Analysis:** Identifies open vs. closed lanes.
    * **Game State:** Visualizes 2D positioning.
* **Automated Scouting:** Generates text-based reports detailing possession share and key playmakers.

## 🛠️ Project Structure

```text
├── data/
│   ├── tracking/          # Raw CSV tracking files and rink images
│   └── rosters/           # Team roster CSVs
├── src/
│   ├── analytics.py       # Distance matrices and pressure metrics
│   ├── data_factory.py    # Data cleaning and enrichment pipeline
│   ├── pass_detector.py   # Possession and pass detection logic
│   ├── pass_analyzer.py   # Passing lane visualization
│   ├── network_map.py     # Aggregate passing network visualization
│   ├── visualizer.py      # Single-frame game state plotting
│   ├── tracking_loader.py # Raw data ingestion utilities
│   └── scouting_report.py # Analytical summary generator
└── README.md



## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/anthonydevito/hockey-passing-networks.git
cd hockey-passing-networks
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt  # or pip install pandas numpy matplotlib scipy
```


## 📊 Usage

1. Generate a Scouting Report
To see a summary of possession and playmaking:
```bash
python -m src.scouting_report
```

2. Visualize a Passing Network
To generate a map of all successful passes in a sequence:
```bash
python -m src.network_map
```

3. Analyze Passing Lanes
To see open lanes for a specific frame (e.g., frame 464):
```bash
python -m src.pass_analyzer
```


## 📝 Data Source
This project utilizes tracking data from the 2022 Beijing Winter Olympics (Canada vs. USA), featuring high-frequency coordinates for players and the puck.


## 🛠️ Requirements
* **Python 3.8+**
* **Pandas**: Data manipulation and analysis.
* **Matplotlib**: Core visualization engine.
* **SciPy**: Spatial distance calculations.
* **NumPy**: Vectorized coordinate mathematics.

## 🚀 Future Roadmap
* **Expected Pass Completion (xP):** Build a model to predict the probability of a pass being completed based on lane pressure.
* **Automated Shift Detection:** Automatically segmenting large tracking files into individual Power Play or Even Strength shifts.
* **Zone Entry Analytics:** Tracking how often players carry the puck across the blue line vs. dumping it in.
* **Animated Replays:** Exporting frame-by-frame visualizations as MP4 or GIF files for video review.


## ⚖️ License
Distributed under the MIT License. See LICENSE for more information.