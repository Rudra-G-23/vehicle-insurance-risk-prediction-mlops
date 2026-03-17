**Intro**
  - Make a repo
  - Clone and I used uv package manger 
  - You also used Basic import like pandas and scikit-learn


**MongoDB**
  - Create an account in [MongoDB](https://www.mongodb.com/)
  - Use free account
  - Organization -> Project -> Cluster
  - Click  network access in side bar add ip address then allow `0.0.0.0/0`
  - Inside cluster connection config
    -  Copy the user and password -> save somewhere
    -  Then select the vs code connection and copy the link.
  - Lean Process not step

**Hide the Credentials**
  - Now we want to push the local data into mongodb 
  - For this we need to create the connection
  - To do that first hide the credentials
  - `uv add python-dotenv` then used anywhere 😁
  - Inside the the the `.env` file, example
  ```txt
  MONGO_USERNAME=rudra_db_user
  MONGO_PASSWORD=ABCDEFGHabced123
  MONGO_CLUSTER=vehicle-cluster.12345px3.mongodb.net
  ```

**Connect with the MongoDB**
  - After this 
  ```py
  client = pymongo.MongoClient(CONNECTION_URL)
  data_base = client[DB_NAME]
  collection = data_base[COLLECTION_NAME]
  ``` 
  - The uploading all the data into server. 
  - First time 😆
  - Then go the website the check the data. 
  - Explore website
  
**Logging & Citation**
  - Create an folder src/logger/__init__.py
  - Then write the code for logging. 
  - Helps in Debugging.
  - Citation used for credit. [GitHub](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)
  - I learn during research paper reading time. 
  - So I think to implement on my work.
  - **Practical Tips**
    1. Always log pipeline start/end
    2. Log data shapes
    3. Log model metrics
    4. Always log exceptions
    5. Use rotating logs
  - Use this `uv pip install -e .`. 
  
**Exception**
  - Used this to detect the error.
  - First think simple then what we need during debugging time.
  - That simple added.
  - At the end using the trackback standard python library we trackback to exact line where the error occurs.
  - In the test folder test_exception.py we test how it works.

**Constants**
  - Define all the variables and directory name at one place
  - Easy to find and centralized place.

**MongoDB Connection**
  - Write the code for connecting the data with the database.

**Config (mongodb to df)**
  - This time we create a script for 
  - Fetch data from MongoDB and create pandas DF

**Data Integration**
- Constant
  - Added in __init__.py 
- Config entity
  - Where file need to store 
  - Mention on this file
- Artifact entity
  - During process time 
  - What it produce 
- Components
  - `components/data_ingestion.py`
  - The code what you written on the `data_access/proj1_data.py`
  - all the function call on this data ingestion py script
- Pipeline
  - This data ingestion py file added in 
  - Pipeline .py script
- app . py / demo .py
  - Run in demo and test


**Pipeline**
  - Training pipeline
  - star_data_ingestion function 
  - at the end run the all pipeline
  - Create a script on test folder 
  - And test it.

**Error - 1 [Data Ingestion Pipeline]**
  - During fetching data from the MongoDB
  - We suffer from error so we created a bugfix/branch 
    - Issues
      - Constants naming issues
      - File miss match
      - DB to connection 
      - DB load error
      - Timeout Error
      - Exception Module Error
      - And What not 🫨
  - Fix all issues and now all done.
  - Merge this branch with the main branch.

**Utils**
  - This script we wrote read and write the `yaml` and `array`
  - We created the utility function for all the application.

**Data Validation**
  - Constants
  - Config Entity
  - Config Artifact
  - Utils 
  - Add all of this to validate the data
  - We write everything in `components/data_validation.py`
  - Add the config/schema.yaml so we can validate
  - Used that in pipeline 
  - Then test all of this.

**Improvement of Data Validation Pipeline**
  - We know that we not prefer to used the f-string in production application/
  - From now we used like this
  ```py
  # Simple
  logger.info(f"Schema Loaded: {self._schema_config}")

  # Industry
  logger.info("Schema Loaded: %s", self._schema_config)
  ```

  - What we added in our code
    - Column existence
    - Column order
    - Data Type
    - Numerical / Categorical groups
    - Missing value threshold
    - Data Drift


**Data Transformation**
  - After validate our data we need to
  - Transform our data so our model can train.
  - First constants
  - Then entity both artifact and config
  - Then added a `components/data_transformation.py`

```yaml
Data Ingestion
      ↓
Data Validation
      ↓
Data Transformation  ← this code
      ↓
Model Trainer
      ↓
Model Evaluation
      ↓
Model Pusher
```
- Add in the training pipeline
- Fix the error and more error 

**Model Trainer**
  - This time we update all const, artifact and config
  - For Model Trainer: `components/model_trainer.py`
  - Added `src\entity\estimator.py` for the model trainer
  - After used create estimator + model trainer script 
  - We all added into pipeline by creating start model trainer 
  - Then call inside the run pipeline and then test the file.
  - Without error life is boring so we found the folder miss 