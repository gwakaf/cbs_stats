import os
import psycopg2
from psycopg2 import sql
import config
from logger import logger

"""TODO: To get more information about the error, query the STL_LOAD_ERRORS table.  """

run_date_str = config.execution_date_str    
YEAR = run_date_str[:4]


host = os.getenv("REDSHIFT_HOST")
port = os.getenv("REDSHIFT_PORT")
dbname = os.getenv("REDSHIFT_DBNAME")
user = os.getenv("REDSHIFT_USER")
password = os.getenv("REDSHIFT_PASSWORD")
redshift_iam_role = os.getenv("REDSHIFT_IAM_ROLE")



def main():
    conn = connect_to_redshift()
    cur = conn.cursor()
    
    try:
        cur.execute(create_posts_stats_table_query)
        cur.execute(create_search_stats_table_query)
        conn.commit()
        logger.info("Tables created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
        
    try:
        cur.execute(copy_command_s3_to_rds(redshift_iam_role,
                                           "search_statistics",
                                           f"s3://{config.AWS_BUCKET_NAME}/search_stats/{config.SEARCH_STATS_FILE_NAME}.csv"))
        conn.commit()
    except Exception as e:
        logger.exception("Error copying the data to Redshift: ")
        conn.rollback()
        cur.execute(load_errors_query)
        load_errors = cur.fetchall()
        logger.error("Recent Redshift load errors:")
        for error in load_errors:
            logger.error(f"Time: {error[0]}, File: {error[1]}, Line: {error[2]}, "
                        f"Column: {error[3]}, Type: {error[4]}, Reason: {error[5]}")
        
        
        
    try:
        cur.execute(copy_command_s3_to_rds(redshift_iam_role,
                                           "posts_statistics",
                                           f"s3://{config.AWS_BUCKET_NAME}/posts_stats/{config.SEARCH_STATS_FILE_NAME}.csv"))
    except Exception as e:
        logger.exception("Error copying the data to Redshift: ")
        conn.rollback()
        cur.execute(load_errors_query)
        load_errors = cur.fetchall()
        logger.error("Recent Redshift load errors:")
        for error in load_errors:
            logger.error(f"Time: {error[0]}, File: {error[1]}, Line: {error[2]}, "
                        f"Column: {error[3]}, Type: {error[4]}, Reason: {error[5]}")
            
        
    cur.close()
    conn.close()
    logger.info("Connection closed.")
    
    

def connect_to_redshift():
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        logger.info("Connected to Redshift")
    except Exception as e:
        logger.exception("Unable to connect: ")
    return conn

def copy_command_s3_to_rds(iam_role, table_name, s3_path):
    
    return f"""
        COPY {table_name}
        FROM {s3_path}
        IAM_ROLE {iam_role}
        DELIMITER ','
        CSV;
    """




"""Queries """
# Create posts_statistics table
create_posts_stats_table_query = """
CREATE TABLE posts_statistics (
    post_id VARCHAR(50) UNIQUE,
    created_timestamp INT,
    author VARCHAR(100),
    title VARCHAR(300),
    upvotes INT,
    comments INT,
    monday_of_the_week DATE
);
"""

# Create search_statistics table
create_search_stats_table_query = """
CREATE TABLE search_statistics (
    name VARCHAR(200) UNIQUE,
    count INT
);
"""

# Query STL_LOAD_ERRORS redshift system table to get more details about loading errors
load_errors_query = """
    SELECT starttime, filename, line_number, colname, type, err_reason
    FROM stl_load_errors
    ORDER BY starttime DESC
    LIMIT 10;
    """





if __name__ == "__main__":
    main()