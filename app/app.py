# Importing essential libraries and modules

from flask import Flask, render_template, request, Markup
import numpy as np
import pandas as pd
from utils.disease import disease_dic
from utils.fertilizer import fertilizer_dic
import requests
import config
import pickle
import io
import torch
from torchvision import transforms
from PIL import Image
from utils.model import ResNet9
import cv2
import os
import uuid
# ==============================================================================================

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Loading plant disease classification model

disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']


# ==============================================================================================

# -------------------------LOADING THE TRAINED MODELS -------------------------------------------
disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()

crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

# ==============================================================================================

def weather_fetch(city_name):
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    print(f"Weather API response: {x}")  # DEBUG LINE

    if x.get("cod") != 404 and "main" in x:
        y = x["main"]
        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None


# ===================== ENHANCED SEVERITY + VISUALIZATION LOGIC ================================

def estimate_severity(image):
    image = image.resize((256, 256))
    np_img = np.array(image)

    # Convert to HSV for better green segmentation
    hsv_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv_img, lower_green, upper_green)
    green_count = cv2.countNonZero(green_mask)
    total_pixels = np_img.shape[0] * np_img.shape[1]

    non_green_mask = cv2.bitwise_not(green_mask)
    red_mask = np.zeros_like(np_img)
    red_mask[:, :, 0] = non_green_mask  # Red overlay for diseased areas

    overlay = cv2.addWeighted(np_img, 1.0, red_mask, 0.5, 0)

    # Combine original and overlay side-by-side
    combined = np.hstack((np_img, overlay))

    # Save image
    filename = f"{uuid.uuid4().hex}.png"
    path = f"static/overlays/{filename}"
    os.makedirs("static/overlays", exist_ok=True)
    cv2.imwrite(path, combined[:, :, ::-1])  # RGB to BGR

    # Calculate severity
    non_green_ratio = 1 - (green_count / total_pixels)
    if non_green_ratio >= 0.5:
        severity = "High"
    elif non_green_ratio >= 0.25:
        severity = "Medium"
    else:
        severity = "Low"

    return severity, path

# ===================== PREDICTION & PLANT VALIDATION ============================================

def predict_image(img, model=disease_model):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img)).convert('RGB')
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    with torch.no_grad():
        output = model(img_u)
        probs = torch.softmax(output, dim=1)
        _, preds = torch.max(probs, dim=1)

    prediction = disease_classes[preds.item()]

    if "healthy" in prediction.lower():
        severity = "None"
        overlay_path = None
    else:
        severity, overlay_path = estimate_severity(image)

    return prediction, severity, overlay_path

def is_plant_image(img):
    """
    Placeholder: detect plant based on green area using HSV.
    To be replaced with CNN later.
    """
    image = Image.open(io.BytesIO(img)).convert('RGB').resize((64, 64))
    np_img = np.array(image)
    hsv = cv2.cvtColor(np_img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))
    green_ratio = np.sum(mask > 0) / (64 * 64)
    return green_ratio > 0.25

# ===============================================================================================

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/crop-recommend')
def crop_recommend():
    return render_template('crop.html', title='Crop Recommendation')

@app.route('/fertilizer')
def fertilizer_recommendation():
    return render_template('fertilizer.html', title='Fertilizer Suggestion')

@app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Crop Recommendation'
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['potassium'])
    ph = float(request.form['ph'])
    rainfall = float(request.form['rainfall'])
    city = request.form.get("city")
    weather_data = weather_fetch(city)
    if weather_data:
        temperature, humidity = weather_data
        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = crop_recommendation_model.predict(data)[0]
        return render_template('crop-result.html', prediction=prediction, title=title)
    else:
        return render_template('try_again.html', title=title)

@app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])
    df = pd.read_csv('Data/fertilizer.csv')
    nr, pr, kr = df[df['Crop'] == crop_name][['N', 'P', 'K']].iloc[0]

    diff = {abs(nr - N): "N", abs(pr - P): "P", abs(kr - K): "K"}
    nutrient_values = {
        "N": N, "P": P, "K": K,
        "Nr": nr, "Pr": pr, "Kr": kr
    }
    nutrient = diff[max(diff)]  # This gives "N", "P", or "K"

    # Compare actual vs required safely
    actual = nutrient_values[nutrient]
    required = nutrient_values[nutrient + "r"]

    key = f"{nutrient}{'High' if actual > required else 'low'}"

    recommendation = Markup(fertilizer_dic[key])
    return render_template('fertilizer-result.html', recommendation=recommendation, title='Fertilizer Suggestion')
@app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    title = 'Disease Detection'

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('disease.html', title=title)
        file = request.files.get('file')
        if not file:
            return render_template('disease.html', title=title)

        try:
            img = file.read()

            if not is_plant_image(img):
                return render_template('disease-result.html',
                                       prediction="⚠️ The uploaded image does not appear to be a plant. Please try again.",
                                       title=title)

            disease, severity, overlay_path = predict_image(img)
            description = disease_dic[disease]

            # Add CSS for styling directly in the HTML string
            styles = """
            <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #2c3e50;
                background-color: #f9f9f9;
                padding: 20px;
            }

            .disease-name {
                font-size: 36px;
                font-weight: 700;
                animation: fadeIn 1s ease-in-out;
                color: #2c3e50;
                margin-top: 20px;
                text-align: center;
            }

            .severity {
                font-size: 28px;
                font-weight: 600;
                animation: bounce 1s infinite alternate;
                margin-top: 10px;
                text-align: center;
            }
            .severity.High { color: red; }
            .severity.Medium { color: orange; }
            .severity.Low { color: green; }

            .section-title {
                font-weight: bold;
                font-size: 24px;
                margin-top: 30px;
                color: #34495e;
                text-align: center;
            }

            .description-text {
                margin-top: 10px;
                font-size: 18px;
                color: #2d3436;
                line-height: 1.8;
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
                text-align: justify;
            }

            .image-preview {
                margin-top: 30px;
                text-align: center;
            }
            .image-preview img {
                border: 3px solid #ccc;
                border-radius: 12px;
                width: 90%;
                max-width: 800px;
                margin-top: 10px;
            }
            .note {
                font-size: 14px;
                color: #7f8c8d;
                margin-top: 5px;
            }

            @keyframes bounce {
                from { transform: scale(1); }
                to { transform: scale(1.05); }
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .severity-bar-container {
            margin-top: 20px;
            text-align: center;
            }

            .bar-label {
            font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 8px;
            }
            
            .progress-bar {
                width: 60%;
                height: 30px;
                background-color: #ecf0f1;
                border-radius: 20px;
                margin: 0 auto;
                overflow: hidden;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
            }
            
            .progress-fill {
                height: 100%;
                text-align: center;
                line-height: 30px;
                color: white;
                font-weight: bold;
                border-radius: 20px;
                transition: width 0.8s ease-in-out;
            }
            
            .progress-fill.Low {
                background-color: #2ecc71;
            }
            .progress-fill.Medium {
                background-color: #f39c12;
            }
            .progress-fill.High {
                background-color: #e74c3c;
            }

            </style>
            """

            # Extract cause and cure if your description is multi-line or structured (optional)
            description_html = f"<div class='section-title'>Description:</div><div class='description-text'>{description}</div>"

            # Construct the full HTML output
            severity_percent = {"Low": 33, "Medium": 66, "High": 100}[severity]

            progress_bar_html = f"""
            <div class='severity-bar-container'>
                <div class='bar-label'>Severity Level</div>
                <div class='progress-bar'>
                    <div class='progress-fill {severity}' style='width: {severity_percent}%'>
                        {severity_percent}%
                    </div>
                </div>
            </div>
            """

            description_html = f"<div class='section-title'>Description:</div><div class='description-text'>{description}</div>"

            full_output = f"""
            {styles}
            <div class='disease-name'>🦠 Disease: {disease}</div>
            <div class='severity {severity}'>⚠️ Severity: {severity}</div>
            {progress_bar_html}
            {description_html}
            """

            if overlay_path:
                full_output += f"""
                <div class='section-title'>Affected Area Visualization:</div>
                <div class='image-preview'>
                    <img src='/{overlay_path}' alt='Affected Area Visualization'>
                    <div class='note'>(Left: Original, Right: Affected Area)</div>
                </div>"""

            return render_template('disease-result.html', prediction=Markup(full_output), title=title)

        except Exception as e:
            print(f"[ERROR] Disease Prediction Failed: {e}")
            return render_template('disease-result.html',
                                   prediction="⚠️ Something went wrong during prediction. Please try again.",
                                   title=title)

    return render_template('disease.html', title=title)

# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=False)
