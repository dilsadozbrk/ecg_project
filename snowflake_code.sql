select current_account();

CREATE OR REPLACE SCHEMA snowpark_stages;
CREATE OR REPLACE SCHEMA RAW_DATA;
CREATE OR REPLACE STAGE ECG_DB.snowpark_stages.csv_stage;
CREATE OR REPLACE SCHEMA ECG_DB.file_format;

-- CSV file format template
CREATE OR REPLACE FILE FORMAT ECG_DB.file_format.csv_format
type = csv
field_delimiter = ','
skip_header = 1;

list @SNOWPARK_STAGES.csv_stage;
select t.$1, t.$2, t.$3, t.$15 From @SNOWPARK_STAGES.csv_stage (file_format => 'ECG_DB.FILE_FORMAT.csv_FORMAT', pattern=>'.*hea_files.*[.]csv.gz') t;


// Creating a raw table 
CREATE OR REPLACE TABLE ECG_DB.RAW_DATA.RAW_PATIENT (
Age INT
, SEX Varchar(2)
, DX_1 VARCHAR(50)
, DX_2 VARCHAR(50)
, DX_3 VARCHAR(50)
, DX_4 VARCHAR(50)
, DX_5 VARCHAR(50)
, DX_6 VARCHAR(50)
, DX_7 VARCHAR(50)
, DX_8 VARCHAR(50)
, DX_9 VARCHAR(50)
, DX_10 VARCHAR(50)
, DX_11 VARCHAR(50)
, DX_12 VARCHAR(50)
, id INT
);


// Copying the csv file into table from stage 
COPY INTO ECG_DB.RAW_DATA.RAW_PATIENT
FROM @SNOWPARK_STAGES.CSV_STAGE
file_format = (format_name = ECG_DB.FILE_FORMAT.csv_FORMAT)
files = ('hea_files.csv.gz');


select * from ECG_DB.RAW_DATA.RAW_PATIENT;

CREATE OR REPLACE TABLE ECG_DB.RAW_DATA.raw_ecg_dimensions (
 Dim_1 INT
, Dim_2 INT
, Dim_3 INT
, Dim_4 INT
, Dim_5 INT
, Dim_6 INT
, Dim_7 INT
, Dim_8 INT
, Dim_9 INT
, Dim_10 INT
, Dim_11 INT
, Dim_12 INT
, Patient_id INT);


COPY INTO ECG_DB.RAW_DATA.raw_ecg_dimensions
FROM @ECG_DB.SNOWPARK_STAGES.CSV_STAGE
file_format = (format_name = ECG_DB.FILE_FORMAT.csv_FORMAT)
pattern = 'mab[_0-9]*.csv.gz';

select Count(*) from raw_ecg_dimensions;