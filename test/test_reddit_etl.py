import pytest
import os
import praw
import boto3
import psycopg2

    
"""
TODO: business cases data checks, aws infrastructure checks
"""
SUBREDDIT_NAME='cormoran_strike'
SEARCH_WORD = 'Cormoran'

@pytest.fixture
def reddit_api_connection():
        reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT")
            )
        return reddit
    
@pytest.fixture
def get_subreddit_submission(reddit_api_connection):
    subreddit = reddit_api_connection.subreddit(SUBREDDIT_NAME)
    submission = next(subreddit.new(limit=1))
    return submission


@pytest.fixture
def aws_s3_connection():
        s3 = boto3.resource(
        's3',
        region_name=os.getenv("REGION_NAME"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        return s3

@pytest.fixture
def aws_redshift_connection():
        conn = psycopg2.connect(
        host=os.getenv("REDSHIFT_HOST"),
        port=os.getenv("REDSHIFT_PORT"),
        dbname=os.getenv("REDSHIFT_DBNAME"),
        user=os.getenv("REDSHIFT_USER"),
        password=os.getenv("REDSHIFT_PASSWORD")
        )
        return conn



def test_reddit_api_connection(reddit_api_connection):
    assert reddit_api_connection is not None


def test_subreddit_submission(reddit_api_connection):
    subreddit = reddit_api_connection.subreddit(SUBREDDIT_NAME)
    test_submission = next(subreddit.new(limit=1))
    assert test_submission is not None
    

@pytest.mark.parametrize("field", ["id", "created_utc", "author", "title", "score", "num_comments"])
def test_submission_fields(get_subreddit_submission, field):
    assert hasattr(get_subreddit_submission, field), f"Missing expected field: {field}"
    assert getattr(get_subreddit_submission, field) is not None, f"Field '{field}' is None"


@pytest.mark.parametrize("attr,expected_type", [
    ("id", str),
    ("created_utc", float),
    ("author", praw.models.reddit.redditor.Redditor),
    ("title", str),
    ("score", int),
    ("num_comments", int)
])
def test_submission_attribute_types(get_subreddit_submission, attr, expected_type):
    value = getattr(get_subreddit_submission, attr, None)
    assert isinstance(value, expected_type), f"Expected {attr} to be {expected_type}, got {type(value)}"



def test_subreddit_search(reddit_api_connection):
    search_result_submission = reddit_api_connection.subreddit(SUBREDDIT_NAME).search(
        query=SEARCH_WORD,
        limit=1
    )
    assert search_result_submission is not None


def test_s3_connection(aws_s3_connection):
    assert aws_s3_connection is not None


def test_redshift_connection(aws_redshift_connection):
    assert aws_redshift_connection is not None


