from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    completion = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")

        # Use the OpenAI API to generate a completion using "codex" engine
        response = openai.Completion.create(
            engine="codex",  # Use "codex" engine for code completions
            prompt=prompt,
            max_tokens=300  # Adjust the number of tokens in the completion
        )

        completion = response.choices[0].text.strip()

    return render_template("index.html", prompt=prompt, completion=completion)

if __name__ == "__main__":
    app.run(debug=True)
