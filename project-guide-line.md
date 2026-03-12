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