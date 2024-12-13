import os
import sys
import praw
from datetime import datetime, timedelta
import csv
import config
from logger import logger

"""
    PRAW docs: https://praw.readthedocs.io/en/stable/code_overview/models/submission.html
"""


run_date_str = config.execution_date_str

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

def main():
    reddit_instance = get_reddit()
    subreddit_weekly_statistics(reddit_instance,config.SUBREDDIT,run_date_str)
    popular_characters(reddit_instance, config.SUBREDDIT, config.CHARACTERS_LIST)


def get_reddit():
    try:
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT
            )
        return reddit
    except Exception as e:
        logger.exception
        sys.exit(1)

   
def subreddit_weekly_statistics(reddit, subreddit, run_date_str):
    """
        Geeting reddit statistics
        Args:
            reddit - reddit instance
            subreddit(str): subreddit name
            run_date_str(str): "%Y%m%d"
    """   
    run_date = datetime.strptime(run_date_str, "%Y%m%d").date()
    week_ago_date = run_date -timedelta(weeks=1)
    
    headers = ['post_id', 'created_timestamp', 'author', 'title', 'upvotes', 'comments', 'monday_of_the_week', 'created_date']
    with open(f'{config.TMP_FILE_PATH}{config.POSTS_STATS_FILE_NAME}{run_date_str}.csv','w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
     
    try:   
        subreddit = reddit.subreddit(subreddit)
    except Exception as e:
        logger.exception(f"Cannot get the subreddits's submissions. Error {e}")
        
    for s in subreddit.new(limit=1000):
        submission_date = datetime.fromtimestamp(s.created_utc).date()

        if submission_date >= week_ago_date and submission_date<run_date:
            monday_of_the_week = submission_date - timedelta(days=submission_date.weekday())
            with open(f'{config.TMP_FILE_PATH}{config.POSTS_STATS_FILE_NAME}{run_date_str}.csv','a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([s.id, int(s.created_utc), s.author, s.title, s.score, s.num_comments, monday_of_the_week, submission_date])
            
"""
    Returns the length of the list of all submissions made in a year timeframe 
    found by a search word in subreddit
    Args:
        reddit - reddit instance
        subreddit(str): subreddit name
        search_wotd: str
"""
def search_count(reddit, subreddit, search_word):
    try:
        submissions = reddit.subreddit(subreddit).search(query=search_word, sort="relevance", time_filter="year", limit=None)
    except Exception as e:
        logger.exception(f"Cannot get the subreddits's submissions for _{search_word}_ search word. Error {e}")
    return len(list(submissions))


"""     
    Saving search results in .csv file: going through the list of names, 
    calculating mentions count
"""
def popular_characters(reddit, subreddit, characters_list):
    headers = ['name', 'count']
    with open(f"{config.TMP_FILE_PATH}{config.SEARCH_STATS_FILE_NAME}.csv",'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

    for character in characters_list:
        n = search_count(reddit,subreddit, character)
        with open(f"{config.TMP_FILE_PATH}{config.SEARCH_STATS_FILE_NAME}.csv",'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([character, n])


    
if __name__ == "__main__":
    main()