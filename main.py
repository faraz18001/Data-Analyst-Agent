from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai.helpers.openai_info import get_openai_callback
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

llm = OpenAI(api_token="")

# Define your enhanced custom prompt
custom_prompt = """
You are an intelligent and friendly AI assistant specializing in data analysis. Your task is to analyze the given DataFrame containing transactional and customer data, and provide insights in a clear, concise, and engaging manner.

When responding to user queries:
1. Always maintain a friendly and professional tone.
2. Provide results in a well-structured and easy-to-read format, using markdown for formatting when appropriate.
3. Instead of raw data, give summarized insights and key takeaways.
4. If asked for visualizations, create appropriate charts or graphs using Matplotlib or Seaborn. Ensure the visualizations are clear, informative, and visually appealing.
5. Offer additional insights or follow-up questions that might be relevant to the user's query.
6. If you cannot answer a query based on the available data, politely explain why and suggest alternative questions that could be answered with the given information.

Remember, your goal is to make data analysis accessible and understandable to users of all levels of expertise. Always strive to provide value and clarity in your responses.
"""

# Enable conversational mode, visualization, and set the custom prompt
df = SmartDataframe("DU Cash Card Aug.xlsx", 
                    config={
                        "llm": llm, 
                        "conversational": True, 
                        "enable_visualization": True,
                        "prompt_template": custom_prompt
                    })

def display_image(image_path):
    img = plt.imread(image_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

with get_openai_callback() as cb:
    while True: 
        user_query = input('Please enter your query (or type "exit" to quit): ')
        
        if user_query.lower() == 'exit':
            print("Thank you for using the Data Analysis Assistant. Goodbye!")
            break
        
        response = df.chat(user_query)

        if response is not None:
            print("\n" + "="*50 + "\n")
            print("Data Analysis Assistant:")
            print(response)
            
            # Check if a visualization was generated
            import os
            image_files = [f for f in os.listdir() if f.endswith('.png') and f.startswith('temp_chart')]
            if image_files:
                print("\nHere's the visualization you requested:")
                display_image(image_files[0])
                os.remove(image_files[0])  # Remove the temporary image file
            
            print("\n" + "="*50 + "\n")

        print("OpenAI API Usage:")
        print(cb)
        print("\n" + "="*50 + "\n")