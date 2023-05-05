import argparse
import json
import os
from time import sleep
import praw
from praw.models import Subreddit, Submission
from praw.exceptions import WebSocketException, RedditAPIException
from PIL import Image
from enum import Enum


def post(title: str, subreddit_lines: list, image_path: str = None, link: str = None, text: str = None, nsfw=False):
    secrets_file = 'client_secrets.json'
    if not os.path.isfile(secrets_file):
        print(f'{secrets_file} not found. Did you rename the template?')
        exit(0)

    with open(secrets_file) as f:
        secrets = json.load(f)

    reddit = praw.Reddit(
        client_id=secrets['client_id'],
        client_secret=secrets['client_secret'],
        user_agent=secrets['user_agent'],
        refresh_token=secrets['refresh_token']
    )

    print(
        f'---------------------------\nPosting "{title}" to {len(subreddit_lines)} subreddits\n---------------------------')

    for subreddit_line in subreddit_lines:
        name, specific_title, flair_name, specific_text = subreddit_line.split(';')
        subreddit: Subreddit = reddit.subreddit(name)

        post_title = specific_title.strip() or title.strip()
        post_text = specific_text.strip() or text.strip() if text else ''
        flair_name = flair_name.strip() if flair_name else ''
        flair_id = ''

        msg_post = f'Posting on  >> {name} <<  with title "{post_title}"'

        if flair_name and subreddit.link_flair_enabled:
            flair_templates = subreddit.flair.link_templates.user_selectable()
            flair_id = next((template["flair_template_id"] for template in flair_templates if template["flair_text"] == flair_name), None)
            if flair_id:
                msg_post += f' and flair "{flair_name}"'

        print(msg_post + "...")

        try:
            if not image_path and not link:
                subreddit.submit(title=post_title, selftext=text, flair_id=flair_id, nsfw=nsfw)
                continue
            elif image_path:
                post: Submission = subreddit.submit_image(title=post_title, image_path=str(image_path), flair_id=flair_id, timeout=60, nsfw=nsfw)
            elif link:
                post: Submission = subreddit.submit(title=post_title, url=str(link), flair_id=flair_id, nsfw=nsfw)
        except (
            WebSocketException,
            BlockingIOError,
        ) as ex:
            print(f'{ex.args[0]}')
            print(f'WebSocketException, can\'t add comment to post - sleeping for a bit...')
            sleep(5)
            continue

        except RedditAPIException as ex:
            for subexception in ex.items:
                print(f'Reddits exception: [{subexception.error_type}] {subexception.message}')

            print('Skipping subreddit...')
            continue

        if post_text and post_text != "False":
            print("Posting comment...")
            post.reply(post_text)

    print('Done!')


parser = argparse.ArgumentParser(description='Post text or images on multiple subreddits')
group = parser.add_mutually_exclusive_group()
parser.add_argument('title', type=str, help='The title of the post. Can be overriden on a subreddit basis in the subreddits file.')
parser.add_argument('subreddits_path', type=argparse.FileType('r'), help='Path to a text file with the list of subreddits, separated by line breaks. Each line follows this format: subreddit;[title];[flair];[text]')
parser.add_argument('--nsfw', action='store_true', help='Marks the post as NSFW after creation')
parser.add_argument('--text', type=str, help='The text to post. If used with --image_path or --link, it will post a comment instead. Can be overriden on a subreddit basis in the subreddits file.')
group.add_argument('--image_path', type=str, help='The path to the image to post')
group.add_argument('--link', type=str, help='The URL to post')
args = parser.parse_args()

if not args.text and not args.link and not args.image_path:
    print('You have to choose the type of post to make - select at least one between --post, --link and --image_path')
    exit(0)

if args.image_path:
    # Ensure the path is a valid image, or raise an exception
    with open(args.image_path) as f:
        img = Image.open(args.image_path)
        img.format

subreddit_lines = ''.join(args.subreddits_path).splitlines()

post(args.title, subreddit_lines, args.image_path, args.link, args.text, args.nsfw)
