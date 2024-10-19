from flask import Flask, request, render_template, jsonify
import sqlite3
from recommend import get_recommendations

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = request.form.get('user_id')
    
    try:
        recommendations = get_recommendations(int(user_id))
        return render_template('recommendations.html', courses=recommendations)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)