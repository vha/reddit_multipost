# reddit_multipost

- Rename `clients_secrets_template.json` to `clients_secrets.json`.
- Create a reddit app to generate your secrets and put them in the json file - [guide](https://www.jcchouinard.com/get-reddit-api-credentials-with-praw/).
- Create a txt with the subreddits you want to post to, separated by line breaks.
- Run it
```sh 
python post.py title subreddits_path [--image_path IMAGE_PATH] [--text TEXT]
```

It will create either a post or an image post depending on the parameters. If you pass image_path and text, it will create an image post and will post a comment with the text.

Example: 
```sh
python post.py "Test post title" "./subreddits/test.txt" --image_path "/path/to/image.png" --text "This will be a comment in the image post"
```
