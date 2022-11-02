# Spotify ETL data pipeline project

## Objective

* A pet project written in Python that builds a simple datafeed of my personal listening history on Spotify, which is a baseline for future enhancements as I gain knowledge in data engineering.
* Acknowledgement : The python script is referenced from [this resource](https://github.com/karolina-sowinska/free-data-engineering-course-for-beginners/blob/master/main.py).

## Components

![diagram](https://i.imgur.com/pcLMoou.png)

* This project is essentially a simple ETL pipeline that:
  * Extract data from spotify public API
  * Transform / validate data received
  * Load the final data into local SQLite database within the Pandas dataframe.

### 1. Extract Data from spotify

* Utilize [requests](https://pypi.org/project/requests/) to create an authorized GET request to spotify's [API](https://developer.spotify.com/console/get-recently-played/).
  * `after` parameter in the request is narrowed down to 24 hours counting from now.
* Parse JSON response with python's built-in json parser. Note that the objects has been narrowed down for purpose of simple data feed: Track name, Artist name, Timestamp, Played date.
  * Create a set of lists with coresponding name as target.
  * Identify the coresponding key-value pair in JSON schema, then use `.append()` method to populate the lists.

### 2. Transform data

* In order to validate data on the script itself, the data is stored in a Pandas dataframe. A dictionary is defined coresponding to extracted lists.
* Call the user-defined validate function `transform_aka_validation(song_df)` which includes :
  * Validate empty dataframe : the pipeline should raise exception if there are no data extracted. [Pandas](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.empty.html) provide a handy method `df.empty` to check if dataframe is null.
  * Validate unique records : no meaningful analysis can come from duplicated dataset - to prevent this, a simple check for unique Primary Key is used. For this data schema, `timestamp` (UNIX timestamp when a given track is played) is the best candidate.

### 3. Load data to local database

* The Load script is executed for a successuful validation; Data stored in dataframe can now be loaded into a local SQLite database.
  * Setup the connection with (1)db engine [SQLalchemy](https://www.sqlalchemy.org/) and (2) cursor [sqlite3 connection](https://www.tutorialspoint.com/python_data_access/python_sqlite_cursor_object.htm).
  * With the cursor in place, execute sql command to create a table `my_played_tracks` by `cursor.execute(<sql_command>)` method
  * Load data from dataframe to the newly created table via Pandas' `DataFrame.to_sql()` method.
* After successful load, the local database is created at the project's root folder, which can be accessed with a RDBMS - Dbeaver or example : ![table](https://i.imgur.com/RpVjrWP.png)

## Conclusion

* This project provides an outline to build a simple ETL script. The script can be manually executed, though an automated scheduler is preferred for nature of data pipelines.
* Main area of improvement can be easily identified further down the road :
  * Automate API token generation to account for token expiration. For now the workaround is a snippet to raise exception respond code != 200.
  * Implement Airflow to orchestrate DAGs (schedule automated jobs) for a much more useful pipeline.
  * Implement analytics tools at the receiving end of pipeline.
  * Various improvements for Transformation step to ensure data integrity in Extraction.

## Extras - steps to recreate the project

* Apart from required parameters in the script, this project includes python dependencies which is listed in `requirements.txt` doc.
* For recreational purpose, after cloning the repo please
  1. install said dependencies using `pip install -r requirements.txt`.
  2 . use python to run main.py script.
