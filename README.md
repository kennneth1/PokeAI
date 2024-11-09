### Train Model
- cd into the training/ folder then create and start a virtual env, run: `pip install -r requirements.txt`
- run `experiment.ipynb` which trains a XGBoost regressor model to predict price of cards

*Move the resulting tensorflow binary model file inside the inference/ folder if need to deploy & test predictions using FastAPI (make sure to reference the correct model file name in `inference/main.py`)*