from flask import Flask, render_template, request, jsonify
from agent import handle_prompt  # uses your existing Gemini function calling setup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    response = handle_prompt(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
