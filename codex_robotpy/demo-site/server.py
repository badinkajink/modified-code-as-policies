from flask import Flask, render_template, request, jsonify
import openai
import os
import simulated_romi_prompt as srp
app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key_path = "openai_api_key.txt"
generate_clicked = False
prompt = "# Enter a prompt or upload a file"
completion = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global prompt
    global completion 
    return render_template("index.html", prompt=prompt, completion=completion)

@app.route("/generate", methods=["POST"])
def generate():
    prompt = str(request.get_json())
    # Use the OpenAI API to generate a completion using "codex" engine
    response = openai.Completion.create(
        engine="code-davinci-002",  # Use "codex" engine for code completions
        prompt=srp.prompt + prompt,
        temperature=1.0,
        max_tokens=200  # Adjust the number of tokens in the completion
    )
    completion = response.choices[0].text.strip()
    return jsonify({"completion": completion})


if __name__ == "__main__":
    app.run(debug=True)
