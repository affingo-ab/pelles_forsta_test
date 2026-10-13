from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'hemlig-nyckel-for-pelle'

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data.json')

def load_data():
    if not os.path.exists(DATA_PATH):
        return {"items": []}
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'Pelle' and password == 'Pelle123!':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Felaktigt användarnamn eller lösenord!'
            
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    data = load_data()
    return render_template('dashboard.html', data=data['items'])

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    data = load_data()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form.get('name')
            value = request.form.get('value')
            if name and value:
                try:
                    data['items'].append({"name": name, "value": float(value)})
                    save_data(data)
                except ValueError:
                    pass
                    
        elif action == 'delete':
            index = int(request.form.get('index'))
            if 0 <= index < len(data['items']):
                data['items'].pop(index)
                save_data(data)
                
        elif action == 'update':
            index = int(request.form.get('index'))
            name = request.form.get('name')
            value = request.form.get('value')
            if 0 <= index < len(data['items']) and name and value:
                try:
                    data['items'][index] = {"name": name, "value": float(value)}
                    save_data(data)
                except ValueError:
                    pass
                    
        return redirect(url_for('manage'))
        
    return render_template('manage.html', data=data['items'])

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
