# 🏠 RentIQ: Metro City Rent Predictor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=flat-square&logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-3.1-FF6600?style=flat-square&logo=xgboost&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)

**An AI-powered web application that predicts house rents across India's 6 major metro cities in real time.**

[🚀 Live Demo](https://nilotpaldhar2004.github.io/Indian-city-rent-predictor/) · [API Backend](https://indian-city-rent-predictor.onrender.com) · [Report a Bug](https://github.com/nilotpaldhar2004/Indian-city-rent-predictor/issues)

</div>

---

## 📸 Preview

> Submit a property's details — BHK, size, city, locality, furnishing — and receive an AI-predicted rent estimate instantly, along with a ±10% confidence band and a full feature importance breakdown.

---

## 🌐 Deployment & Architecture

This project uses a split-hosting architecture optimized for free-tier performance:

* **Backend API:** FastAPI application hosted on [Render](https://render.com).
* **Frontend Dashboard:** Static web UI served via [GitHub Pages](https://pages.github.com).
* **Keep-Alive Automation:** Scheduled GitHub Actions workflow pinging `/ping` every 10 minutes to eliminate Render cold starts.

---

## ✨ Features

- **Real-Time Predictions** — Sub-10ms inference with a tuned XGBoost model served via FastAPI.
- **6 Metro Cities** — Mumbai, Delhi, Bangalore, Chennai, Hyderabad, and Kolkata.
- **Explainable AI** — Built-in Chart.js visualization showing each feature's learned importance weight.
- **Confidence Band** — Includes a ±10% low/high range estimate for every prediction.
- **Uptime Monitoring** — Dedicated `/ping` keep-alive endpoint.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Machine Learning** | Python, Pandas, Scikit-Learn, XGBoost, Optuna |
| **Backend API** | FastAPI, Uvicorn, Pydantic (v2) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Chart.js |
| **Deployment/DevOps**| Render (API), GitHub Pages (Frontend), GitHub Actions |

---

## 📂 Project Structure

```
Indian-city-rent-predictor/
│
├── app.py                                      # FastAPI backend server
├── index.html                                  # Frontend web interface
├── indian-metropolitan-city-rent-prediction.ipynb  # Model training notebook
├── requirements.txt                            # Python dependencies
├── xgboost_rent_model.pkl                      # Trained XGBoost model file
├── label_encoders.pkl                          # Scikit-Learn label encoders
├── LICENSE                                     # MIT License
├── .gitignore                                  # Git ignore rules
└── README.md                                   # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/nilotpaldhar2004/Indian-city-rent-predictor.git
cd Indian-city-rent-predictor
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Verify model files

Ensure `xgboost_rent_model.pkl` and `label_encoders.pkl` are present in the project root directory alongside `app.py`.

### 4. Start the server

```bash
python app.py
```

The API starts on `http://localhost:10000`. Open that URL in your browser — it serves `index.html` directly.

---

## 🌐 Deployment Setup

| Component | Host | URL |
|---|---|---|
| Frontend (`index.html`) | GitHub Pages | `https://nilotpaldhar2004.github.io/Indian-city-rent-predictor/` |
| Backend (`app.py`) | Render | `https://indian-city-rent-predictor.onrender.com` |

### Deploy the backend to Render

1. Push your repository to GitHub (ensuring `.pkl` model files are committed)
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repository
4. Set **Start Command** to `python app.py` (or `uvicorn app:app --host 0.0.0.0 --port $PORT`)
5. Set **Environment** to `Python 3`
6. Deploy — Render provides a public URL

### Deploy the frontend to GitHub Pages

1. In your GitHub repository, go to **Settings → Pages**
2. Set **Source** to the `main` branch, root `/`
3. Save — GitHub Pages automatically serves `index.html`

---

## 📡 API Reference

### `GET /health`

Returns the current status of the model and encoders.

```json
{
  "status": "ok",
  "model_loaded": true,
  "encoders_loaded": true,
  "version": "2.0.0"
}
```

### `GET /ping`

Keep-alive endpoint used by automated pingers.

```json
{ "pong": true }
```

### `POST /predict`

Accepts a JSON body and returns the predicted monthly rent.

**Request body:**

```json
{
  "BHK": 2,
  "Size": 1000,
  "City": "Bangalore",
  "Area Locality": "Koramangala",
  "Furnishing Status": "Semi-Furnished",
  "Tenant Preferred": "Bachelors/Family",
  "Bathroom": 2,
  "Point of Contact": "Contact Owner",
  "CurrentFloor": 3,
  "TotalFloors": 10
}
```

**Response:**

```json
{
  "predicted_rent": 28500.0,
  "latency_ms": 4.21
}
```

Interactive API documentation is available at `/docs` (Swagger UI) when the server is running.

---

## 🤖 Model Details

| Property | Value |
|---|---|
| Algorithm | XGBoost (Gradient Boosted Trees) |
| Hyperparameter Tuning | Optuna (Bayesian optimization) |
| Training Data | Indian housing listings across 6 metro cities |
| Features | 10 (BHK, Size, City, Area Locality, Furnishing Status, Tenant Preferred, Bathroom, Point of Contact, Current Floor, Total Floors) |
| Categorical Encoding | Scikit-Learn Label Encoding |

**Feature importance (model-learned weights):**

| Feature | Impact |
|---|---|
| Point of Contact | 27.5% |
| Size (Sq. Ft.) | 18.5% |
| Total Floors | 10.8% |
| City | 10.6% |
| Bathroom | 10.4% |
| BHK | 7.5% |
| Area Locality | 6.5% |
| Current Floor | 3.5% |
| Furnishing Status | 2.5% |
| Tenant Preferred | 1.5% |

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Nilotpal Dhar**

- GitHub: [@nilotpaldhar2004](https://github.com/nilotpaldhar2004)

---

<div align="center">
  <sub>Built with Python, FastAPI, and XGBoost · Deployed on Render + GitHub Pages</sub>
</div>