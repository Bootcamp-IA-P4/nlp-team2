# Modzilla: API for comment moderation on YouTube

<div align="center">
  <img src="https://res.cloudinary.com/diowtsfaq/image/upload/v1752495470/logoFull_s3ytcn.png" alt="Descripción de la imagen" width="600" height="500">
</div>


## 📚 Table of Contents

1. [🧾 Overview](#overview)
2. [🎯 System Purpose and Scope](#system-purpose-and-scope)
3. [🔍 Main Features](#-main-features)
4. [💡 Possible Improvements](#-possible-improvements)
5. [📁 Folder Structure](#-folder-structure)
6. [🏗️ Architecture Diagram](#-architecture-diagram)
7. [⚙️ Installation and Usage](#️-installation-and-usage)
   - [1️⃣ Clone the repository](#1️⃣-clone-the-repository)
   - [2️⃣ Create and activate the virtual environment](#2️⃣-create-and-activate-the-virtual-environment)
   - [3️⃣ Install dependencies](#3️⃣-install-dependencies)
   - [4️⃣ Start the Streamlit](#4️⃣-start-the-streamlit)
   - [5️⃣ Run test](#5️⃣-run-test)
9. [🚀 Deployment](#deployment)
10. [🧑‍💻 Collaborators](#-collaborators)

## 🧾 Overview

This document provides a technical overview of the nlp-team2 repository, a machine learning system designed for classifying comments of youtube videos as toxic or not toxic based on NLP (Natural Language Processing) tecnology. The repository implements a complete pipeline from data exploration to model deployment, focusing on ensuring high accuracy and recall for toxic comments detection.

## 🎯 System Purpose and Scope

The nlp-team2 repository serves as a comprehensive mushroom classification system that:

1. Analyzes relationships between youtube comments characteristics and toxici
2. Trains and evaluates multiple classification models
3. Deploys the best-performing model for inference
4. Provides a structured input validation system to ensure reliable predictions
5. Deploys a functional, intuitive API with great analysis capacity.

## 🔍 Main Features

✅ Complete EDA with visualizations to understand variable relationships.

✅ Trained Transformer model to predict whenever a comment is toxic or not

✅ Connecting to the API

✅ Connecting the backend with the frontend

✅ Implement solution using CSS, HTML, and Vanilla JavaScript

✅ Create connection with the database

✅ Dockerized version of the program.

✅ Model in production

## 💡 Possible Improvements

⏩ Analysis of other social networks

⏩ Higher speed in loading results

⏩ Experiments or deployments with neural network models.

## 📁 Folder Structure

```bash
📂 Mushroom-Classifier/

nlp-team2/
├── .github/
│   └── pull_request_template.md
├── .gitignore
├── .qodo/
│   └── testConfig.toml
├── client/
│   ├── .gitignore
│   ├── Dockerfile
│   ├── README.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── public/
│   │   ├── img/
│   │   │   ├── gifgodzilla.gif
│   │   │   ├── icongojira.png
│   │   │   ├── logoFull.png
│   │   │   ├── logoPet.png
│   │   │   └── logofont.png
│   │   ├── index.html
│   │   └── vite.svg
│   ├── src/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── Main.jsx
│   │   ├── assets/
│   │   │   └── react.svg
│   │   ├── components/
│   │   │   ├── AnalyzeTab.jsx
│   │   │   ├── AppMetadata.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── GuideTab.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── HistoryTab.jsx
│   │   │   ├── ProgressLoader.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── ToxicityBadge.jsx
│   │   ├── contexts/
│   │   │   └── ThemeContext.jsx
│   │   ├── hooks/
│   │   │   ├── useApiData.js
│   │   │   └── useAppInfo.js
│   │   ├── index.css
│   │   └── utils/
│   │       └── mockData.js
│   ├── tailwind.config.js
│   ├── tests/
│   │   ├── App.test.jsx
│   │   ├── README.md
│   │   ├── basic-component.test.jsx
│   │   ├── basic.test.js
│   │   ├── components/
│   │   │   ├── Dashboard.test.jsx
│   │   │   ├── Header.test.jsx
│   │   │   ├── Sidebar.test.jsx
│   │   │   └── ThemeContext.test.jsx
│   │   └── setup/
│   │       ├── apiMocks.js
│   │       └── setupTests.js
│   │   └── utils/
│   │       └── mockData.test.js
│   ├── vite.config.js
│   └── vitest.config.js
├── docker-compose.yml
├── eda/
│   └── eda_nlp_(1).ipynb
├── mlFlow/
│   ├── NOTES.md
│   ├── README.md
│   ├── data/
│   │   └── raw/
│   │       ├── hatespeech.csv
│   │       ├── homophobia_human_like_1000.csv
│   │       └── youtoxic_enriched_full.csv
│   ├── enviroment.yml
│   ├── experiments/
│   │   ├── demo_feature_engineering.py
│   │   ├── mlflow_experiments.py
│   │   └── test_transformer_simple.py
│   ├── notebooks/
│   │   ├── eda-nlp.ipynb
│   │   ├── mlflow-experiments.ipynb
│   │   └── model-comparison.ipynb
│   ├── requirements.txt
│   ├── scripts/
│   │   ├── check_experiments.py
│   │   ├── save_current_model.py
│   │   ├── test_backup_model.py
│   │   └── test_model_predictions.py
│   └── src/
│       ├── __init__.py
│       ├── data_preprocessing.py
│       ├── feature_engineering.py
│       ├── model_utils.py
│       └── transformer_models_clean.py
├── requirements.txt
├── server/
│   ├── Dockerfile
│   ├── __main__.py
│   ├── core/
│   │   ├── LOGGING_GUIDE.md
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── print_dev.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_manager.py
│   │   └── models.py
│   ├── main.py
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── toxicity_routes.py
│   │   ├── pipeline.py
│   │   └── predictor.py
│   ├── scraper/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── progress_manager.py
│   │   ├── scrp.py
│   │   └── scrp_socket.py
│   └── tests/
│       ├── README.md
│       ├── conftest.py
│       ├── pytest.ini
│       ├── run_coverage.ps1
│       ├── run_coverage.sh
│       ├── test_database.py
│       ├── test_main.py
│       ├── test_print_dev.py
│       └── test_scrp.py
```

## 🏗️ Architecture Diagram

<div align="center">
  <img src="https://res.cloudinary.com/diowtsfaq/image/upload/v1747050292/Capture_nshpys.png" alt="Descripción de la imagen" width="900" height="450">
</div>

## ⚙️ Installation and Usage

### 1️⃣ Clone the repository

```bash
git clone [https://github.com/Bootcamp-IA-P4/nlp-team2)
cd nlp-team2
```

### 2️⃣ Create and activate the virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/MacOS
.venv\Scripts\activate     # On Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```


### 4️⃣ Run app

```bash
uvicorn server.main:app --reload
```

### 5️⃣ Run test

[Readme Frontend tests](https://github.com/Bootcamp-IA-P4/nlp-team2/blob/dev/client/tests/README.md)

[Readme Backend tests](https://github.com/Bootcamp-IA-P4/nlp-team2/blob/dev/server/tests/README.md)


## 🚀 Deployment

- The model can be tested on render, with the following links:

  [Frontend](https://nlp-client-x3pc.onrender.com/)

  [Backend](https://nlp-server-212396604740.us-east5.run.app/)

## 🧑‍💻 Collaborators

This project was developed by the following contributors:

- [Juan Carlos Macías](https://www.linkedin.com/in/juancarlosmacias/)
- [Fernando García Catalán](https://www.linkedin.com/in/fernandogarciacatalan/)
- [Alejandro Rajado](https://www.linkedin.com/in/alejandro-rajado-martín/)
- [Vada Velázquez](https://www.linkedin.com/in/vadavelazquez/)


