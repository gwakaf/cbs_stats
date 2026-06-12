# Subreddit Statistics ETL
Airflow-orchestrated ETL pipeline that extracts Reddit API data from a subreddit dedicated to the Cormoran Strike novels by Robert Galbraith, stages it in AWS S3, loads curated data into Redshift, validates transformations with Pytest, and visualizes trends in Looker Studio. It can be easily customized for a different subreddit by adjusting a few parameters.

## Table of Contents
- [Overview](#overview)
- [Tech Stack and Architecture](#tech-stack-and-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
  - [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)


## Overview
This project demonstrates a common production-style analytics pipeline pattern:
  - extract data from an external API
  - load raw data into a staging area
  - clean, validate, and transform the data
  - load curated data into an OLAP data warehouse
  - visualize analytical insights in a dashboard


## Tech Stack and Architecture
<img width="899" alt="Screenshot 2025-01-25 at 9 17 20 PM" src="https://github.com/user-attachments/assets/7f85cba4-2e6d-48b3-ba5a-3875a58751b9" />

+ Extract data from Reddit API
+ Load into AWS S3
+ Copy to AWS Redshift
+ Visualize with Looker Studio Dashboard
+ Orchestrate with Airflow in Docker


## Getting Started
### Prerequisites
- docker to run Airflow locally
- AWS S3 bucket
- Amazon Redshift instance
- Looker Studio dashboard template
  
### Configuration
Set up environment variables for connections to:
- Reddit API
- AWS S3
- AWS Redshift

Required Python dependencies are defined in `docker-compose.yaml` using `PIP_ADDITIONAL_REQUIREMENTS`.

### Installation
1. Clone the repository  
2. Add your .env file with environment variables (refer to the configuration section for details).
3. Start the Docker containers using the docker-compose.yaml file:
   ```bash
   docker-compose up
4. Trigger airflow dag manually or schedule it

## Usage
+ The ETL pipeline is scheduled to run weekly in Airflow. It extracts subreddit data, stores raw or staged data in AWS S3, and loads curated tables into Amazon Redshift.
To backfill historical data, run:
   ```bash
    docker-compose exec airflow-scheduler airflow dags backfill -s 2023-01-01 -e 2024-10-31 reddit_pipeline_dag

+ To customize this project for another subreddit, you need to change the subreddit's name and the words of interest variables in src/config.py to your desired values.

## Testing/Data Quality
The Airflow pipeline includes a validation task that runs Pytest checks for the ETL logic. These tests help verify that extracted Reddit data is cleaned, transformed, and prepared correctly before loading.

   ```bash
    pytest test/test_reddit_etl.py
```

+ Example checks include:
  - Required field checks for post title, author, created timestamp, score, and comment count.
  - Null and empty-value checks for fields used in transformations and dashboard metrics.
  - Type validation for numeric fields such as score, number of comments, and timestamps.
  - Duplicate detection to avoid loading the same Reddit post multiple times.
  - Transformation checks to verify calculated metrics and keyword/category flags.
  - Row-count checks between extraction, staging, and curated outputs.
  - Load validation to confirm that curated data is available in Amazon Redshift for dashboarding.

## Results
Looker Studio Dashboard

<img width="599" alt="st_pic" src="https://github.com/user-attachments/assets/8c882be1-1935-4f32-a5e8-d250498f537a" />

