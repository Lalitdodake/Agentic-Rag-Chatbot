import  json
from datasets import Dataset
from models import *

from vector_db_handler import  VectorDBHandler

vectordb_handler = VectorDBHandler()
retriever = vectordb_handler.get_retriever()



with open("ragas_qa_dataset.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# Convert to HuggingFace Dataset
dataset = Dataset.from_list(qa_data)

print(dataset)


def build_ragas_dataset(dataset):
    questions = []
    answers = []
    contexts = []
    ground_truths = []

    for row in dataset:
        question = row["question"]
        ground_truth = row["answer"]

        retrieved_docs = retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])


        print("Retrieved Docs----", retrieved_docs)
        print("Retrieved context----", context)
        prompt = f"""
        Go through the context and answer given question strictly based on context. 
        Context: {context}
        Question: {question}
        Answer:
        """

        llm_answer = llm_model.invoke(prompt).content

        questions.append(question)
        answers.append(llm_answer)
        contexts.append(context)
        ground_truths.append(ground_truth)

    return Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })

ragas_dataset = build_ragas_dataset(dataset)

ragas_data_list = ragas_dataset.to_list()


with open("ragas_evaluation_dataset_final.json", "w", encoding="utf-8") as f:
    json.dump(ragas_data_list, f, indent=2, ensure_ascii=False)



