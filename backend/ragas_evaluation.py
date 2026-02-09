import json
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall, context_entity_recall, answer_correctness
import os
os.environ["RAGAS_DISABLE_VERTEXAI"] = "true"

with open("ragas_evaluation_dataset_final.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

dataset = Dataset.from_list(qa_data)
from models import *

print(dataset)
score = evaluate(dataset,metrics=[faithfulness,
                                  answer_relevancy,
                                  context_precision,
                                  context_recall,
                                  context_entity_recall,
                                  answer_correctness],
                 llm= llm_model, embeddings = embedding_model)
print(score)