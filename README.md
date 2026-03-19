# 🚗 Vehicle Insurance Risk Prediction – End-to-End MLOps Project

An **industry-style Machine Learning Operations (MLOps) project** that predicts vehicle insurance risk using an automated ML pipeline.

This project demonstrates how a machine learning system moves from **data ingestion → model training → evaluation → deployment → CI/CD automation** using modern MLOps practices.

---

# 📌 Problem Statement

Insurance companies need to estimate the **risk associated with insuring a vehicle**.
Accurate risk prediction helps companies:

* Reduce financial loss
* Price policies correctly
* Detect high-risk customers

This project builds a **complete ML pipeline** that automates this prediction process.


![Pipeline Architecture Diagram](./assets/helper/pipeline-architecture-1.png)

---

# 🚀 Project Highlights

- ✔ End-to-End MLOps Pipeline
- ✔ MongoDB Data Source
- ✔ Modular ML Pipeline Architecture
- ✔ AWS S3 Model Registry
- ✔ Dockerized Application
- ✔ CI/CD with GitHub Actions
- ✔ Automated Deployment on AWS EC2

---

# 🏗️ Project Architecture


```
Data Source
   │
   ▼
MongoDB Atlas
   │
   ▼
Data Ingestion
   │
   ▼
Data Validation
   │
   ▼
Data Transformation
   │
   ▼
Model Training
   │
   ▼
Model Evaluation
   │
   ▼
Model Registry (AWS S3)
   │
   ▼
Prediction Pipeline
   │
   ▼
Flask Web Application
   │
   ▼
Docker Container
   │
   ▼
CI/CD Pipeline (GitHub Actions)
   │
   ▼
AWS EC2 Deployment
```

# 🎥 Demo

The project provides a Flask web interface for predictions.



# ⚡ Installation

Clone the repository:

```bash
git clone https://github.com/Rudra-G-23/vehicle-insurance-risk-prediction-mlops.git
cd vehicle-insurance-risk-prediction-mlops
```

Create environment:

```bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
```

Install dependencies:
<!--pip install -r requirements.txt-->
```bash
uv sync
```

---

# ⚙️ Tech Stack

**Programming**

* Python

**Machine Learning**

* Scikit-learn
* Pandas
* NumPy
* Polars

**Database**

* MongoDB Atlas

**Cloud Services**

* AWS S3 (Model Registry)
* AWS EC2 (Deployment)
* AWS ECR (Docker Image Storage)

**DevOps & MLOps**

* Docker
* GitHub Actions
* CI/CD Pipeline
* Self Hosted Runner

**Web Framework**

* Flask

---

# 📂 Project Structure

```
vehicle-insurance-risk-prediction-mlops
│
├── artifacts
│
├── notebook
│   ├── EDA.ipynb
│   └── mongoDB_demo.ipynb
│
├── src
│   │
│   ├── components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   │
│   ├── configuration
│   │   ├── mongo_db_connection.py
│   │   └── aws_connection.py
│   │
│   ├── entity
│   │   ├── config_entity.py
│   │   ├── artifact_entity.py
│   │   └── estimator.py
│   │
│   ├── data_access
│   │   └── proj1_data.py
│   │
│   ├── pipeline
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   │
│   ├── utils
│   │   └── main_utils.py
│   │
│   ├── exception.py
│   └── logger.py
│
├── static
├── templates
│
├── app.py
├── demo.py
├── requirements.txt
├── setup.py
├── pyproject.toml
├── Dockerfile
└── README.md
```

---

# 🚀 Project Workflow

## 1. Project Setup

Create project template and install dependencies.

```bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
```

---

## 2️. MongoDB Atlas Setup

MongoDB is used as the **data source** for the pipeline.

Steps:

1. Create MongoDB Atlas account
2. Create a new cluster
3. Create database user
4. Allow network access

```
0.0.0.0/0
```

5. Copy the connection string.

Example:

```
mongodb+srv://username:password@cluster.mongodb.net
```

---

## 3️. Data Ingestion

The ingestion pipeline:

* Connects to MongoDB
* Fetches raw dataset
* Converts JSON data to Pandas DataFrame
* Splits dataset into **train and test**

Output artifacts:

```
artifacts/data_ingestion/train.csv
artifacts/data_ingestion/test.csv
```

---

## 4️. Data Validation

Validation checks ensure:

* correct schema
* correct data types
* no missing columns

Configuration file:

```
config/schema.yaml
```

---

## 5️. Data Transformation

Feature engineering pipeline performs:

* missing value handling
* categorical encoding
* feature scaling

Output artifacts:

```
transformed_train.npy
transformed_test.npy
preprocessor.pkl
```

```
Data Ingestion  →  Data Validation  →  Data Transformation  →  Model Trainer
     ↓                    ↓                    ↓                    ↓
 raw data          clean data         numpy arrays         model.pkl
                                    (preprocessor.pkl)
 ```

---

## 6️. Model Training

Multiple models are trained and compared.

The best performing model is selected based on evaluation metrics.

Artifacts generated:

```
model.pkl
training_metrics.json
```

```
 config/model.yaml   →   read params
                         ↓
                  train model
                         ↓
artifact/model.pkl  →   save trained model
```

---

## 7️. Model Evaluation

The new trained model is compared with the **previous production model stored in AWS S3**.

If performance improves beyond the threshold:

```
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE = 0.02
```

The model is promoted.

---

## 8️. Model Registry (AWS S3)

The selected model is pushed to an **S3 bucket**.

Example bucket:

```
my-model-mlopsproj
```

Used for:

* model versioning
* model tracking

---

## 9. Prediction Pipeline

The prediction pipeline:

* loads the trained model
* preprocesses new input data
* returns prediction results

Implemented using **Flask API**.

---

## 10. CI/CD Pipeline

Continuous integration and deployment using **GitHub Actions**.

Workflow:

```
Code Push
   ↓
GitHub Actions Trigger
   ↓
Docker Image Build
   ↓
Push to AWS ECR
   ↓
Deploy on AWS EC2
```

## 11. Docker Setup

Build docker image:

```bash
docker build -t vehicle-insurance .
```

Run container:

```bash
docker run -p 5080:5080 vehicle-insurance
```

---

## 12. AWS Deployment

Deployment infrastructure:

* **AWS ECR** → store docker image
* **AWS EC2** → host application
* **GitHub Runner** → automate deployment

Application endpoint:

```
http://<EC2_PUBLIC_IP>:5080
```

Training endpoint:

```
http://<EC2_PUBLIC_IP>:5080/training
```

---

# 🔮 Future Improvements

* Add experiment tracking using MLflow
* Implement model monitoring
* Add data drift detection
* Deploy using Kubernetes
* Implement feature store

---

# 👨‍💻 Author

**Rudra Prasad Bhuyan**

* GitHub: https://github.com/Rudra-G-23
* LinkedIn: https://www.linkedin.com/in/rudra-prasad-bhuyan-44a388235

Give the repository a **star ⭐** and feel free to contribute.

# ⭐ Citation
```bibtex
@misc{bhuyan2026vehicle_mlops,
  author = {Bhuyan, Rudra Prasad},
  title = {Vehicle Insurance Production Grade MLOps Capstone},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  url = {https://github.com/Rudra-G-23/vehicle-insurance-risk-prediction-mlops}
}
```