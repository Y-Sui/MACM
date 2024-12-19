# Thinker
Analysis_conditions_objective = """
Help me to analyze the conditions and the objective of a problem. 
The objective should cover the main goal of the problem and the constraints that need to be satisfied.
The conditions must be derived directly from the problem; deductions or calculations to establish these conditions are not allowed.
You don't need to provide me with a solution for the time being.

Example 1:
Question:
Louis earns a base monthly salary of $\\$$1,200 with 5$\\%$ commission on sales. For a month with $\\$$25,000 in sales, what are Louis's total earnings?
Conditions:
1. Louis earns a base monthly salary of $1,200.
2. He also earns a commission of 5$\\%$ on sales.
3. In a particular month, Louis makes $25,000 in sales.
Objective:
Calculate Louis's total earnings for the month, which includes both his base salary and the commission from the sales. The constraints are that the commission is 5$\\%$ of the sales and the base salary is fixed at $1,200.

Example 2:
Question:
A line segment has one endpoint at $(6,8)$ and midpoint at $(1,1)$. What is the sum of the coordinates of the other endpoint?
Conditions:
1. A line segment has one endpoint at (6,8).
2. The midpoint of this line segment is at (1,1).
Objective:
1. Find the coordinates of the other endpoint of the line segment.
2. Find the sum of these coordinates.
3. The constraints are that the midpoint of the line segment is at (1,1) and one endpoint is at (6,8).

Real question:
Question:
{Question}
"""

Fix_conditions_prompt = """
I need you to fix a conclusion based on a problem. 
You only need to find some content, which is similar to wrong the conclusion from the problem description as the fixed conclusion.
You just need to provide the fixed conclusion, don't say any other words

Example 1:
problem:
Avery earns 30$ each day, how much will he earn for 30 days?
Wrong statement:
Avery earns 20$ each day
Fixed statement:
Avery earns 30$ each day

Example 2:
problem:
The sum of two numbers is 25 and their difference is 9. What is their product?
Wrong statement:
The sum of two numbers is 18
Fixed statement:
The sum of two numbers is 25

Real question:
problem:
{question}
Wrong statement:
{Initial_conditions}
Fixed statement:
"""
# Discover_new_conditions = """
# I need you to derive some useful, specific conditions with logical relationships for a target, based on some known conditions 
# (at least 3). You will need to clearly indicate to me which known condition or conditions led you to each of these new conditions.

# Example 1:
# Known conditions: 
# 1. f(3) = 5
# 2. for all x > 0, f(3x) = f(x) + 2
# Objective:
# 1. find $f^{{-1}}(11)$
# New conditions:
# 1. Based on Known condition 2, we can get: f(9) = f(3) + 2.
# 2. Based on Known condition 2, and Known condition 1, we can get: f(9) = 7.
# 3. Based on Known condition 2, we can get: f(27) = f(9) + 2.

# Example 2:
# Known conditions: 
# 1. The difference between the squares of two different prime numbers is 1488.
# 2. Both prime numbers are less than 50.
# Objective:
# 1. Identify the two prime numbers that satisfy these conditions.
# 2. Submit the numbers in either order, separated by a comma.
# New conditions:
# 1. Based on Known condition 1, we can get: Both primes are odd.
# 2. Based on Known condition 1 and Known condition 2, we can get: One prime is significantly larger than the other.
# 3. Based on Known condition 1, we can get: The larger prime number cannot be 3,5, or 7.

# Real question:
# Known conditions:
# {Known_conditions}
# Objective:
# {Objective}
# New conditions:
# """

# Discover_new_conditions = """
# I need you to derive the most direct condition with logical relationships, based on some known conditions. 
# You can NOT skip the intermediate steps by using the conditions that are not directly shown in the known conditions.
# You have to use code to perform the math calculation.
# You will need to clearly indicate to me which known condition or conditions led you to each of these new conditions by using the same format as the examples (Based on Known condition..., we can get:...Reason:..)

# Example 1:
# Known conditions: 
# 1. f(3) = 5
# 2. for all x > 0, f(3x) = f(x) + 2
# Objective:
# 1. find $f^{{-1}}(11)$
# New condition:
# Based on Known condition 2, we can get: f(9) = f(3) + 2.
# Reason: when x = 3, f(3*3) = f(3) + 2, thus f(9) = f(3) + 2.

# Example 2:
# Known conditions: 
# 1. The difference between the squares of two different prime numbers is 1488.
# 2. Both prime numbers are less than 50.
# Objective:
# 1. Identify the two prime numbers that satisfy these conditions.
# 2. Submit the numbers in either order, separated by a comma.
# New condition:
# Based on Known condition 1 and Known condition 2, we can get: One prime is significantly larger than the other.
# Reason: 1488 is a large number compare with 50

# Real question:
# Known conditions:
# {Known_conditions}
# Objective:
# {Objective}
# New condition:
# """

# Thinker for the new conditions

Discover_new_conditions = """
I have some known conditions:
{Known_conditions}
And my objective is:
{Objective}
Reflections from my supervisor (if any):
{Reflections}
Guidances from my supervisor (if any):
{Guidances}
Please follow the supervisor's feedback (reflections and guidances) to generate new conditions based on the known conditions.

NOTE:
1. You are only allowed to use the known conditions to generate new conditions (the new conditions are the trial-and-error process, aka your thinking process).
2. You have to follow the feedback from the supervisor.
3. You have to use code to perform the math calculation.
4. Don't repeat the known conditions in the new conditions, only provide the new conditions.
"""

Summarize_Answer = """
Please summarize your answer by using the following format:
Based on Known condition and supervisor's feedback [provide the conditions and supervisor feedback], we can get: [new conditions here]
"""


# Discover_new_conditions = """
# I need you to derive the most direct condition with logical relationships, based on some known conditions. 
# You can NOT skip the intermediate steps by using the conditions that are not directly shown in the known conditions.
# You have to use code to perform the math calculation.
# You will need to clearly indicate to me which known condition or conditions led you to each of these new conditions by using the same format as the examples (Based on Known condition..., we can get:...Reason:..)

# Example 1:
# Known conditions: 
# 1. f(3) = 5
# 2. for all x > 0, f(3x) = f(x) + 2
# New condition:
# Based on Known condition 2, we can get: f(9) = f(3) + 2.
# Reason: when x = 3, f(3*3) = f(3) + 2, thus f(9) = f(3) + 2.

# Example 2:
# Known conditions: 
# 1. The difference between the squares of two different prime numbers is 1488.
# 2. Both prime numbers are less than 50.
# New condition:
# Based on Known condition 1 and Known condition 2, we can get: One prime is significantly larger than the other.
# Reason: 1488 is a large number compare with 50

# Real question:
# Known conditions:
# {Known_conditions}
# New condition:
# """


# Determine_Steps = """
# I need you to come up with one solution targeted at our objective, based on all the known conditions. 
# Each solution should include specific and clear steps.

# Example 1:
# Known conditions: 
# 1. f(3) = 5
# 2. for all x > 0, f(3x) = f(x) + 2
# 3. Because f(3x) = f(x) + 2, so f(9) = f(3) + 2
# 4. Because f(3x) = f(x) + 2, and f(3) = 5, so f(9) = 7
# 5. Because f(3x) = f(x) + 2, so f(27) = f(9) + 2
# Objective:
# find $f^{{-1}}(11)$
# Solutions:
# Step 1:
# Use f(9) to find f(27)
# Step 2:
# Use f(27) to find f(81)
# Step 3:
# Repeat until find x that f(x) = 11

# Example 2:
# Known conditions: 
# 1. a + 1 / b = 22 / 7
# 2. b + 1 / c = 8
# 3. abc = 21
# 4. c = 1 / (8 - b)
# 5. a = (22 / 7) - (1 / b) 
# Objective:
# Calaculate c + 1 / a
# Solutions:
# Step 1:
# Substitude a in abc = 21 by (22 / 7) - (1 / b) 
# Step 2:
# Substitude c in abc = 21 by 1 / (8 - b) 
# Step 3:
# Calculate b 
# Step 4:
# Calculate a and c
# Step 5:
# Calculate c + 1 / a

# Real question:
# Known conditions:
# {Known_conditions}
# Objective:
# {Objective}
# Solutions:
# """


Determine_Steps = """
Help me to come up with one solution targeting at our objective. 

Example 1:
Known conditions: 
1. f(3) = 5
2. for all x > 0, f(3x) = f(x) + 2
3. Because f(3x) = f(x) + 2, so f(9) = f(3) + 2
4. Because f(3x) = f(x) + 2, and f(3) = 5, so f(9) = 7
5. Because f(3x) = f(x) + 2, so f(27) = f(9) + 2
Objective:
find $f^{{-1}}(11)$
Solutions:
Step 1:
Use f(9) to find f(27)
Step 2:
Use f(27) to find f(81)
Step 3:
Repeat until find x that f(x) = 11

Example 2:
Known conditions: 
1. a + 1 / b = 22 / 7
2. b + 1 / c = 8
3. abc = 21
4. c = 1 / (8 - b)
5. a = (22 / 7) - (1 / b) 
Objective:
Calaculate c + 1 / a
Solutions:
Step 1:
Substitude a in abc = 21 by (22 / 7) - (1 / b) 
Step 2:
Substitude c in abc = 21 by 1 / (8 - b) 
Step 3:
Calculate b 
Step 4:
Calculate a and c
Step 5:
Calculate c + 1 / a

Real question:
Known conditions:
{Known_conditions}
Objective:
{Objective}
Solutions:
"""

# Judge

Judge_condtion = """
I need you to determine if the statement is a condition included inside the problem.
You are only allowed to use the 'True' or 'False' as the final answer.
If it is correct, answer 'True'. 
If it is not correct, answer 'False'. 

Example 1:
problem:
Avery earns 30$ each day, how much will he earn for 30 days?
Statement:
Avery earns 20$ each day
Judgement:
False

Example 2:
problem:
The sum of two numbers is 25 and their difference is 9. What is their product?
Statement:
The sum of two numbers is 25
Judgement:
True

Real question:
problem:
{question}
Statement:
{Initial_conditions}
Judgement:
"""

# Judge_T_F = """
# I need you to determine if the statement is correct or not based on the current conditions? 
# You are only allowed to use the 'True' or 'False' as the final answer.
# If it is correct, answer 'True'. 
# If it is not correct, answer 'False'. 
# You need to use code to determine if you can.

# Example 1: 
# Known condtions:
# 1. S = a / (1 - b)
# 2. 1 / S = b / (1 - a)
# statement: 
# Based on Known condition 1 and Known condition 2, we can get: (a / (1 - b)) * (b / (1 - a)) = 1
# Answer:
# True

# Example 2: 
# Known condtions:
# 1. a = 22 / 7 - 1 / b
# 2. a + 1 / c = 8
# statement: 
# Based on Known condition 1, we can get: a = 22b / (7b - 1)
# Answer:
# False

# Real question:
# Known condtions:
# {Known_condtions}
# statement:
# {condition_from_thinker}
# Answer:
# """

# Judge_T_F = """
# Help me to carefully verify if the statement is correct.
# You have to use code to verify the math calculation.
# Just answer "True" or "False"

# Example 1: 
# Known condtions:
# 1. S = a / (1 - b)
# 2. 1 / S = b / (1 - a)
# statement: 
# Based on Known condition 1 and Known condition 2, we can get: (a / (1 - b)) * (b / (1 - a)) = 1
# Answer:
# True

# Example 2: 
# Known condtions:
# 1. a = 22 / 7 - 1 / b
# 2. a + 1 / c = 8
# statement: 
# Based on Known condition 1, we can get: a = 22b / (7b - 1)
# Answer:
# False

# Real question:
# Known condtions:
# {Known_condtions}
# statement:
# {condition_from_thinker}
# Answer:
# """

Judge_T_F = """
I have some Known condtions:
{Known_condtions}
Help me to carefully verify if the statement:
{condition_from_thinker} is correct.
You have to use code to verify the math calculation.
"""

T_or_F_prompt = """
Please just tell me if the statement is correct by using 'True' or 'False'.
"""


# Judge_if_got_Answer = """
# I need you to determine if the objective is included inside the current conditions? 
# You are only allowed to use the 'True' or 'False' as the final answer.
# If yes, answer 'True'. 
# If No, answer 'False'. 
# You can use code to determine if necessary.

# Example 1: 
# Known condtions:
# 1. S = a / (1 - b)
# 2. 1 / S = b / (1 - a)
# Objective: 
# find the value of a + b
# Answer:
# False

# Example 2: 
# Known condtions:
# 1. a = 22 / 7 - 1 / b
# 2. a + 1 / c = 8
# Objective: 
# find a + 1 / c
# Answer:
# True

# Real question:
# Known condtions:
# {Known_condtions}
# Objective: 
# {Objective}
# Answer:
# """


# Judge_if_got_Answer = """
# Help me to determine if the objective is one of the current conditions.
# You are only allowed to use the 'True' or 'False' as the final answer.

# Example 1: 
# Known condtions:
# 1. S = a / (1 - b)
# 2. 1 / S = b / (1 - a)
# Objective: 
# find the value of a + b
# Answer:
# False

# Example 2: 
# Known condtions:
# 1. a = 22 / 7 - 1 / b
# 2. a + 1 / c = 8
# Objective: 
# find a + 1 / c
# Answer:
# True

# Real question:
# Known condtions:
# {Known_condtions}
# Objective: 
# {Objective}
# Answer:
# """



Judge_if_got_Answer = """
I have some known conditions:
{Known_condtions}
And I want to {Objective}.
Help me to determine if the objective can be obtained based on the known conditions or the objective is already one of the current conditions.
Only when you find a direct solution in the known conditions, you can answer 'True'.
You have to use code to verify the math calculation.

Key Instructions:
* Employ at least 10 distinct reasoning steps in the conditions. Otherwise, answer 'False'.
"""

If_got_Answer_T_F = """
Please summarize your analysis just by using 'True' or 'False'.
"""


# Executor

# find_target = """
# I need you to find the final objective based on some condtions and several steps, you need to use \\boxed to mark your answer.
# You can use code if necessary.
# Our objective is:
# {Objective}
# We have:
# {Conditions}
# You can use the following steps:
# {Steps}
# You final answer:
# """

find_target = """
I need you to find the final objective based on some steps.
Our objective is:
{Objective}
We have:
{Conditions}
The steps that you should follow:
{Steps}
You answer:
"""

box_target = """Now you need to use \\boxed to mark your answer. 
If the task is to find a expression that fit the requirement, please just return the expression without calculation. 
For example, if the task requires you find a expression that is equal to 24, please return the expressiion like 3 * (3 + 8) - 9 = 24.
Otherwise, don't return anything else, just return float number in \\boxed.
"""


# Meta-reasoner

Provide_meta_guidance = """
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

Guidance_answer = """
Please provide your guidance by using the following format:
Based on the known conditions and objective, we can get: [provide your reflection here]
Guidance: [provide your exact guidance here]
"""