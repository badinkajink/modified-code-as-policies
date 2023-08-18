from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key_path = "api_key.txt"

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    completion = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        print(prompt)
        print(type(request.form.get("generate")))
        # Only make the OpenAI API request if the "Generate" button is clicked
        if request.form.get("generate"):
            print("receive generate")
            # Use the OpenAI API to generate a completion using "codex" engine
            # response = openai.Completion.create(
            #     engine="code-davinci-002",  # Use "codex" engine for code completions
            #     prompt=prompt,
            #     max_tokens=300  # Adjust the number of tokens in the completion
            # )
            # completion = response.choices[0].text.strip()
            completion = "generate received"

    return render_template("index.html", prompt=prompt, completion=completion)

@app.route("/generate", methods=["GET", "POST"])
def generate():
    prompt = ""
    completion = ""
    json_data = str(request.get_json())
    prompt = json_data
    response = openai.Completion.create(
        engine="code-davinci-002",  # Use "codex" engine for code completions
        prompt=prompt,
        max_tokens=300  # Adjust the number of tokens in the completion
    )

    completion = response.choices[0].text.strip()
    return render_template("index.html", prompt=prompt, completion=completion)



if __name__ == "__main__":
    app.run(debug=True)
