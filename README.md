🌱 AI-Driven Crop Disease Prediction and Management System


✨ Project Overview
Welcome to the AI-Driven Crop Disease Prediction and Management System! This innovative Flask-based web application is designed to empower farmers and agricultural experts with intelligent, data-driven insights to optimize crop health and yield. By leveraging the power of machine learning and deep learning, our system provides crucial recommendations and predictions based on real-time data and user inputs.

🌟 Key Features
Our system offers a comprehensive suite of tools to support modern agriculture:

🌿 Crop Recommendation: Get personalized suggestions on the most suitable crop to grow in your farm, analyzing your soil parameters and local weather conditions.
🔬 Fertilizer Recommendation: Receive precise advice on the ideal fertilizer composition (N, P, K) to balance your soil's nutrient levels for optimal plant growth.
🍃 Plant Disease Detection: Swiftly identify potential plant diseases by simply uploading an image of an affected leaf. Our deep learning model provides instant diagnosis.
☀️ Real-time Weather Integration: Benefit from personalized suggestions, as the system integrates live temperature and humidity data via the OpenWeatherMap API.
🚀 Tech Stack
This project is built with a robust and modern technology stack:

Frontend:

HTML & CSS: Structured and styled using Jinja templates for dynamic content rendering.
Backend:

Python: The core logic is powered by Python.
Flask: A lightweight and flexible web framework for the application backend.
Machine Learning & Deep Learning:

Random Forest: Utilized for accurate crop recommendation, processing various soil and environmental features.
ResNet9 (CNN Architecture): Employed for sophisticated plant disease classification from images, ensuring high accuracy.
PyTorch: The primary deep learning framework for building and deploying the disease detection model.
NumPy, Pandas, PIL, Torchvision: Essential libraries for data manipulation, image processing, and model operations.
API Integration:

OpenWeatherMap API: Fetches real-time temperature and humidity data to enhance crop and fertilizer recommendations.
📁 Project Structure
project/
├── app.py                      # Main Flask application file
├── config.py                   # Configuration settings (e.g., API keys)
├── models/                     # Stores trained ML/DL models
│   ├── plant_disease_model.pth # PyTorch model for disease detection
│   └── RandomForest.pkl        # Scikit-learn model for crop recommendation
├── utils/                      # Helper scripts and modules
│   ├── disease.py              # Logic for disease prediction
│   ├── fertilizer.py           # Logic for fertilizer recommendation
│   └── model.py                # Functions for loading and interacting with ML models
├── templates/                  # HTML templates for web pages
│   ├── index.html              # Homepage
│   ├── crop.html               # Crop recommendation page
│   ├── fertilizer.html         # Fertilizer recommendation page
│   ├── disease.html            # Plant disease detection page
│   └── layout.html             # Base template for consistent UI
├── static/                     # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── Data/                       # Datasets used for training or reference
│   └── fertilizer.csv          # Example: Dataset for fertilizer recommendations
└── requirements.txt            # Python dependencies
⚙️ Setup Instructions
Follow these steps to get the application up and running on your local machine:

Clone the repository:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
(Remember to replace your-username/your-repo-name with the actual GitHub path to your project.)

Create a virtual environment:
It's recommended to use a virtual environment to manage dependencies.

Bash

python -m venv venv
Activate the virtual environment:

Windows:
Bash

.\venv\Scripts\activate
macOS / Linux:
Bash

source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
Set your OpenWeatherMap API key:

Obtain a free API key from OpenWeatherMap.
Open config.py and replace 'your_openweathermap_api_key' with your actual key:
Python

weather_api_key = 'YOUR_ACTUAL_OPENWEATHERMAP_API_KEY_HERE'
Run the application:

Bash

python app.py
Access the application:
Open your web browser and visit: http://127.0.0.1:5000

📸 Image Upload Guidelines (for Disease Detection)
To ensure accurate disease detection, please follow these guidelines when uploading images:

Clear Image: Upload a high-resolution, clear image of the plant leaf.
Supported Types: Only .jpg, .jpeg, and .png file types are supported.
Good Lighting: Ensure the leaf is well-lit, preferably with natural, even lighting.
Focus: The affected leaf should be in sharp focus.
No Clutter: Avoid background clutter that might distract the model.
Single Leaf (Ideally): If possible, focus on a single affected leaf rather than a cluster.
🧠 Models Used
1. Crop Recommendation Model
Algorithm: Random Forest Classifier
Key Features: Nitrogen (N), Phosphorous (P), Potassium (K), Temperature, Humidity, pH Level, and Rainfall.
Functionality: Predicts the most suitable crop based on the input soil and environmental parameters.
2. Disease Detection Model
Architecture: Convolutional Neural Network (CNN) - Specifically, a ResNet9 architecture.
Dataset: Trained extensively on the widely recognized PlantVillage Dataset.
Classes: Capable of classifying 38 distinct plant-disease categories, covering a wide range of common crop ailments.
Functionality: Analyzes uploaded leaf images to identify the presence and type of plant disease.
🖼️ Screenshots / Demo
(Self-correction: This is a crucial section for any attractive README. Since I can't generate images, I'm adding a placeholder here. You should add actual screenshots or a GIF/video link of your running application here!)

🤝 Contributing
We welcome contributions to enhance this project! If you'd like to contribute, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/YourFeatureName).
Make your changes and ensure they are well-documented.
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature/YourFeatureName).
Open a Pull Request.
## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgements
Thanks to the creators of the PlantVillage Dataset for providing the valuable data for disease classification.
Special thanks to the developers of Flask, PyTorch, and other open-source libraries that made this project possible.