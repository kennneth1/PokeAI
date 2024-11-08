### Train Model
- cd into training then create and start a virtual env, then `pip install -r requirements.txt`
- run `experiment.ipynb` which trains a XGBoost regressor model to predict price of cards

*Move the tensorflow binary model file inside the inference/ folder if need to deploy & test predictions using FastAPI (make sure to reference the correct model file name in `inference/main.py`*

### Testing Inference: Dockerize and test locally
- cd into inference then start up docker and run the following commands:
- `docker build -t fastapi-model .`
- `docker run -d -p 80:80 fastapi-model`

`Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method POST -ContentType "application/json; charset=utf-8" -Body '{
    "mos_since_release": 15,
    "is_near_mint_ungraded": 0,
    "grade_category": 1,
    "is_secret": 1,
    "is_full_art": 0,
    "is_eeveelution": 0,
    "is_legendary": 1,
    "is_og_char": 0,
    "is_gallery": 0,
    "bb_mo_price_by_set": 300,
    "ir_score": 0
}'`


