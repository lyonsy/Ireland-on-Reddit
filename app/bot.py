import time
import os
import logging
import praw
import config


logging.basicConfig(
    level=logging.INFO, format="%(levelname)s: %(asctime)s - %(message)s"
)


def authenticate():
    logging.info("Authenticating...")
    reddit = praw.Reddit(
        client_id=config.CLIENT_ID,
        client_secret=config.client_secret,
        password=config.password,
        user_agent="MyBot",
        username=config.username,
    )
    logging.info(f"Authenticated as {reddit.user.me()}")
    return reddit


def process_submission(reddit, submission):
    title = " " + submission.title
    url = submission.url
    xpost = f"[r/{submission.subreddit.display_name}]"
    source_url = f"https://www.reddit.com{submission.permalink}"

    new_post_title = xpost + title
    new_post_url = url
    post_to = reddit.subreddit(config.SUBREDDIT_TO_POST)

    new_post(post_to, new_post_title, new_post_url, source_url)
    logging.info(new_post_title)


def new_post(subreddit, title, url, source_url):
    if config.POST_MODE == "direct":
        post = subreddit.submit(title, url=url)
        comment_text = f"[Link to original post here]({source_url})"
        post.reply(comment_text).mod.distinguish(sticky=True)
    elif config.POST_MODE == "comment":
        subreddit.submit(title, url=source_url)
    else:
        logging.ERROR('Invalid POST_MODE chosen. Select "direct" or "comment".')


def monitor(reddit, submissions_found):
    counter = 0
    for submission in reddit.subreddit(config.SUBREDDITS_TO_MONITOR).hot(
        limit=config.SEARCH_LIMIT
    ):
        for expression in config.EXPRESSIONS_TO_MONITOR:
            if (
                expression in submission.title.lower()
                and submission.id not in submissions_found
            ):
                if submission.over_18:
                    logging.ERROR(f"Post {submission.title} is NSFW: {submission.id}")
                    break
                else:
                    process_submission(reddit, submission)
                    submissions_found.append(submission.id)
                    counter += 1

                    with open("submissions_processed.txt", "a") as f:
                        f.write(submission.id + "\n")

    logging.info(f"{counter} submission(s) found")

    logging.info("Waiting...")
    time.sleep(config.WAIT_TIME * 60)


def get_submissions_processed():
    if not os.path.isfile("submissions_processed.txt"):
        submissions_processed = []
    else:
        with open("submissions_processed.txt", "r") as f:
            submissions_processed = f.read()
            submissions_processed = submissions_processed.split("\n")

    return submissions_processed


def main():
    logging.info("Reddit bot running...")
    reddit = authenticate()

    submissions_found = get_submissions_processed()
    while True:
        try:
            monitor(reddit, submissions_found)
        except Exception as e:
            logging.warning(f"Random exception occurred: {e}")
            time.sleep(config.WAIT_TIME * 60)


if __name__ == "__main__":
    main()
