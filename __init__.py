from flask import Flask, render_template, jsonify
from urllib.request import Request, urlopen
from datetime import datetime
import json

app = Flask(__name__)

# -----------------------------
# Page d'accueil
# -----------------------------
@app.route('/')
def hello_world():
    return render_template('hello.html')

# -----------------------------
# Exercice 5 : /contact/
# -----------------------------
@app.route("/contact/")
def contact():
    return render_template("contact.html")

# -----------------------------
# Exercice 3 : /tawarano/
# -----------------------------
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
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({
            'Jour': dt_value,
            'temp': temp_day_value
        })

    return jsonify(results=results)

# -----------------------------
# Exercice 3 bis / 3 ter : graphique ligne
# -----------------------------
@app.route("/rapport/")
def rapport():
    return render_template("graphique.html")

# -----------------------------
# Exercice 4 : histogramme
# -----------------------------
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

# -----------------------------
# Exercice 6 : page commits
# -----------------------------
@app.route("/commits/")
def commits():
    return render_template("commits.html")

# API données commits GitHub
@app.route("/commits-data/")
def commits_data():
    GITHUB_USERNAME = "tedmlkskywalker"
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/5MCSI_Metriques/commits"

    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(req)
    raw = response.read()
    commits_json = json.loads(raw.decode("utf-8"))

    minute_counts = {m: 0 for m in range(60)}

    for c in commits_json:
        date_str = c.get("commit", {}).get("author", {}).get("date")
        if not date_str:
            continue
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        minute_counts[dt.minute] += 1

    results = [{"minute": m, "count": minute_counts[m]} for m in range(60)]
    return jsonify(results=results)

# -----------------------------
# Lancement
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
