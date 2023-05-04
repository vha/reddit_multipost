# Reddit multipost

Command line tool to post to multiple subreddits at the same time that works with both text and image posts. Can also automatically post a comment on image posts after creation.

## Setup

- Install requirements:

```sh
pip install -r requirements.txt
```

- Rename `clients_secrets_template.json` to `clients_secrets.json`.
- Create a reddit app to generate your secrets and update your `clients_secrets.json` with them - [guide](https://www.jcchouinard.com/get-reddit-api-credentials-with-praw/).
- Create a text file with the subreddits you want to post to, separated by line breaks. You can select a flair for your post using a comma after the subreddit's name. See `example_subreddits.txt` for an example.

## Usage

```sh
python post.py title subreddits_path [--image_path IMAGE_PATH] [--text TEXT]
```

### Example

```sh
python post.py "Test post title" "/path/to/subreddits.txt" --image_path "/path/to/image.png" --text "This will be a comment in the image post"
```

It will create either a post or an image post depending on the arguments. 

If image_path is not set, it will create a text post, and viceversa.

If you pass both image_path and text, it will create an image post and post a comment with the text.
