# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return "Flask server is running!"

# # Route for bot info
# @app.route('/bot_info', methods=['POST'])
# def bot_info():
#     data = request.json
#     return jsonify({"message": "Bot info saved", "data": data})

# # Route for customization
# @app.route('/customization', methods=['POST'])
# def customization():
#     data = request.json
#     return jsonify({"message": "Customization saved", "data": data})

# # Route for templates
# @app.route('/templates', methods=['GET'])
# def templates():
#     return jsonify({"message": "Templates retrieved", "templates": []})

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# from transformers import pipeline
# import json

# app = Flask(__name__)

# # Initialize the question-answering pipeline
# qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# # Load the scraped data
# def load_data():
#     with open("aiotrix_data.json", "r") as f:
#         return json.load(f)

# data = load_data()

# @app.route('/')
# def index():
#     return "Flask server is running!"

# @app.route('/answer', methods=['POST'])
# def answer_question():
#     from qa_system import get_relevant_context  # Import function from qa_system

#     question = request.json.get('question', '')
#     context = get_relevant_context(question, data)

#     if not context:
#         return jsonify({"answer": "No relevant context found for the question."}), 400

#     result = qa_pipeline(question=question, context=context)
#     return jsonify({"answer": result['answer']})

# if __name__ == '__main__':
#     app.run(debug=True)




























# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from bs4 import BeautifulSoup
# import requests
# import re
# import json
# from transformers import pipeline

# app = Flask(__name__)
# CORS(app)

# # Initialize the question-answering pipeline
# qa_pipeline = pipeline("question-answering")

# # URLs to scrape
# PAGES = [
#     "",
#     "/about-us",
#     "/services",
#     "/careers",
#     "/contact-us",
#     "/services/artificial-intelligence",
#     "/services/iot-solutions",
#     "/services/data-analysis-and-visualization",
#     "/services/product-development-and-mvp-development",
#     "/services/mobile-application-development",
#     "/services/industry-4-automation",
#     "/blogs/project-ekalavya",
#     "/blogs/flutter-optimization",
#     "/careers/ekalavya/apprenticeship",
#     "/careers/ekalavya/internship",
#     "/careers/ekalavya/seminars",
#     "/terms-and-conditions",
#     "/privacy-policy"
# ]

# def flatten_dict(d):
#     """ Helper function to flatten nested dictionaries into a single string. """
#     flat_str = ""
#     for key, value in d.items():
#         if isinstance(value, dict):
#             flat_str += flatten_dict(value)
#         else:
#             flat_str += f" {value}"
#     return flat_str

# @app.route('/')
# def index():
#     return "Flask server is running!"

# # Route for bot info
# @app.route('/bot_info', methods=['POST'])
# def bot_info():
#     data = request.json
#     return jsonify({"message": "Bot info saved", "data": data})

# # Route for customization
# @app.route('/customization', methods=['POST'])
# def customization():
#     data = request.json
#     return jsonify({"message": "Customization saved", "data": data})

# # Route for templates
# @app.route('/templates', methods=['GET'])
# def templates():
#     return jsonify({"message": "Templates retrieved", "templates": []})

# # Route for scraping website content
# @app.route('/scrape', methods=['GET'])
# def scrape_website():
#     base_url = 'https://www.aiotrix.com'
#     data = {}

#     for page in PAGES:
#         url = base_url + page
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             texts = soup.get_text(separator=" ").strip()
#             data[page] = texts
#         else:
#             return jsonify({"message": f"Failed to retrieve {url}", "status_code": response.status_code}), 500

#     # Save to JSON file
#     with open("aiotrix_data.json", "w") as f:
#         json.dump(data, f, indent=4)

#     return jsonify({"message": "Scraping successful"})

# # Route for question answering
# @app.route('/answer', methods=['POST'])
# def answer_question():
#     data = request.json
#     question = data.get('question', '')

#     # Load the scraped data
#     with open("aiotrix_data.json", "r") as f:
#         scraped_data = json.load(f)

#     # Flatten the scraped data dictionary
#     context = flatten_dict(scraped_data)

#     result = qa_pipeline(question=question, context=context)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)











from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch
import json

app = Flask(__name__)
CORS(app)

# Load data and initialize models
def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

data = load_data('aiotrix_data.json')
qa_pipeline = pipeline('question-answering', model='bert-large-uncased-whole-word-masking-finetuned-squad')
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
questions = [item['question'] for item in data]
question_embeddings = model.encode(questions, convert_to_tensor=True)

@app.route('/')
def index():
    return "Welcome to the AIOTRIX QA System"

@app.route('/answer', methods=['POST'])
def answer():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({"error": "Question cannot be empty"}), 400

    user_question_embedding = model.encode(user_question, convert_to_tensor=True)
    cos_similarities = util.pytorch_cos_sim(user_question_embedding, question_embeddings)
    best_match_idx = torch.argmax(cos_similarities).item()
    best_match_score = cos_similarities[0, best_match_idx].item()

    if best_match_score > 0.5:
        matched_item = data[best_match_idx]
        context = matched_item['context']
        result = qa_pipeline({'context': context, 'question': user_question})
        return jsonify({"answer": result['answer']})
    else:
        return jsonify({"answer": "Sorry, I don't have the context for that question."})

if __name__ == "__main__":
    app.run(debug=True)
