from openai import OpenAI
import os
from X_utils import Session, Tweet

prompt = """From this Page content, select a title from the New Reviews section and write an X post to introduce it and make people want to listen to it.
You are publishing 1 song a day. use emojis in your post when possible.
Your post should be 280 characters max. use one '\n' as a line break.
Here is a tweet example. Use exactly the same tone : 

-- input example -- 

Nick Lowe
Indoor Safari
Yep Roc
Pop/Rock
A little bit more rocking and a little bit less croony, the album features the legendary singer/songwriter in lively collaboration with Los Straitjackets.
- Tim Sendra

-- output example --

Today's new song recomendation is Indoor Safari from Nick Lowe ! \n
A little bit more rocking and a little bit less croony, the album features the collaboration with Los Straitjackets. \n

-- end of example --
"""
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_openai(messages, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def generate_post(text, prompt=prompt, max_length=None):
    # Lire les tweets de la base de données
    session = Session()
    tweets = session.query(Tweet).order_by(Tweet.id.desc()).limit(10).all()
    logtweet_content = " --- ".join([tweet.text for tweet in tweets])
    session.close()

    # Prepare messages for the OpenAI API
    messages = [
        {"role": "system", "content": "You are an assistant that analyzes web pages and creates posts for X (formerly Twitter)."},
        {"role": "user", "content": f"{prompt}\n\n Page content:\n{text}\n\nPrevious tweets:\n{logtweet_content}\n\nPlease create a new tweet about an artist mentioned in the previous tweets."}
    ]

    # Call the OpenAI API
    resp = call_openai(messages)

    # If max_length is specified and the response exceeds this length
    if max_length and len(resp) > max_length:
        print("max length recall")
        # Ask the API to reformulate while respecting the character limit
        messages.append({"role": "assistant", "content": resp})
        messages.append({"role": "user", "content": f"Please reformulate this response to be no longer than {max_length} characters."})
        resp = call_openai(messages)

    return resp