import os
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv

load_dotenv()

def run_evaluation():
    print("Running Evaluation Pipeline...")
    
    # 1. Define Golden Dataset
    dataset = [
        {
            "input": "What is RAGScope?",
            "actual_output": "RAGScope is a production-grade RAG platform.",
            "expected_output": "RAGScope is a production-grade RAG platform.",
            "retrieval_context": ["RAGScope is a production-grade RAG platform with telemetry."]
        },
        {
            "input": "Does RAGScope support telemetry?",
            "actual_output": "Yes, it logs every request into PostgreSQL.",
            "expected_output": "Yes, it logs telemetry.",
            "retrieval_context": ["RAGScope logs telemetry into PostgreSQL database."]
        }
    ]

    test_cases = []
    for data in dataset:
        test_case = LLMTestCase(
            input=data["input"],
            actual_output=data["actual_output"],
            expected_output=data["expected_output"],
            retrieval_context=data["retrieval_context"]
        )
        test_cases.append(test_case)

    # 2. Define Metrics
    answer_relevancy = AnswerRelevancyMetric(threshold=0.5)
    faithfulness = FaithfulnessMetric(threshold=0.5)

    # 3. Evaluate
    results = evaluate(test_cases, [answer_relevancy, faithfulness])
    
    print("Evaluation Complete. Results:")
    print(results)

if __name__ == "__main__":
    run_evaluation()
