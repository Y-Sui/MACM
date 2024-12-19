import os
from openai import OpenAI
from load_dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("METAREASONER_OPENAI_API_KEY"))
   
def generate_from_thinker(prompts, max_tokens, model="gpt-4o-mini", temperature=0.7, n=1):
    assistant = client.beta.assistants.create(
        model=model,
        instructions="""You are a thinker. I need you to help me think about some problems.
        You need to provide me the answer based on the format of the example.""".strip(),
        name="Thinker",
        tools=[{"type": "code_interpreter"}],
    )

    thread = client.beta.threads.create()
    for i in range(len(prompts)):   
        message = prompts[i]["content"]

        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        ) 
        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )      
        while run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if keep_retrieving_run.status == "completed":
                # print("\n")

                all_messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                # print(f"all_messages:\n{all_messages}")
                
                try:
                    Assistant_response = all_messages.data[0].content[0].text.value
                except Exception as e:
                    print(f"An error occurred: {e}") # Avoid the image outputs
                    Assistant_response = "I need to rethink this problem."
                break

            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                print(f"Run status: {keep_retrieving_run.status}")
                break
    return Assistant_response  
        

def generate_from_meta_reasoner(prompts, max_tokens, model="gpt-4o-mini", temperature=0.7, n=1):
    assistant = client.beta.assistants.create(
        model=model,
        instructions="""You are a Meta-reasoner, tasked with analyzing the reasoning process of another AI and providing guidance for its further steps. Your goal is to provide explicit guidance to improve the efficiency and effectiveness of the AI's problem-solving approach.""".strip(),
        name="Meta-reasoner",
        tools=[{"type": "code_interpreter"}],
    )

    thread = client.beta.threads.create()
    for i in range(len(prompts)):   
        message = prompts[i]["content"]

        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        ) 
        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )      
        while run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if keep_retrieving_run.status == "completed":
                all_messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                try:
                    Assistant_response = all_messages.data[0].content[0].text.value
                except Exception as e:
                    print(f"An error occurred: {e}") # Avoid the image outputs
                    Assistant_response = "I need to rethink this problem."
                break

            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                print(f"Run status: {keep_retrieving_run.status}")
                break
    return Assistant_response  
        

def generate_from_judge(prompts, max_tokens, model="gpt-4o-mini", temperature=0.7, n=1):

    assistant = client.beta.assistants.create(
        model=model,
        instructions="""You're a judge. I need you to make judgments on some statements.""".strip(),
        name="Judge",
        tools=[{"type": "code_interpreter"}],
    )

    thread = client.beta.threads.create()
    for i in range(len(prompts)):   
        message = prompts[i]["content"]

        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        ) 
        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )      
        while run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if keep_retrieving_run.status == "completed":
                all_messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                try:
                    Assistant_response = all_messages.data[0].content[0].text.value
                except Exception as e:
                    print(f"An error occurred: {e}") # Avoid the image outputs
                    Assistant_response = "False"
                break

            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                print(f"Run status: {keep_retrieving_run.status}")
                break
    return Assistant_response


def generate_from_executor(prompts, max_tokens, model="gpt-4o-mini", temperature=0.7, n=1):
    assistant = client.beta.assistants.create(
        model=model,
        instructions="""You're an excutor. I need you to calculate the final result based on some conditions and steps.
        You need to provide me the answer based on the format of the examples.""".strip(),
        name="Executor",
        tools=[{"type": "code_interpreter"}],
    )

    thread = client.beta.threads.create()
    for i in range(len(prompts)):   
        message = prompts[i]["content"]

        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        ) 
        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )      
        while run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if keep_retrieving_run.status == "completed":
                # print("\n")

                all_messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                # print(f"all_messages:\n{all_messages}")
                
                try:
                    Assistant_response = all_messages.data[0].content[0].text.value
                except Exception as e:
                    print(f"An error occurred: {e}") # Avoid the image outputs
                    Assistant_response = "False"
                break

            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                print(f"Run status: {keep_retrieving_run.status}")
                break
    return Assistant_response

