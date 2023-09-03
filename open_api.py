import openai
from decouple import config

# Set your OpenAI API key
openai.api_key = config("OPEN_API_SK_KEY")


def transform_text(prompt):
    # Prompt based on the provided content
    prompt = f"""
    I would like to modify the content below to prevent plagiarism.
    Kindly provide the output in HTML format and add inline css and please no color for text.

    {prompt}
    """
    # Generate additional information in HTML format
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=500,  # Adjust as needed
        temperature=0.8,  # Adjust as needed
        format="text"
    )
    # Print the generated HTML content
    generated_content = response.choices[0].text.strip()
    return generated_content


def transform_title(prompt):
    # Prompt based on the provided content
    prompt = f"""
    Give me a new title  using this title below but make it different but same meaning

    {prompt}
    """
    # Generate additional information in HTML format
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=100,  # Adjust as needed
        temperature=0.8,  # Adjust as needed
        format="text"
    )
    # Print the generated HTML content
    generated_content = response.choices[0].text.strip()
    return generated_content


# print(transform_title("2022 Grey Cup Winner and Full List of Winners"))
# print(transform_text("""
# <ul>
# <li>First Round: April 15-29.</li>
#
#
#
# <li>Second Round: April 30-June 15.</li>
#
#
#
# <li>Conference Finals: May 16-30.</li>
#
#
#
# <li>Stanley Cup Finals: June 3-17.</li>
# </ul>"""))
