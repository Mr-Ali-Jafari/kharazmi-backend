import pandas as pd
import numpy as np
import pickle

df = pd.read_csv('questions_and_answers.csv', encoding='utf-8')


print(df.head())


questions = df['question'].values
answers = df['answer'].values

def get_answer(question, questions, answers):
    similarities = [similarity(question, q) for q in questions]
    most_similar_index = np.argmax(similarities)
    return answers[most_similar_index]

def similarity(query, question):
    query_words = set(query.lower().split())
    question_words = set(question.lower().split())
    return len(query_words & question_words) / len(query_words | question_words)



with open('app/qa_model.pkl', 'wb') as f:
    pickle.dump((questions, answers), f)

with open('app/qa_model.pkl', 'rb') as f:
    loaded_questions, loaded_answers = pickle.load(f)


