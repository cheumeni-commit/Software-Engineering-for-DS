
import joblib

from src.config.directories import directories
from src.constants import SAVE_MODEL


def predict(X):
    model = load_model()
    result = model_inference(model, X)
    return result

def load_model():
    loaded_model = joblib.load(directories.raw_store_dir + '/' + SAVE_MODEL)
    return loaded_model

def model_inference(loaded_model, X):
    result = loaded_model.predict(X)
    return result