import argparse
import json
import praw
from praw.models import Subreddit, Submission
from PIL import Image


def post(title: str, subreddits: list, image_path: str = None, text: str = None):
    with open('client_secrets.json') as f:
        secrets = json.load(f)

    reddit = praw.Reddit(
        client_id=secrets['client_id'],
        client_secret=secrets['client_secret'],
        user_agent=secrets['user_agent'],
        refresh_token=secrets['refresh_token'],
        timeout=60
    )

    for subreddit_line in subreddits:
        name, *params = subreddit_line.split(',')
        subreddit: Subreddit = reddit.subreddit(name)

        if params:
            flair_templates = subreddit.flair.link_templates
            flair_id = next(
                (template["id"] for template in flair_templates if template["text"] == params[0].strip()), None)

        if not image_path:
            subreddit.submit(title=title, selftext=text, flair_id=flair_id)
            continue

        post: Submission = subreddit.submit_image(
            title=title, image_path=str(image_path), flair_id=flair_id)

        if text:
            post.reply(text)


parser = argparse.ArgumentParser(
    description='Post text or images on multiple subreddits')

parser.add_argument('title', type=str, help='The title of the post')
parser.add_argument('subreddits_path', type=argparse.FileType('r'),
                    help='Path to a text file with the list of subreddits, separated by line breaks')
parser.add_argument('--image_path', type=str,
                    help='The path to the image to post')
parser.add_argument('--text', type=str,
                    help='The text to post. If used with image_path, it will post a comment in the image post')

args = parser.parse_args()

if args.image_path:
    # Ensure the path is a valid image, or raise an exception
    with open(args.image_path) as f:
        img = Image.open(args.image_path)
        img.format

subreddits = ''.join(args.subreddits_path).splitlines()

post(args.title, subreddits, args.image_path, args.text)
