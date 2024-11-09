from fastapi import FastAPI
import xgboost as xgb
import numpy as np
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    mos_since_release: float
    num_grade: int
    is_secret: float
    is_full_art: float
    is_eeveelution: float
    is_legendary: float
    is_og_char: float
    is_tag_team: float
    is_alt_art: float
    bb_mo_price_by_set: float
    avg_mo_price_by_grade_set: float
    ir_score: float

# Initialize FastAPI app
app = FastAPI()

# Load the trained XGBoost model
model = xgb.XGBRegressor()
model.load_model('models/my_model.bin')  # Load the saved binary model
feature_names = model.get_booster().feature_names
print("Feature names:", feature_names)

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Convert the input data to a numpy array for prediction
        data = np.array([[
            request.mos_since_release,
            request.num_grade,
            request.is_secret,
            request.is_full_art,
            request.is_eeveelution,
            request.is_legendary,
            request.is_og_char,
            request.is_tag_team,
            request.is_alt_art,
            request.avg_mo_price_by_grade_set,
            request.bb_mo_price_by_set,
            request.ir_score
        ]])  # Ensure it's a 2D array for prediction

        # Predict using the model
        prediction = model.predict(data)
        
        return {"prediction": round(prediction.tolist()[0],2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")