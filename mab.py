import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import beta
from sentence_transformers import SentenceTransformer

import streamlit as st
import openai
import os
import json
import time
from load_dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("METAREASONER_OPENAI_API_KEY"))  # Initialize the OpenAI client

def make_api_call(messages, max_tokens=200, is_final_answer=False):
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-3.5 Turbo, adjust as needed
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                if is_final_answer:
                    print(f"Failed to generate final answer after 3 attempts. Error: {str(e)}")
                    return {"title": "Error",
                            "content": f"Failed to generate final answer after 3 attempts. Error: {str(e)}"}
                else:
                    print(f"Failed to generate step after 3 attempts. Error: {str(e)}")
                    return {"title": "Error", "content": f"Failed to generate step after 3 attempts. Error: {str(e)}",
                            "next_action": "final_answer"}
            time.sleep(1)  # Wait for 1 second before retrying

class DynamicMultiArmedBandit:
    def __init__(self, similarity_threshold=0.8):
        self.strategy_stats = {}  # Maps strategy hash to (successes, failures)
        self.similarity_threshold = similarity_threshold
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # For strategy embeddings

    def add_strategy(self, strategy):
        """Add a new strategy dynamically."""
        embedding = self.model.encode(strategy).reshape(1, -1)
        for existing_strategy, (emb, stats) in self.strategy_stats.items():
            if cosine_similarity(embedding, emb)[0][0] > self.similarity_threshold:
                return existing_strategy  # Return existing similar strategy
        strategy_id = len(self.strategy_stats)
        self.strategy_stats[strategy_id] = (embedding, [0, 0])  # (embedding, [successes, failures])
        return strategy_id

    def select_strategy(self):
        """Select a strategy using Thompson Sampling."""
        best_score = -1
        best_strategy = None
        for strategy_id, (_, stats) in self.strategy_stats.items():
            successes, failures = stats
            sample = beta(successes + 1, failures + 1).rvs()
            if sample > best_score:
                best_score = sample
                best_strategy = strategy_id
        return best_strategy

    def update(self, strategy_id, reward):
        """Update reward statistics for the chosen strategy."""
        _, stats = self.strategy_stats[strategy_id]
        if reward > 0:
            stats[0] += 1  # Increment successes
        else:
            stats[1] += 1  # Increment failures

def llm_generate_strategy(history, task):
    """Placeholder for LLM generating strategies."""
    # Replace with actual LLM calls
    prompt = """
I have some known conditions:
{Known_conditions}
And my objective is:
{Objective}
Rethink the requirement of the objective and reflect on the known conditions, then provide guidance for further steps.

The reflection should include the following aspects:
1. progress: Has the AI made sufficient progress towards solving the objective?
2. strategy: What is the current strategy for the conditions we have? Is the current approach effective for the given task?
3. accuracy: Are there any mistakes or misconceptions in the intermediate steps?
4. efficiency: Is the AI taking unnecessary detours or repeating steps?

Based on your analysis, provide guidance for further steps. Consider the following strategies:
1. If progress is insufficient or the strategy seems ineffective, recommend starting again from the beginning with a change of approach.
2. If there are mistakes in intermediate steps, suggest backtracking to the point where the error occurred.
3. If the current approach is working well, encourage the AI to continue and provide specific suggestions for the next steps.
4. If the AI seems stuck, propose alternative methods or perspectives to consider.

NOTE:
1. You are only allowed to provide one guidance from the above four strategies based on the known conditions and objective.
2. Your reflection should be concise and focused on the key aspects of progress, strategy, accuracy, and efficiency. Do not provide a detailed analysis of each step.
"""
    messages = [{"role": "system", "content": prompt.format(Known_conditions=history, Objective=task)}]
    new_strategies = make_api_call(messages)
    return new_strategies

def evaluate_strategy(strategy):
    """Simulate evaluation of a strategy."""
    prompt = f"""
Based on the given conditions and objective, evaluate the effectiveness of the following strategy:
{strategy},
only give a score of 1 if the strategy is effective, otherwise give a score of 0. Only return "1" or "0".
"""
    messages = [{"role": "system", "content": prompt}]
    response = make_api_call(messages)
    if response == "1":
        return 1
    else:
        return 0


def llm_generate_actions(task):
    """Placeholder for LLM generating actions."""
    # Replace with actual LLM calls
    prompt = f"""
Given the following task:
{task}
Provide a sequence of actions to solve the task. Each action should be a step towards achieving the objective. Consider the following aspects:
1. Use the provided numbers and operations to reach the target value.
2. Ensure that each number is used exactly once.
3. Provide a clear and concise explanation for each step.
"""
    messages = [{"role": "system", "content": prompt}]
    actions = make_api_call(messages)
    return actions


# Main Loop
bandit = DynamicMultiArmedBandit()
task = "Solve the game of 24 (use all 4 provided numbers exactly once each and +-/* to make 24) for [9 8 8 3]"

for _ in range(5):  # Number of iterations
    history = llm_generate_actions(task)
    new_strategy = llm_generate_strategy(history, task)
    print(f"Generated Strategy: {new_strategy}")
    strategy_id = bandit.add_strategy(new_strategy)
    chosen_strategy_id = bandit.select_strategy()
    reward = evaluate_strategy(new_strategy)
    bandit.update(chosen_strategy_id, reward)

# Output results
for strategy_id, (_, stats) in bandit.strategy_stats.items():
    print(f"Strategy {strategy_id} - Successes: {stats[0]}, Failures: {stats[1]}")
