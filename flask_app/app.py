from flask import Flask, render_template, request, jsonify 
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('log_prob.html')


@app.route('/solve', methods=['POST'])
def solve():
    user_data = request.json
    hts, ats, hos, hwpg, awpg = user_data['hts'], user_data['ats'], user_data['hos'], user_data['hwpg'], user_data['awpg']
    proba = _solve_prob(hts, ats, hos, hwpg, awpg)
    return jsonify({'proba':proba})

def _solve_prob(hts, ats, hos, hwpg, awpg):
    model = pickle.load(open('log_model.sav','rb'))
    X_new = np.array([[hts, ats, hos, hwpg, awpg]])
    prob = model.predict_proba(X_new)[:,1][0]
    prob = round(prob*100, 1)
    prob = f'{prob}%'
    return prob

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)



