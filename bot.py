import time
import os
import logging
import praw
from config import *
import config


logging.basicConfig(
    level=logging.INFO, format="%(levelname)s: %(asctime)s - %(message)s"
)
# logging.disable(logging.CRITICAL)


def authenticate():
    logging.info("Authenticating...")
    reddit = praw.Reddit(
        client_id=config.CLIENT_ID,
        client_secret=config.client_secret,
        password=config.password,
        user_agent="MyBot",
        username=config.username,
    )
    logging.info("Authenticated as {}".format(reddit.user.me()))
    return reddit


def process_submission(reddit, submission):
    title = submission.title  # Submission's title
    url = submission.url  # Submission's url
    xpost = "[r/{}] ".format(
        submission.subreddit.display_name
    )  # x-post string: [r/subreddit]
    source_url = (
        "https://www.reddit.com" + submission.permalink
    )  # link to submission's comment section

    new_post_title = xpost + title
    new_post_url = url
    post_to = reddit.subreddit(SUBREDDIT_TO_POST)

    new_post(post_to, new_post_title, new_post_url, source_url)
    logging.info(new_post_title)


def new_post(subreddit, title, url, source_url):
    if POST_MODE == "direct":
        post = subreddit.submit(title, url=url)
        comment_text = "[Link to original post here]({})".format(source_url)
        post.reply(comment_text).mod.distinguish(sticky=True)

    elif POST_MODE == "comment":
        subreddit.submit(title, url=source_url)

    else:
        logging.ERROR('Invalid POST_MODE chosen. Select "direct" or "comment".')


def monitor(reddit, submissions_found):
    counter = 0
    for submission in reddit.subreddit(SUBREDDITS_TO_MONITOR).hot(limit=SEARCH_LIMIT):
        for expression in EXPRESSIONS_TO_MONITOR:
            if (
                expression in submission.title.lower()
                and submission.id not in submissions_found
            ):
                if submission.over_18:
                    logging.ERROR(
                        "Post %s is NSFW:%s " % submission.title, submission.id
                    )
                    break
                else:
                    process_submission(reddit, submission)
                    submissions_found.append(submission.id)
                    counter += 1

                    with open("submissions_processed.txt", "a") as f:
                        f.write(submission.id + "\n")

    logging.info(str(counter) + " submission(s) found")  # log results

    # Sleep for a few minutes
    logging.info("Waiting...")  # log results
    time.sleep(WAIT_TIME * 60)


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

    # Authentication
    reddit = authenticate()

    # Monitor Reddit for new submissions
    submissions_found = get_submissions_processed()
    while True:
        try:
            monitor(reddit, submissions_found)
        except Exception as e:
            logging.warning("Random exception occurred: {}".format(e))
            time.sleep(WAIT_TIME * 60)


if __name__ == "__main__":
    main()
