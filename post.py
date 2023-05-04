# Import the argparse module and the reddit_multi library
import argparse
import json
import praw
from praw.models import Subreddit, Submission
from PIL import Image


def post(title: str, subreddits: list, image_path: str = None, text: str = None):
    # Read and parse the client_secrets.json file
    with open('client_secrets.json') as f:
        secrets = json.load(f)

    reddit = praw.Reddit(
        client_id=secrets['client_id'],
        client_secret=secrets['client_secret'],
        user_agent=secrets['user_agent'],
        refresh_token=secrets['refresh_token'],
        timeout=60
    )

    for subreddit_name in subreddits:
        subreddit: Subreddit = reddit.subreddit(subreddit_name)
        if not image_path:
            subreddit.submit(title=title, selftext=text)
            continue

        post = subreddit.submit_image(
            title=title, image_path=str(image_path))

        if text:
            post.reply(text)


# Create a parser object
parser = argparse.ArgumentParser(
    description='Post on reddit using reddit_multi')

# Add an argument for the path to the file
parser.add_argument('title', type=str, help='The title of the post')
parser.add_argument('subreddits', type=argparse.FileType('r'),
                    help='Path to a text file with the list of subreddits, separated by line breaks')
parser.add_argument('--image_path', type=str,
                    help='The path to the image to post')
parser.add_argument('--text', type=str,
                    help='The text to post. If used with image_path, it will post a comment in the image post')

# Parse the arguments
args = parser.parse_args()

# if args.image_path and args.text:
#     raise argparse.ArgumentError(
#         'You can only use either --image_path or --text, not both')


if args.image_path:
    # Ensure the path is a valid image, or it will raise an exception
    with open(args.image_path) as f:
        img = Image.open(args.image_path)
        img.format

subreddits = ''.join(args.subreddits).splitlines()

post(args.title, subreddits, args.image_path, args.text)
