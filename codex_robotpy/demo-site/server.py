from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key_path = "openai_api_key.txt"
generate_clicked = False
prompt = "# Enter your prompt here or upload a file"
completion = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global prompt
    global completion 

    return render_template("index.html", prompt=prompt, completion=completion)

@app.route("/generate", methods=["POST"])
def generate():
    global prompt
    global completion 
    json_data = str((request.get_json()))
    print(json_data)
    prompt = request.form.get("prompt")
    print(prompt)
    # Use the OpenAI API to generate a completion using "codex" engine
    # response = openai.Completion.create(
    #     engine="code-davinci-002",  # Use "codex" engine for code completions
    #     prompt=prompt,
    #     temperature=1.0,
    #     max_tokens=256  # Adjust the number of tokens in the completion
    # )
    # completion = response.choices[0].text.strip()
    completion="asdfasdf"
    return jsonify({"completion": completion})


if __name__ == "__main__":
    app.run(debug=True)
