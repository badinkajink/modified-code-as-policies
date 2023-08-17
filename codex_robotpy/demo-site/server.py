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

        # Use the OpenAI API to generate a completion
        response = openai.Completion.create(
            engine="davinci",  # Use "davinci" engine for text completions
            prompt=prompt,
            max_tokens=50  # Adjust the number of tokens in the completion
        )

        completion = response.choices[0].text.strip()

    return render_template("index.html", prompt=prompt, completion=completion)

if __name__ == "__main__":
    app.run(debug=True)
