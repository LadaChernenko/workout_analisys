# Workout Analysis Pipeline
This repository contains the code and resources for a Workout Analysis Pipeline, designed to process and analyze workout data extracted from training diaries on social media (VK). The pipeline automates the collection, processing, and visualization of workout metrics using a combination of Python scripts, APIs for large language models (LLMs), and data visualization libraries.

## Key Features
**Data Collection**: Automates the parsing of VK posts to retrieve training diary entries.
**Preprocessing**: Cleans and structures the raw text using regular expressions and classification methods.
**LLM Integration**: Extracts key workout metrics such as repetitions, sets, and exercise names from unstructured text using LLM APIs.
**Post-processing**: Converts extracted metrics into structured formats (e.g., tables) for easier analysis.
**Visualization**: Generates dashboards and graphs to summarize workout data trends and insights.

## Repository Structure
- `get_data.py`: Fetches posts from VK and extracts workout-related texts.
- `data_prep.py`: Preprocesses and classifies raw text data for further analysis.
- `summarisation.py`: Handles interactions with LLM APIs, including sending queries and parsing responses.
- `pipeline.py`: Executes the entire processing pipeline, integrating all stages of data collection, preprocessing, LLM analysis, and post-processing.
- `utils.py`: Includes utility functions for handling JSON format corrections and other data operations.
- `analisys.ipynb`: A Jupyter Notebook for creating visualizations and dashboards based on the processed data.

## Technologies Used

**Programming Language**: Python 3.10
**Libraries**:
**Data Collection and Processing**: requests, tqdm, fire
**Natural Language Processing**: LLM APIs (e.g., OpenAI)
**Visualization**: pandas, matplotlib, seaborn

## Getting Started
Clone the repository:

```bash
git clone <repository>
cd <repository>
```

Set up a virtual environment:
```bash

VENV_NAME=venv
python3.10 -m venv $VENV_NAME
. "$VENV_NAME"/bin/activate
python3.10 -m pip install -r requirements.txt
```
Run the pipeline: Execute scripts or utilize the Jupyter Notebook for data analysis and visualization.