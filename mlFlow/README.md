# nlp-youtube-toxicity-analysis

This project focuses on analyzing YouTube comments for toxicity using machine learning techniques. The main components of the project include exploratory data analysis (EDA), model experimentation, and comparison of various models.

## Project Structure

- **notebooks/**: Contains Jupyter notebooks for EDA and model experimentation.
  - `eda-nlp.ipynb`: Performs exploratory data analysis on the YouTube comments dataset.
  - `mlflow-experiments.ipynb`: Designed for running experiments with MLflow to track models and parameters.
  - `model-comparison.ipynb`: Compares the performance of various models using MLflow for tracking results.

- **data/**: Contains the datasets used in the project.
  - **raw/**: Contains the raw dataset.
    - `youtoxic_english_1000.csv`: Raw dataset of YouTube comments labeled for toxicity.
  - **processed/**: Directory for storing processed data files after preprocessing.

- **src/**: Contains source code for data processing and model utilities.
  - `__init__.py`: Marks the directory as a Python package.
  - `data_preprocessing.py`: Functions for cleaning and preprocessing the YouTube comments dataset.
  - `feature_engineering.py`: Functions for extracting features from the dataset for model training.
  - `model_utils.py`: Utility functions for model training, evaluation, and saving/loading models.

- **mlruns/**: Directory created by MLflow to store results of experiments and model runs.

- **models/**: Directory for storing trained models.

- **experiments/**: Contains scripts for tracking experiments.
  - `mlflow_tracking.py`: Code for tracking experiments using MLflow, including logging parameters, metrics, and models.

- **requirements.txt**: Lists the Python dependencies required for the project.

- **environment.yml**: Used to create a conda environment with the specified dependencies.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd nlp-youtube-toxicity-analysis
   ```

2. Install the required dependencies:
   - Using pip:
     ```
     pip install -r requirements.txt
     ```
   - Or using conda:
     ```
     conda env create -f environment.yml
     ```

3. Launch Jupyter Notebook:
   ```
   jupyter notebook
   ```

4. Open the notebooks in the `notebooks/` directory to start your analysis.

## Usage Guidelines

- Use `eda-nlp.ipynb` for initial data exploration and visualization.
- Use `mlflow-experiments.ipynb` to run and track different machine learning models.
- Use `model-comparison.ipynb` to evaluate and compare the performance of the models.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.