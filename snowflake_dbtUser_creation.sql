# Snowflake user creation

-- Use an admin role
USE ROLE ACCOUNTADMIN;

-- Create the `transform` role
CREATE ROLE IF NOT EXISTS transform;
GRANT ROLE TRANSFORM TO ROLE ACCOUNTADMIN;

-- Create the default warehouse if necessary
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH;
GRANT OPERATE ON WAREHOUSE COMPUTE_WH TO ROLE TRANSFORM;

-- Create the `dbt` user and assign to role
CREATE USER IF NOT EXISTS dbt
  PASSWORD='**********'
  LOGIN_NAME='dbt'
  MUST_CHANGE_PASSWORD=FALSE
  DEFAULT_WAREHOUSE='COMPUTE_WH'
  DEFAULT_ROLE='transform'
  DEFAULT_NAMESPACE='ECG_DB.RAW'
  COMMENT='DBT user used for data transformation';
GRANT ROLE transform to USER dbt;

-- Create our database and schemas
CREATE SCHEMA IF NOT EXISTS ECG_DB.RAW;

-- Set up permissions to role `transform`
GRANT ALL ON WAREHOUSE COMPUTE_WH TO ROLE transform; 
GRANT ALL ON DATABASE ECG_DB to ROLE transform;
GRANT ALL ON ALL SCHEMAS IN DATABASE ECG_DB to ROLE transform;
GRANT ALL ON FUTURE SCHEMAS IN DATABASE ECG_DB to ROLE transform;
GRANT ALL ON ALL TABLES IN SCHEMA ECG_DB.RAW to ROLE transform;
GRANT ALL ON FUTURE TABLES IN SCHEMA ECG_DB.RAW to ROLE transform;

