import os
import csv
import re
import pandas as pd
from tqdm import tqdm
from typing import Callable

def remove_boxed_text(input_string:str) -> str:
    """
    Remove the boxed text from a string.
    """
    match = re.search(r'\\boxed\{(.*?)\}', input_string)
    label_match = re.search(r'Label: \{(.*?)\}', input_string)

    # Check if there was a match and extract the content
    if match:
        parsed_value = match.group(1)
        return parsed_value
    elif label_match:
        parsed_value = label_match.group(1)
        return parsed_value
    else:
        return input_string
    

def evaluate_game_of_24(engine: Callable, debug:bool, model_name: str, steps:int, n:int, min_voters:int, max_voters:int):
    """
    Evaluate the performance of a model on the Game of 24 task.
    """
    outputs = []
    answers = []
    success_rate = 0
    total = 0
    
    datasets = list(pd.read_csv("data/game_24/24.csv")['Puzzles'])

    def is_valid_solution(input_nums, equation):
        try:
            # Check if the equation evaluates to 24
            result = eval(equation)
            if result != 24:
                return False

            # Check if all input numbers are used exactly once
            input_counts = {str(num): input_nums.count(num) for num in input_nums}
            for num in input_counts:
                if equation.count(num) != input_counts[num]:
                    return False
            return True
        except:
            return False
    
    for data in tqdm(datasets):
        
        # Generate model output
        task_instrcution = """
        Use numbers and basic arithmetic operations (+ - * /) to obtain 24. 
        Each step, you are only allowed to choose two of the remaining numbers to obtain a new number. 
        Make sure all four numbers must be used exactly once and they are all used.
                
        Rules of the 24 Game:
        1. Use each of the four numbers exactly once
        2. Use only basic arithmetic operations: addition (+), subtraction (-), multiplication (×), and division (÷)
        3. The final result must equal 24
        4. Parentheses can be used to change the order of operations
        """.strip()
        
        input = task_instrcution + "\ninput:" + data
        
        raw_model_output = engine(
            input,
            steps=steps,
            n=n,
            min_voters=min_voters,
            max_voters=max_voters,
        )
        model_output = remove_boxed_text(raw_model_output)
        
        if debug:
            print(f"Data: {data}")
            print(f"Model Output: {model_output}")
            input()
        else:
            outputs.append(model_output)

            # Check if the model's output is a valid solution
            if is_valid_solution(data, model_output):
                success_rate += 1

            total += 1

    try:
        os.makedirs("/output")
        print("create output directory")
    except:
        pass

    # Save results to a file
    with open(f"/output/{model_name}_game_of_24.txt", "w+") as f:
        for k, (output, answer) in enumerate(zip(outputs, answers)):
            f.write(f"{k} | OUTPUT: {output} | ANSWER: {answer}\n")

        f.write("#####################\n")
        print(f"Success Rate = {success_rate}/{total} = {success_rate/total:.3f}")
        f.write(f"Success Rate = {success_rate}/{total} = {success_rate/total:.3f}\n")