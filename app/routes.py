import pickle

import statsmodels.api as sm  # type: ignore
from flask import Flask, jsonify, redirect, render_template, request, url_for

#from app.model import predict

# Initialiser l'application Flask
app = Flask(__name__)
# Charger le modèle sauvegardé
with open('app/saved_model/seismic_model.pkl', 'rb') as f:
    model = pickle.load(f)
    
const=1
# Route d'accueil
@app.route('/')
def index():
    return render_template('web/index.html')

@app.route('/commencer')
def commencer():
    return render_template('web/sign-up.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données du formulaire
        depth = float(request.form['depth'])
        significance = float(request.form['significance'])
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])

        # Créer un tableau avec les valeurs d'entrée
        data_input = [[const,significance, depth, latitude, longitude]]
        
        # Ajouter la constante (1) aux données d'entrée
        # data_input_with_const = sm.add_constant(data_input)

        # Faire une prédiction
        prediction = model.predict(data_input)[0]

        # Rediriger vers la page des résultats avec la prédiction
        return redirect(url_for('result', prediction=prediction))

    except Exception as e:
        return f"Erreur : {e}"

@app.route('/result')
def result():
    prediction = float(request.args.get('prediction'))
    return render_template('web/article-details.html', prediction=prediction)  # Page des résultats