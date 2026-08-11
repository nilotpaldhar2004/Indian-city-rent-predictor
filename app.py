import os
import logging
import time
import pickle
import pandas as pd
import xgboost as xgb
import sklearn
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("rent-api")

MODEL_PATH = os.getenv("MODEL_PATH", "xgboost_rent_model.pkl")
ENCODER_PATH = os.getenv("ENCODER_PATH", "label_encoders.pkl")
PORT = int(os.getenv("PORT", 10000))


FEATURES = [
    "BHK", "Size", "Area Locality", "City",
    "Furnishing Status", "Tenant Preferred",
    "Bathroom", "Point of Contact",
    "CurrentFloor", "TotalFloors",
]

CATEGORICAL = [
    "Area Locality", "City", "Furnishing Status",
    "Tenant Preferred", "Point of Contact",
]

ml_models = {}


class RentRequest(BaseModel):
    BHK: int
    Size: float
    City: str
    Area_Locality: str = Field(alias="Area Locality")
    Furnishing_Status: str = Field(alias="Furnishing Status")
    Tenant_Preferred: str = Field(alias="Tenant Preferred")
    Bathroom: int
    Point_of_Contact: str = Field(alias="Point of Contact")
    CurrentFloor: float
    TotalFloors: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads the ML models into memory when the server starts."""
    try:
        with open(MODEL_PATH, "rb") as f:
            ml_models["model"] = pickle.load(f)
        logger.info("Model loaded from '%s'", MODEL_PATH)
    except FileNotFoundError:
        logger.error("Model file '%s' not found.", MODEL_PATH)
        ml_models["model"] = None

    try:
        with open(ENCODER_PATH, "rb") as f:
            ml_models["encoders"] = pickle.load(f)
        logger.info("Encoders loaded from '%s'", ENCODER_PATH)
    except FileNotFoundError:
        logger.error("Encoders file '%s' not found.", ENCODER_PATH)
        ml_models["encoders"] = None

    yield
    ml_models.clear()


app = FastAPI(
    title="RentIQ API",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health():
    """Health check endpoint for uptime monitors."""
    model_loaded = ml_models.get("model") is not None
    encoders_loaded = ml_models.get("encoders") is not None
    ready = model_loaded and encoders_loaded

    status_code = 200 if ready else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ok" if ready else "degraded",
            "model_loaded": model_loaded,
            "encoders_loaded": encoders_loaded,
            "version": "2.0.0"
        }
    )


@app.get("/ping")
async def ping():
    """Keep-alive ping endpoint."""
    return {"pong": True}


@app.post("/predict")
async def predict(req: RentRequest):
    """Predicts rent based on the incoming JSON data."""
    model = ml_models.get("model")
    encoders = ml_models.get("encoders")

    if not model or not encoders:
        raise HTTPException(status_code=503, detail="Model not ready. Check server logs.")

    try:
        t0 = time.perf_counter()

        data = req.model_dump(by_alias=True)
        df = pd.DataFrame([data])

        for col in CATEGORICAL:
            known = list(encoders[col].classes_)
            value = df[col].iloc[0]

            if value not in known:
                logger.warning("Unseen value '%s' for '%s'. Defaulting to '%s'.", value, col, known[0])
                df[col] = known[0]

            df[col] = encoders[col].transform(df[col])

        df = df[FEATURES]

        predicted_rent = float(model.predict(df)[0])
        latency_ms = (time.perf_counter() - t0) * 1000

        logger.info(
            "Prediction | city=%s | bhk=%d | size=%.0f sqft | rent=₹%.0f | latency=%.2fms",
            data.get("City"), data.get("BHK"), data.get("Size"),
            predicted_rent, latency_ms,
        )

        return {
            "predicted_rent": round(predicted_rent, 2),
            "latency_ms": round(latency_ms, 2)
        }

    except Exception as exc:
        logger.exception("Prediction failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(exc)}")


if __name__ == "__main__":
    logger.info("Starting RentIQ API on port %d", PORT)
    uvicorn.run(app, host="0.0.0.0", port=PORT)