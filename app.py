#APP FLASK (commande : flask run)
# Partie formulaire non utilisée (uniquement appel à l'API)

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_wtf import Form 
#from flask_wtf import validators 

#from wtforms.fields import TextField, BooleanField
#from wtforms.validators import Required

from wtforms.fields import StringField
from wtforms import BooleanField, PasswordField, TextAreaField, validators,TextField
from wtforms.widgets import TextArea
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_wtf import FlaskForm
#from toolbox.predict import 
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
fic_best_model = 'best_model.pickle'
with open(fic_best_model, 'rb') as df_best_model:
    model = pickle.load(df_best_model)
#formulaire d'appel à l'API (facultatif)
class SimpleForm(FlaskForm):
    form_id = TextField('id:', validators=[validators.required()])
    
    @app.route("/", methods=['GET', 'POST'])
    def home():
        Message="Bienvenue sur l'API de prédiction de scoring: entrez '/' suivi du numéro de client pour voir les prédictions"
        return Message


    @app.route("/predict/<id_client>", methods=['GET', 'POST'])    
    def form():
        form = SimpleForm(request.form)
        print(form.errors)

        if request.method == 'POST':
            form_id=request.form['id']
            print(form_id)
            return(redirect('predict/'+form_id)) 
    
        if form.validate():
            # Save the comment here.
            flash('Vous avez demandé l\'ID : ' + form_id)
            redirect('')
        else:
            flash('Veuillez compléter le champ. ')
    
        return render_template('formulaire_id.html', form=form)



@app.route('/<id_client>', methods=['GET', 'POST'])
def credit(id_client):
    print("dataframe")
    FILE_TEST_SET = 'test_set.pickle'
    with open(FILE_TEST_SET, 'rb') as df_test_set:
        dataframe = pickle.load(df_test_set)
       


    try:
        prediction, proba = predict_flask(id_client, dataframe)
        dict_final = {
        'Vous avez demandé le client:' :int(id_client),
        'prédiction' : int(prediction),
        'probabilité' : float(proba[0][0])
        }       
    except ValueError:

        dict_final = {
        'Vous avez demandé le client:' :int(id_client),
        'prédiction' : '-',
        'probabilité' : '-'
        }
        Message="Ce client n'existe pas dans la BD, merci d'en choisir un autre"
        return Message

    return jsonify(dict_final)


def predict_flask(ID, dataframe):
    '''Fonction de prédiction utilisée par l\'API flask :
    a partir de l'identifiant et du jeu de données
    renvoie la prédiction à partir du modèle'''
    print(dataframe)
    ID = int(ID)
    X = dataframe[dataframe['SK_ID_CURR'] == ID]
    X = X.drop(['SK_ID_CURR'], axis=1)
    proba = model.predict_proba(X)
    print(proba)
    print(proba[0])
    print(proba[0][0])
    if proba[0][0] > 0.5:
        return 0, proba
    else:
        return 1, proba


    return predictio, proba

#lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)