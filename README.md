# Subreddit Statistics ETL
Cormoran Strike Fandom Subreddit statistics.

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
This ETL pipeline analyzes activity on a subreddit dedicated to the Cormoran Strike novels by Robert Galbraith. It extracts data using the Reddit API, transforms it into a relational database format, stores the results in AWS S3, and visualizes the insights through a Looker Studio dashboard.
The project offers lighthearted and engaging statistics for fans of this beloved crime fiction series. It is also highly adaptable, allowing users to analyze any other fandom by simply providing parameters such as the subreddit name and a list of characters.


## Tech Stack and Architecture
<img width="899" alt="Screenshot 2025-01-25 at 9 17 20 PM" src="https://github.com/user-attachments/assets/7f85cba4-2e6d-48b3-ba5a-3875a58751b9" />
+ Extract data using Reddit API
+ Load into AWS S3
+ Copy to AWS Redshift
+ Visualize with Looker Studio Dashboard
+ Orchestrate with Airflow in Docker


## Getting Started
### Prerequisites
- docker to run airflow
- AWS S3 bucket
- AWS redshift instance
- Looker studio dashboard template
  
### Configuration
User has to set up environmental variables to connect:
- Reddit API
- AWS S3
- AWS Redshift

The required  dependencies are defined in docker-compose.yaml file as PIP_ADDITIONAL_REQUIREMENTS

### Installation
1. Clone the repository  
2. Add your .env file with environment variables (refer to the configuration section for details).
3. Start the Docker containers using the docker-compose.yaml file:
   ```bash
   docker-compose up
4. Trigger airflow dag manually or schedule it

## Usage
+ ETL pipeline runs weekly orchestrated by airflow, getting subreddit data and saving it to AWS S3 storage and AWS Redshidt tables
To get historic information user can use airflow backfilling command
   ```bash
    docker-compose exec airflow-scheduler airflow dags backfill -s 2023-01-01 -e 2024-10-31 reddit_pipeline_dag

+ To customize this project for another subreddit, you need to change the subreddit's name and the words of interest variables in src/config.py to your desired values.

## Testing
The airflow task is configured to execute the test.py file, which contains all the test cases written using the pytest framework.
   ```bash
      pytest src/test/test_reddit_etl.py





   
