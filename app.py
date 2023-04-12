from flask import Flask, request, jsonify
import openai
import os
from personal_data import chatgpt_api_key

openai.api_key = chatgpt_api_key

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_code():
    prompt = request.json.get('prompt', '')

    #prompt = f"Convert this Java code to Python:\n\n{java_code}\n"

    response = openai.Completion.create(
        engine="text-davinci-codex-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n\n"]
    )

    python_code = response.choices[0].text.strip()
    return jsonify(pythonCode=python_code)

if __name__ == '__main__':
    app.run(debug=True)