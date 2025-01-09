import openai
from flask import Flask, render_template, request

app = Flask(__name__)

# Your OpenAI API key (replace with your actual key)
openai.api_key = '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'

# Temporary storage for cases
cases = []

@app.route('/')
def home():
    return "Welcome to Lawyer Assistant!"

@app.route('/submit_case', methods=['GET', 'POST'])
def submit_case():
    if request.method == 'POST':
        case_name = request.form['case_name']
        client_name = request.form['client_name']
        case_type = request.form['case_type']
        description = request.form['description']
        date_filed = request.form['date_filed']

        # Store the case in the cases list
        cases.append({
            'case_name': case_name,
            'client_name': client_name,
            'case_type': case_type,
            'description': description,
            'date_filed': date_filed
        })

        # Get GPT insights
        legal_insights = get_legal_insights(description)

        # Show all submitted cases with insights
        return render_template('case_list.html', cases=cases, insights=legal_insights)

    return render_template('upload.html')


def get_legal_insights(description):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a legal assistant with expertise in various areas of law, capable of offering detailed and specialized insights for lawyers."},
                {"role": "user", "content": f"Given the following case description, provide the following insights:\n1. Legal stands or defenses the lawyer might take.\n2. Key evidence that might be required.\n3. Relevant legal terms or sections that may be applicable.\n4. Similar older cases for reference.\n\nCase Description: {description}"}
            ],
            max_tokens=1000
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error in GPT integration: {str(e)}"




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

