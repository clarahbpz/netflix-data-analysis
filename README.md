# 🎬 Netflix Content Analysis Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://netflix-data-analysis-49oyrd3m2wsfdpaqjec3th.streamlit.app/)

An end-to-end data analysis project featuring an interactive web dashboard and a comprehensive Exploratory Data Analysis (EDA) notebook. Built to explore, filter, and visualize trends within the Netflix catalog of movies and TV shows.

## 🚀 Overview

This project transforms raw dataset rows into actionable visual insights. It is divided into two main components:
1. **Exploratory Data Analysis (EDA):** A documented Jupyter Notebook detailing the data cleaning and preliminary visualization process.
2. **Interactive Dashboard:** A deployed Streamlit application that allows users to dynamically query the data through an intuitive UI.

## 📊 Key Features

- **Interactive Visualizations:** Built with Plotly to allow hover-over details, zooming, and dynamic scaling.
- **Smart Filtering System:** Multi-select options for content type, country of production, and genres.
- **Dynamic Search Engine:** Session-state managed text search for specific titles.
- **KPI Tracking:** Real-time metrics updating based on the applied filters.
- **Word Cloud Generation:** Text analysis of the most frequent words in titles.

## 🛠️ Technologies & Tools

- **Language:** Python
- **Data Manipulation:** Pandas
- **Web Framework:** Streamlit
- **Data Visualization:** Plotly Express, Matplotlib, Seaborn (for EDA)
- **Text Analysis:** WordCloud
- **Environment:** Jupyter Notebook

## 📁 Project Structure

netflix-data-analysis/
│
├── analysis/.ipynb      
├── data/

│   └── netflix_titles.csv     
├── app.py                     
├── requirements.txt           
├── .gitignore
└── README.md

## ▶️ How to Run Locally

#### Clone the repository:

bash git clone [https://github.com/clarahbpz/netflix-data-analysis.git](https://github.com/clarahbpz/netflix-data-analysis.git)

#### Navigate to the project directory:

cd netflix-data-analysis

#### Install the required dependencies:

pip install -r requirements.txt

#### Launch the Streamlit application:

streamlit run app.py

## 🎯 Project Purpose

This project was developed as a portfolio piece to demonstrate a complete data workflow. It applies engineering principles to data extraction, cleaning, and visualization, culminating in the deployment of a user-friendly, production-ready web application.

## 📌 Future Improvements

Integrate the TMDb API to fetch real-time ratings and poster images.

Develop a Machine Learning-based recommendation engine for similar titles.

Expand the dataset to compare Netflix trends with other streaming platforms (e.g., Amazon Prime, Disney+).

Author: Clara Hilbert Polizel

