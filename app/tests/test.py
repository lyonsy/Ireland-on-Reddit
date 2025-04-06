import pytest
from unittest.mock import MagicMock
from app.bot import process_submission


@pytest.fixture
def mock_submission():
    mock_submission = MagicMock()
    mock_submission.title = "Test Submission Title"
    mock_submission.url = "https://example.com"
    mock_submission.subreddit.display_name = "test_subreddit"
    mock_submission.permalink = "/r/test_subreddit/comments/12345/test_submission"
    return mock_submission


@pytest.fixture
def mock_config():
    mock_config = MagicMock()
    mock_config.SUBREDDIT_TO_POST = "subreddit_to_post"
    mock_config.POST_MODE = "comment"
    return mock_config


def test_process_submission(mock_submission, mock_config, mocker):
    mock_reddit = MagicMock()
    mocker.patch("app.bot.config", mock_config)
    mock_new_post = mocker.patch("app.bot.new_post")
    process_submission(mock_reddit, mock_submission)
    mock_reddit.subreddit.assert_called_once_with("subreddit_to_post")
    mock_new_post.assert_called_once()

    args, kwargs = mock_new_post.call_args
    assert args[0] == mock_reddit.subreddit.return_value
    assert args[1] == "[r/test_subreddit] Test Submission Title"
    assert args[2] == "https://example.com"
    assert (
        "https://www.reddit.com/r/test_subreddit/comments/12345/test_submission"
        in args[3]
    )
