from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# 1. Import the LangChain OpenAI models and Ragas wrappers
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

def evaluate_rag(questions: list, answers: list, contexts: list, ground_truths: list):
    """Run Ragas evaluation on the provided QA lists."""
    # 2. Initialize and wrap the models
    llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
    embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

    eval_dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })

    # 3. Explicitly pass llm and embeddings into evaluate
    results = evaluate(
        eval_dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
        llm=llm,
        embeddings=embeddings
    )

    return results
