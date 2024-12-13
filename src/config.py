import sys

try:
    execution_date_str = sys.argv[1]
except Exception as e:
    print(f"Error with an input execution date parameter. Error {e}")
    sys.exit(1)


TMP_FILE_PATH = '/opt/airflow/data/'
POSTS_STATS_FILE_NAME = 'posts_weekly_statistics_'
SEARCH_STATS_FILE_NAME = 'year_search_count'
AWS_BUCKET_NAME = "strike-stats"

SUBREDDIT = 'cormoran_strike'
CHARACTERS_LIST = ['Matthew', 'Lucy', 'Leda', 'Charlotte', 'Wardle', 'Anstis', 'Shanker', 'Ilsa', 'Nick', 'Barclay', 'Pat']


