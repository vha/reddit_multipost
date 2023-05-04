# Reddit multipost

Command line tool to post to multiple subreddits at the same time that works with both text and image posts. Can also automatically post a comment on image posts after creation.

## Setup

- Install requirements:

```sh
pip install -r requirements.txt
```

- Rename `clients_secrets_template.json` to `clients_secrets.json`.
- Create a reddit app to generate your secrets and update your `clients_secrets.json` with them - [guide](https://www.jcchouinard.com/get-reddit-api-credentials-with-praw/).
- Create a text file (or use `example_subreddits.txt` as a base) with the subreddits you want to post to, separated by line breaks. Read `Subreddit file` below for the proper format.

## Usage

```sh
post.py [-h] [--nsfw] [--text TEXT] [--image_path IMAGE_PATH | --link LINK] title subreddits_path
```

It will create a self post, a link post or an image post depending on the arguments.

If only --post is set (no --image_path or --link), it will create a self post.

--link and --image_path are mutually exclusive.

If you use --text together with --link or --image_path, it will post a comment with --text in the image/link post created.

## Subreddit file

You can override the post title, the comment or add a flair on a subreddit basis.

### File format

Each line of the file corresponds to a different subreddit to post to. If you want to post to two subreddits, your txt must have exactly 2 lines. Don't leave an empty line.
This is the line format:

```txt
<subreddit>;[<title>];[<flair>];[<comment>]
```

Only `subreddit` is mandatory. you can leave the rest blank to use the default leaving just the `;`. This is a valid subreddit entry that will post to `subreddittest`:

```txt
subreddittest;;;
```

If you don't want to post a comment to a subreddit specifically, you can type `False` in the `comment` portion:

```txt
subreddittest;;;False
```

Check the `example_subreddits.txt` file for more examples.

### Examples

#### Create a selfpost

```sh
python post.py "Test post title" "/path/to/subreddits.txt" --text "This will be a selfpost"
```

#### Create an image post with a comment

```sh
python post.py "Test post title" "/path/to/subreddits.txt" --image_path "/path/to/image.png" --text "This will be a comment in the image post"
```

#### Create a link post with no comment

```sh
python post.py "Test post title" "/path/to/subreddits.txt" --link "https://www.example.com/"
```



