from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# File di dati
PLAYERS_FILE = 'players.json'
MATCHES_FILE = 'matches.json'

# Carica i dati dei giocatori
def load_players():
    with open(PLAYERS_FILE, 'r') as f:
        return json.load(f)

# Salva i dati dei giocatori
def save_players(players):
    with open(PLAYERS_FILE, 'w') as f:
        json.dump(players, f)

# Carica le partite
def load_matches():
    with open(MATCHES_FILE, 'r') as f:
        return json.load(f)

# Salva le partite
def save_matches(matches):
    with open(MATCHES_FILE, 'w') as f:
        json.dump(matches, f)

# Funzione per calcolare il nuovo rating ELO
def calculate_elo(player1, player2, score1, score2):
    k = 32
    r1 = 10 ** (player1['rating'] / 400)
    r2 = 10 ** (player2['rating'] / 400)
    
    e1 = r1 / (r1 + r2)
    e2 = r2 / (r1 + r2)
    
    if score1 > score2:
        s1, s2 = 1, 0
    else:
        s1, s2 = 0, 1
    
    player1['rating'] = player1['rating'] + k * (s1 - e1)
    player2['rating'] = player2['rating'] + k * (s2 - e2)

@app.route('/')
def index():
    players = load_players()
    return render_template('index.html', players=players)

@app.route('/submit_match', methods=['POST'])
def submit_match():
    player1_name = request.form['player1']
    player2_name = request.form['player2']
    score1 = int(request.form['score1'])
    score2 = int(request.form['score2'])
    
    players = load_players()
    matches = load_matches()
    
    player1 = next(player for player in players if player['name'] == player1_name)
    player2 = next(player for player in players if player['name'] == player2_name)
    
    calculate_elo(player1, player2, score1, score2)
    
    save_players(players)
    
    matches.append({
        'player1': player1_name,
        'player2': player2_name,
        'score1': score1,
        'score2': score2
    })
    save_matches(matches)
    
    return redirect(url_for('index'))

@app.route('/history')
def history():
    matches = load_matches()
    return render_template('history.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
