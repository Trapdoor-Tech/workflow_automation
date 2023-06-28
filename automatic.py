import httpx
import openai
import os
from notion_client import Client


# Retrieve API key and parent page ID from environment variables
api_key = os.environ.get("NOTION_API_KEY")
parent_page_id = os.environ.get("NOTION_PARENT_PAGE_ID")

#input definition
name = "Multilinear Extensions"
page_title = name
def generate_prompt():
    prompt = name,
    return prompt   

def generate_system_prompt():
    conversation = """First of all,  Limit the length of response within 900 words. You will assume the role of a math teacher, and I will ask questions regarding definitions. Your responses should include the following components:

Provide the background information of the given definition.
Explain the purpose or application of this definition.
Offer an example to enhance my comprehension of this definition.
Provide a proof or justification for the validity of the definition.
Introduce the relationship with zk-snark.

The response should be organized on a Notion page with the following headings: Background, Usage, Example, ,Proof and Relationship;"""
    return conversation   

prompt = generate_prompt()
prompt = " ".join(prompt)
system_prompt = generate_system_prompt()
system_prompt = " ".join(system_prompt)
response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", 
                        "content": prompt},
                      {
                     "role": "system",
                        "content": system_prompt
                     }]
            )

result = response.choices[0].message.content


def create_notion_page(api_key, parent_page_id, page_title, content):
    """
    Create a new page under an existing Notion page.

    :param api_key: Notion API key.
    :param parent_page_id: The ID of the parent page under which the new page will be created.
    :param page_title: The title of the new page.
    :param content: The content to insert into the page.
    :param notion_version: The version of the Notion API to use (default is "2021-08-16").
    :return: The response from the Notion API.
    """
    # Split the content into pieces of 2000 characters or less
    content_pieces = [content[i:i+2000] for i in range(0, len(content), 2000)]

    # Build the children array with separate paragraph blocks for each content piece
    children = []
    for piece in content_pieces:
        paragraph_block = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": piece
                        }
                    }
                ]
            }
        }
        children.append(paragraph_block)


    # Define the payload
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": page_title
                        }
                    }
                ]
            }
        },
        "children":children
    }

    # Define the headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Send a POST request to create a new page in the Notion database
    response = httpx.post("https://api.notion.com/v1/pages", json=payload, headers=headers)

    # Return the response
    return response.json()


# Create a new page in Notion under the parent page
response = create_notion_page(api_key, parent_page_id, page_title, result)

# Print the response
print(response)
