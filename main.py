import os
import re
import json
import random
from prompt.prompts import *
from collections import Counter
from macm.executor import Execute_steps
from macm.judge import Judge_statement, Judge_answer, Judge_condition
from macm.thinker import Analysis_conditions, Think_thoughts, Think_Steps, Meta_reasoner

def check_condition(question,condition, n):
    """
    Use several Judges to check the statement
    Input:
    conditions, unchecked_conditions, the number of the inspectors (List, Str, int)
    Output:
    True/False (bool)
    """
    for _ in range(n):
        if Judge_condition(question,condition).strip() == "False":
            return False
    return True

def check_statement(conditions,unchecked_condition, n):
    """
    Use several Judges to check the new condition
    Input:
    conditions, unchecked_conditions, the number of the inspectors (List, Str, int)
    Output:
    True/False (bool)
    """
    for _ in range(n):
        answer = Judge_statement(conditions,unchecked_condition)
        if  "False" in answer or "false" in answer:
            return False
    return True

def check_answer(conditions,objectives):
    """
    Use several Judges to check the answer
    Input:
    unchecked_conditions, the number of the inspectors (Str, int)
    Output:
    True/False (bool)
    """
    if_got_answer = Judge_answer(conditions,objectives)
    if "False" in if_got_answer or "false" in if_got_answer:
        return False
    return True

def check_if_got_answer(conditions,objectives,n):
    for _ in range(n):
        if check_answer(conditions,objectives) == False:
            return False
    return True    

def main(question, times, n, min_voters, max_voters):
    """
    Input question and get the final answer from muti-Agent got
    Input:
    quesion, the number of times new conditions are identified, the number of the inspectors  (Str, int, int)
    Output:
    final answer (Str)
    """
    possible_answers = []
    use_meta_reasoner = True
    try:
        voter_count = 0
        tie = True
        
        # Vote
        while tie or voter_count < min_voters:
            voter_count += 1
            print(f"\n{voter_count} Thinker is analyzing the question...")
            conditions,objectives = Analysis_conditions(question)
            print("\n# conditions:", conditions)
            print("\n# objectives:", objectives)
            Initial_condition_numbers = len(conditions) # This line will be used for the $while$ mode
            feedbacks = []
            # Think thoughts
            # while len(conditions) - Initial_condition_numbers <= times: 
            for time in range(times): # Try to reduce the LLM queries.
                if use_meta_reasoner:
                    print(f"\n{voter_count} Meta-reasoner is providing the guidance...")
                    feedbacks = Meta_reasoner(conditions,objectives,question)
                    print("  \n# feedbacks:", feedbacks)
                
                print(f"\n# {voter_count} Thinker is thinking new thoughts...")
                unchecked_conditions = Think_thoughts(conditions,objectives,feedbacks)
                print("  \n# conditions before judge:", unchecked_conditions)
                checked_conditions = []
                
                for unchecked_condition in unchecked_conditions:
                    print(f"\n{voter_count} Judge is checking conditions...")
                    if check_statement(conditions,unchecked_condition,n):
                        start = unchecked_condition.find("we can get: ")
                        if start != -1:
                            unchecked_condition = unchecked_condition[start + len("we can get: "):]
                        checked_conditions.append(unchecked_condition)
                conditions = conditions + checked_conditions
                print("  \n# conditions after judge:", conditions)
                if_got_answer = check_if_got_answer(conditions,objectives,1)
                if if_got_answer:
                    print("  \n# The answer is found.")
                    break
            print(f"\n{voter_count} thinker is thinking steps...")
            steps = Think_Steps(conditions,objectives)
            print("  \n# steps:", steps)
            
            print(f"\n{voter_count} Executor is trying to calculate the answer...")
            final_answer = Execute_steps(conditions,objectives,steps)
            print("  \n# final_answer:", final_answer)
            
            # Achieve one potiential answer
            Answer = re.search(r'\\boxed\{(.*)(?=\})', final_answer)  
            if Answer:
                Answer_boxed = Answer.group(1)
            else:
                Answer_boxed = "No match found"
            possible_answers.append(Answer_boxed)
            if voter_count >= min_voters:
                counter = Counter(possible_answers)
                most_votes = counter.most_common(1)[0][1]  
                tie_count = len(list(filter(lambda x: x[1] == most_votes, counter.items())))
                
                tie = tie_count > 1
                print("\nThere is a tie vote. We need to add another voter.")
                if voter_count >= max_voters:
                    print("\nReached maximum voter limit.")
                    break
        most_possible_answer, count = counter.most_common(1)[0]
        print(f"  \nThe final answer is {most_possible_answer}")
        return most_possible_answer
    except Exception as e:
        print(f"Error processing file: {e}")


def evaluate_dataset(folder_path, times, n, limit=5):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    random.shuffle(all_files)  # Shuffle the order of files randomly

    for count, file_path in enumerate(all_files[:limit]):
        with open(file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
                problem = data.get("problem")
                if problem:
                    print(f"#{count} Problem:\n", problem)
                    solution = data.get("solution")
                    print(f"#{count} Solution\n", solution)
                    main(problem, times, n)
            except json.JSONDecodeError:
                print(f"Error reading file {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                            
                                          
if __name__ == "__main__":
    n = 1 # verification times
    times = 3 # The upper limit of the mining times
    min_voters = 3 # min number of voters
    max_voters = 5 # max number of voters
    question = """
    Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Each step, you are only allowed to choose two of the remaining numbers to obtain a new number.
    
Rules of the 24 Game
Use each of the four numbers exactly once
Use only basic arithmetic operations: addition (+), subtraction (-), multiplication (×), and division (÷)
The final result must equal 24
Parentheses can be used to change the order of operations

Input: 4 4 6 8
Steps:
4 + 8 = 12 (left: 4 6 12)
6 - 4 = 2 (left: 2 12)
2 * 12 = 24 (left: 24)
Answer: (6 - 4) * (4 + 8) = 24
Input: 2 9 10 12
Steps:
12 * 2 = 24 (left: 9 10 24)
10 - 9 = 1 (left: 1 24)
24 * 1 = 24 (left: 24)
Answer: (12 * 2) * (10 - 9) = 24
Input: 4 9 10 13
Steps:
13 - 10 = 3 (left: 3 4 9)
9 - 3 = 6 (left: 4 6)
4 * 6 = 24 (left: 24)
Answer: 4 * (9 - (13 - 10)) = 24
Input: 1 4 8 8
Steps:
8 / 4 = 2 (left: 1 2 8)
1 + 2 = 3 (left: 3 8)
3 * 8 = 24 (left: 24)
Answer: (1 + 8 / 4) * 8 = 24
Input: 5 5 5 9
Steps:
5 + 5 = 10 (left: 5 9 10)
10 + 5 = 15 (left: 9 15)
15 + 9 = 24 (left: 24)
Answer: ((5 + 5) + 5) + 9 = 24
    
    3 3 8 9
 """   
    
    # Input your own question
    question = """
    Solve the game of 24 (use all 4 provided numbers exactly once each and +-/* to make 24) for [9 8 8 3]"""

    main(question, times, n, min_voters, max_voters)  # Assuming these are defined elsewhere
