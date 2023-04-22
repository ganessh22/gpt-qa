import sys

# The line `# import openai` is a comment and does not actually import the `openai` module. It is
# likely that this line was commented out because the `openai` module is not being used in the code.
import openai
from flask import Flask, render_template_string, request

app = Flask(__name__)

API_KEY = sys.argv[1]
fine_tune_model_path = sys.argv[2]
with open(fine_tune_model_path, "r") as f:
    FINE_TUNED_MODEL = f.readline().strip()
openai.api_key = API_KEY


def openai_response(prompt: str) -> str:
    return openai.Completion.create(
        model=FINE_TUNED_MODEL,
        prompt=prompt
    ).choices[0].text.strip()


@app.route('/', methods=['GET', 'POST'])
def index():
    prompt = ''
    response = "awaiting input"
    if request.method == 'POST':
        prompt = request.form['text_input']
        response = openai_response(prompt)
    return render_template_string('''
        <html>
        <head>
            <style>
                html, body {
                    height: 100%;
                    margin: 0;
                }

                .container {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100%;
                    font-family: Arial, sans-serif;
                }

                h1 {
                    font-family: 'Comic Sans MS', cursive, sans-serif;
                    font-size: 2.5em;
                    font-weight: bold;
                    margin-bottom: 30px;
                }

                form {
                    display: inline-block;
                }

                label {
                    font-size: 1.2em;
                }

                input[type="text"] {
                    font-size: 1em;
                    padding: 5px;
                }

                input[type="submit"] {
                    font-size: 1em;
                    padding: 5px;
                    margin-left: 10px;
                }

                .response {
                    font-size: 1.2em;
                    margin-top: 30px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Question Answerer GPT</h1>
                <form method="POST">
                    <label for="text_input">Enter text:</label>
                    <input type="text" id="text_input" name="text_input">
                    <input type="submit" value="Submit">
                </form>
                <br>
                <div class="response">Response: {{ response }}</div>
            </div>
        </body>
        </html>
    ''', response=response)


if __name__ == '__main__':
    app.run()