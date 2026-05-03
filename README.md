# Machine Learning Classification of HCC

A machine learning system for classification of Hepatocellular Carcinoma (HCC), featuring a full-stack web application with backend ML models and a Flask frontend.

## Project Structure

```
machine-learning-classification-of-HCC/
├── code/
│   ├── backend/              # ML models, training notebooks, datasets
│   │   ├── code.ipynb        # Model training notebook
│   │   ├── HCC.csv           # HCC dataset
│   │   ├── xdata.csv         # Feature data
│   │   ├── ydata.csv         # Target data
│   │   ├── decision.joblib   # Decision Tree model
│   │   ├── random_forest.joblib
│   │   └── ...               # Additional trained models
│   ├── frontend/             # Flask web application
│   │   ├── app.py            # Main Flask app
│   │   ├── templates/        # HTML templates
│   │   ├── static/           # CSS, JS, images
│   │   └── Models/           # Models served by frontend
│   └── partial-code/         # Alternate/partial implementation
│       └── backend/          # Partial backend code
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

- Multi-model ML classification (Decision Tree, Random Forest, Stacking)
- Flask web application with prediction interface
- Data profiling and visualization
- Model comparison and ROC/AUC analysis

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python code/frontend/app.py
```

## Tech Stack

- Python, Scikit-learn
- Flask
- Pandas, NumPy
- Matplotlib / Seaborn
