import sys
sys.tracebacklimit = 1
from src.pipeline.training_pipeline import TrainingPipeline

print("Starting training pipeline...")

pipeline = TrainingPipeline()
pipeline.run_pipeline()

print("Pipeline finished.")