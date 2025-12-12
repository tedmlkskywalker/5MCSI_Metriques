from flask import Flask, render_template, jsonify
from datetime import datetime
from urllib.request import urlopen
import json

app = Flask(__name__)

# --------------------------------------------------
# Page d'accueil (Exercice 1)
# --------------------------------------------------
@app.route('/')
def hello_world():
    return render_template('hello.html')


# --------------------------------------------------
# Exercice 2 : Route /contact/
# --------------------------------------------------
@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"


# --------------------------------------------------
# Exercice 3 : API météo /tawarano/
# --------------------------------------------------
@app.route('/tawarano/')
def meteo():
    response = urlopen(
        'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx'
    )
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin → °C
        results.append({
            'Jour': dt_value,
            'temp': round(temp_day_value, 2)
        })

    return jsonify(results=results)


# --------------------------------------------------
# Exercice 3 bis : Page HTML graphique
# --------------------------------------------------
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


# --------------------------------------------------
# (OPTIONNEL – utile pour Exercice 6 plus tard)
# Extraction des minutes depuis une date ISO
# --------------------------------------------------
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


# --------------------------------------------------
# Lancement de l'application
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
