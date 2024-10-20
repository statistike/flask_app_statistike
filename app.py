from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

API_KEY = '97c2298dc142bd4354d0cf7e83b72bc57ae98cc3fa7a534176f1c3b8aec723ef'  # Tvoj SerpAPI ključ
SEARCH_ENDPOINT = 'https://serpapi.com/search'

# Predefinisani odgovori za jednostavna pitanja
simple_responses = {
    "kako si": [
        "Odlično, hvala na pitanju!",
        "Osećam se sjajno, a ti?",
        "Danas sam raspoložen da pričam s tobom!",
        "Super sam, nadam se da si i ti!",
        "Pomalo umoran, ali spreman da ti pomognem!",
        "Uvek sam tu za razgovor!",
        "Osećam se motivisano danas!",
        "Dobro sam, hvala što si pitao!",
        "Srećan sam što mogu da pomažem!",
        "Danas sam pun energije!"
    ],
    "šta radiš": [
        "Pomažem ti s tvojim pitanjima!",
        "Razmišljam o načinima kako ti mogu pomoći.",
        "Upravo sada se fokusiram na tvoje pitanje.",
        "Razmišljam o odgovorima!",
        "Čekam tvoja sledeća pitanja!",
        "Pripremam se da ti dam najbolje odgovore."
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question'].lower()  # Pitanje pretvaramo u mala slova
    response = ""
    sources = []

    # Prepoznavanje jednostavnih pitanja i generisanje odgovora
    for key in simple_responses:
        if key in question:
            response = random.choice(simple_responses[key])  # Nasumično bira odgovor
            return render_template('index.html', response=response, sources=sources)

    # Ako nije prepoznato jednostavno pitanje, pretražujemo internet koristeći SerpAPI
    params = {
        'q': question,
        'api_key': API_KEY,
        'hl': 'en',  # Jezik
        'gl': 'us',  # Geolokacija
    }
    
    search_response = requests.get(SEARCH_ENDPOINT, params=params)

    if search_response.status_code == 200:
        search_results = search_response.json()
        if 'organic_results' in search_results and search_results['organic_results']:
            first_result = search_results['organic_results'][0]
            response = first_result.get('snippet', 'Nema dostupnih informacija.')
            sources.append(first_result.get('link', ''))
        else:
            response = "Nažalost, nisam mogao da pronađem informacije."
    else:
        response = "Došlo je do greške prilikom pretrage."

    return render_template('index.html', response=response, sources=sources)

if __name__ == '__main__':
    app.run(debug=True)
