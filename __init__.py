from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/commits/")
def commits():
    # 1. Récupération
 url = "https://api.github.com/repos/cm2025ma-cmyk/5MCSI_Metriques/commits"
    
    try:
        response = urlopen(url)
        data_json = json.loads(response.read())
        
        commits_par_minute = {}
        
        # 2. Traitement (Ta méthode datetime)
        for commit in data_json:
            date_string = commit['commit']['author']['date']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            
            minute = date_object.minute
            minute_str = str(minute).zfill(2) # Transforme 5 en "05"
            
            if minute_str in commits_par_minute:
                commits_par_minute[minute_str] += 1
            else:
                commits_par_minute[minute_str] = 1

        # 3. Formatage pour Google Charts
        data_for_chart = [['Minute', 'Commits']]
        for minute in sorted(commits_par_minute.keys()):
            data_for_chart.append([minute, commits_par_minute[minute]])
            
    except Exception as e:
        return f"Erreur : {e}"

    # 4. Envoi des données au fichier HTML
    # C'est ici qu'on fait le lien !
    return render_template("commits.html", data=data_for_chart)
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
if __name__ == "__main__":
  app.run(debug=True)
