# import json
# import re
# from transformers import pipeline

# def load_data(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)

# def normalize_text(text):
#     return text.lower()

# short_name_mapping = {
#     "kiran": "kiran r. shetty",
#     "aravinth": "aravinth sivasamboo",
#     "asha": "asha aravinth",
#     "karthik": "karthik suvarna",
#     "vikranth": "vikranth salian",
#     "adithi": "adithi n prabhu",
#     "anvitha": "anvitha s",
#     "vikas": "vikas shetty",
#     "likhith": "likhith kumar",
#     "sujan": "sujan n p",
#     "shwetha": "shwetha acharya",
#     "sachin": "sachin a",
#     "mayur": "mayur acharya"
# }

# keywords = {
#     "company_overview": ["company", "overview", "about aiotrix"],
#     "about_us": ["about us", "team", "company history", "location", "mangalore"],
#     "services": ["services", "solutions", "artificial intelligence", "data analysis and visualization", "product development and mvp development", "mobile application development", "industry 4.0 automations"],
#     "project_ekalavya": ["project ekalavya", "ekalavya", "apprenticeship", "internship", "seminars"],
#     "team": ["team", "aravinth sivasamboo", "asha aravinth", "kiran r. shetty", "karthik suvarna", "vikranth salian", "adithi n prabhu", "anvitha s", "vikas shetty", "likhith kumar", "sujan n p", "shwetha acharya", "sachin a", "mayur acharya"],
#     "contact_us": ["contact", "location", "phone", "email"]
# }

# def get_relevant_context(question, data):
#     question = normalize_text(question)
    
#     for short_name, full_name in short_name_mapping.items():
#         if re.search(short_name, question):
#             question = re.sub(short_name, full_name, question)
    
#     combined_context = []

#     for key, terms in keywords.items():
#         for term in terms:
#             if re.search(term, question):
#                 print(f"Matched keyword: {term} in category: {key}")  # Debug statement
#                 if key == "team":
#                     for member in data["team"]["members"]:
#                         if re.search(normalize_text(member["name"]), question):
#                             combined_context.append(f"{member['name']} is {member['role']}")
#                             print(f"Added team member context: {member['name']} is {member['role']}")  # Debug statement
#                 elif key == "services":
#                     services = data["services"]["content"]["services_offered"]
#                     combined_context.append("We provide the following services: " + ', '.join([service['name'] for service in services]))
#                     for service in services:
#                         combined_context.append(f"{service['name']}: {service['description']}")
#                         print(f"Added service context: {service['name']}: {service['description']}")  # Debug statement
#                 elif key == "project_ekalavya":
#                     ekalavya_content = data.get("blogs", {}).get("project-ekalavya", {}).get("content", {})
#                     if ekalavya_content:
#                         combined_context.append(ekalavya_content.get("intro", ""))
#                         combined_context.append(ekalavya_content.get("project_ekalavya", {}).get("description", ""))
#                         combined_context.append(ekalavya_content.get("training_program", {}).get("description", ""))
#                         combined_context.append(ekalavya_content.get("mentorship", {}).get("description", ""))
#                         combined_context.append(ekalavya_content.get("workshops", {}).get("description", ""))
#                         combined_context.append(ekalavya_content.get("leadership", {}).get("description", ""))
#                         combined_context.append(ekalavya_content.get("path_to_success", {}).get("description", ""))
#                         combined_context.append(" ".join([topic["details"] for topic in ekalavya_content.get("topics", [])]))
#                         combined_context.append(ekalavya_content.get("future_innovators", {}).get("description", ""))
#                         combined_context.append(ekalavya_content.get("how_to_apply", {}).get("description", ""))
#                         combined_context.append(" ".join([pathway["description"] for pathway in ekalavya_content.get("pathways", [])]))
#                         combined_context.append(ekalavya_content.get("conclusion", {}).get("description", ""))
#                         print(f"Added Project Ekalavya context: {ekalavya_content}")  # Debug statement
#                     else:
#                         print("No content found for Project Ekalavya")  # Debug statement
#                 else:
#                     content = data.get(key, {}).get("content", {})
#                     if isinstance(content, dict):
#                         combined_context.append(' '.join(content.values()))
#                         print(f"Added dict content for {key}: {' '.join(content.values())}")  # Debug statement
#                     elif isinstance(content, list):
#                         combined_context.extend(content)
#                         print(f"Added list content for {key}: {content}")  # Debug statement
#                     else:
#                         combined_context.append(content)
#                         print(f"Added other content for {key}: {content}")  # Debug statement

#     combined_context_str = ' '.join(filter(None, combined_context)) if combined_context else None
#     print(f"Combined context: {combined_context_str}")  # Debug statement
#     return combined_context_str

# def main():
#     qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
#     data = load_data("aiotrix_data.json")
    
#     while True:
#         question = input("Please enter your question (or 'exit' to quit): ")
#         if question.lower() == 'exit':
#             break

#         context = get_relevant_context(question, data)
#         if not context:
#             if 'services' in question.lower():
#                 # Directly print the services for clarity
#                 services = data["services"]["content"]["services_offered"]
#                 service_list = '\n'.join([service['name'] for service in services])
#                 print(f"Services AIOTRIX provides:\n{service_list}")
#             elif 'project ekalavya' in question.lower() or 'ekalavya' in question.lower():
#                 # Directly print the Project Ekalavya content
#                 ekalavya_content = data.get("blogs", {}).get("project-ekalavya", {}).get("content", {})
#                 if ekalavya_content:
#                     print(f"Project Ekalavya Intro: {ekalavya_content.get('intro', '')}")
#                     print(f"Description: {ekalavya_content.get('project_ekalavya', {}).get('description', '')}")
#                     print(f"Training Program: {ekalavya_content.get('training_program', {}).get('description', '')}")
#                     print(f"Mentorship: {ekalavya_content.get('mentorship', {}).get('description', '')}")
#                     print(f"Workshops: {ekalavya_content.get('workshops', {}).get('description', '')}")
#                     print(f"Leadership: {ekalavya_content.get('leadership', {}).get('description', '')}")
#                     print(f"Path to Success: {ekalavya_content.get('path_to_success', {}).get('description', '')}")
#                     print(f"Topics: {' '.join([topic['details'] for topic in ekalavya_content.get('topics', [])])}")
#                     print(f"Future Innovators: {ekalavya_content.get('future_innovators', {}).get('description', '')}")
#                     print(f"How to Apply: {ekalavya_content.get('how_to_apply', {}).get('description', '')}")
#                     print(f"Pathways: {' '.join([pathway['description'] for pathway in ekalavya_content.get('pathways', [])])}")
#                     print(f"Conclusion: {ekalavya_content.get('conclusion', {}).get('description', '')}")
#                 else:
#                     print("No content found for Project Ekalavya.")
#             else:
#                 print("No relevant context found for the question.")
#             continue

#         try:
#             result = qa_pipeline(question=question, context=context)
#             print(f"Answer: {result['answer']}")
#         except Exception as e:
#             print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()















# import json
# from transformers import pipeline

# def load_data(filepath):
#     """ Load the JSON file containing the questions and context. """
#     with open(filepath, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#     return data

# def main():
#     # Load data from JSON file
#     data = load_data('aiotrix_data.json')

#     # Initialize the Hugging Face pipeline for question answering
#     qa_pipeline = pipeline('question-answering', model='bert-large-uncased-whole-word-masking-finetuned-squad')

#     while True:
#         user_question = input("Please enter your question (or 'exit' to quit): ").strip()
#         if user_question.lower() == 'exit':
#             break

#         matched = False
#         for item in data:
#             context = item['context']
#             question = item['question']
#             if user_question.lower() in question.lower():
#                 # Use the model to get the most relevant context
#                 result = qa_pipeline({'context': context, 'question': user_question})
#                 print(f"Answer: {context}\n")
#                 matched = True
#                 break

#         if not matched:
#             print("Sorry, I don't have the context for that question. Please try another question.\n")

# if __name__ == "__main__":
#     main()





import json
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch

def load_data(filepath):
    """ Load the JSON file containing the questions and context. """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def main():
    # Load data from JSON file
    data = load_data('aiotrix_data.json')

    # Initialize the Hugging Face pipeline for question answering
    qa_pipeline = pipeline('question-answering', model='bert-large-uncased-whole-word-masking-finetuned-squad')

    # Initialize the Sentence Transformer model for embeddings
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Generate embeddings for all questions
    questions = [item['question'] for item in data]
    question_embeddings = model.encode(questions, convert_to_tensor=True)

    while True:
        user_question = input("Please enter your question (or 'exit' to quit): ").strip()
        if user_question.lower() == 'exit':
            break
        if not user_question:
            print("Question cannot be empty. Please try again.")
            continue

        # Generate embedding for the user question
        user_question_embedding = model.encode(user_question, convert_to_tensor=True)

        # Compute cosine similarities
        cos_similarities = util.pytorch_cos_sim(user_question_embedding, question_embeddings)

        # Find the best match
        best_match_idx = torch.argmax(cos_similarities).item()
        best_match_score = cos_similarities[0, best_match_idx].item()

        if best_match_score > 0.5:  # Threshold for considering a match
            matched_item = data[best_match_idx]
            context = matched_item['context']
            question = matched_item['question']
            result = qa_pipeline({'context': context, 'question': user_question})
            print(f"Answer: {result['answer']}\n")
        else:
            print("Sorry, I don't have the context for that question. Please try another question.\n")

if __name__ == "__main__":
    main()
