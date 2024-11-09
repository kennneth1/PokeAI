from fastapi import FastAPI
import xgboost as xgb
import numpy as np
from pydantic import BaseModel, Field
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class PredictionRequest(BaseModel):
    mos_since_release: int = Field(..., ge=0, description="Months since release, must ge 0")
    num_grade: int = Field(..., ge=1, le=10, description="Numerical PSA grade between 1 and 10")
    is_secret: int = Field(..., ge=0, le=1, description="Binary flag (0 or 1)")
    is_full_art: int = Field(..., ge=0, le=1, description="Binary flag (0 or 1)")
    is_eeveelution: int = Field(..., ge=0, le=1, description="Binary flag (0 or 1)")
    is_legendary: int = Field(..., ge=0, le=1, description="Binary flag (0 or 1)")
    is_og_char: int = Field(..., ge=0, le=1, description="Binary flag (0 or 1)")
    is_tag_team: int = Field(..., ge=0, le=1, description="Binary flag (0 or 1)")
    is_alt_art: int = Field(..., ge=0, le=1, description="Binary flag (0 or 1)")
    bb_mo_price_by_set: float = Field(..., ge=10, description="Avg booster box price of set for this month")
    avg_mo_price_by_grade_set: float = Field(..., ge=10, description="Avg price of set/grade for this month")
    ir_score: int = Field(..., ge=0, le=3, description="3 for SIR, 1 for IR")

# Initialize FastAPI app
app = FastAPI()

# Load the trained XGBoost model
model = xgb.XGBRegressor()
model.load_model('models/my_model.bin')  # Load the saved binary model
feature_names = model.get_booster().feature_names
print("Feature names:", feature_names)

@app.post("/predict")
async def predict(request: PredictionRequest):
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
        predicted_price = round(prediction.tolist()[0], 2)
        return {"prediction": predicted_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")


class InvalidDataError(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(InvalidDataError)
async def invalid_data_handler(request: Request, exc: InvalidDataError):
    return JSONResponse(
        status_code=400,
        content={"message": f"Invalid data provided: {exc.name}"}
    )