# 🐾 Dangerous Animal Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-orange?style=for-the-badge)
![Gradio](https://img.shields.io/badge/Gradio-UI%20Framework-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A professional AI-powered application for real-time detection and analysis of dangerous wildlife.**

</div>

---

## 📖 Introduction

The **Dangerous Animal Detection System** is a cutting-edge deep learning application designed to identify potential wildlife threats in images. Built with **YOLOv8** and wrapped in a sleek **Gradio** interface, this tool not only detects animals but also provides comprehensive educational profiles, safety assessments, and population statistics. 

Whether for wildlife monitoring, safety awareness, or educational purposes, this application bridges the gap between raw data and actionable insights.

## ✨ Key Features

- **🔍 Precision Object Detection**: Utilizes a custom-trained YOLOv8 model (`best.pt`) to accurately identify specific animal species in uploaded images.
- **📊 Rich Information Profiles**: Instantly generates detailed cards for each detected animal, covering:
    - **Habitat & Background**: Where they live and their behavior.
    - **Safety Assessment**: Clear "Dangerous", "Caution", or "Safe" indicators.
    - **Ecological Impact**: their advantages and disadvantages in the ecosystem.
    - **Lifespan**: Average age in the wild.
- **📜 Session History**: Automatically tracks all detections in a session, allowing users to review past findings and export data to CSV.
- **🌏 Dynamic Analytics**: Visualizes population distribution data for detected species using interactive Matplotlib charts.
- **🎨 Modern Professional UI**: Features a polished, responsive design with custom CSS, intuitive navigation, and clear visual hierarchy.

## 🦁 Supported Animals

The system is currently trained to detect and analyze the following species:

| Predator / Potential Threat | Low Threat / Non-Aggressive |
|-----------------------------|-----------------------------|
| 🐊 **Alligator**            | 🦌 **Deer**                 |
| 🐻 **Bear**                 | 🦌 **Moose**                |
| 🐗 **Boar**                 | 🦊 **Fox**                  |
| 🐆 **Cougar**               | 🦝 **Raccoon**              |
| 🐺 **Coyote**               | 🦨 **Skunk**                |
| 🐍 **Snake**                |                             |
| 🐺 **Wolf**                 |                             |

## 🛠️ Tech Stack

- **Core Logic**: Python 3
- **ML Engine**: Ultralytics YOLOv8
- **Interface**: Gradio (Web UI)
- **Data Handling**: Pandas
- **Visualization**: Matplotlib
- **Image Processing**: PIL (Pillow), OpenCV

## 🚀 Installation & Setup

Follow these steps to deploy the application locally.

### Prerequisites

- Python 3.8 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/BuAli353/Dangerous_Animal_Detection.git
cd Dangerous_Animal_Detection
```

### 2. Create a Virtual Environment (Recommended)
```bash
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*Note: Ensure `best.pt` (the trained model weights) is present in the root directory. If not, you will need to place your trained YOLOv8 model file there.*

## 💻 Usage

Run the web application with a single command:

```bash
python app.py
```

The terminal will provide a local URL (usually `http://127.0.0.1:7860`). Open this link in your browser to interact with the application.

## 📂 Project Structure

```
Dangerous_Animal_Detection/
├── app.py                 # Main application source code
├── best.pt               # Trained YOLOv8 model weights
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git configuration
└── __pycache__/           # Compiled Python files
```

## 🔮 Future Roadmap

- [ ] **Real-time Video Analysis**: Extend detection capabilities to live video feeds.
- [ ] **Geospatial Mapping**: Plot detection locations on an interactive map.
- [ ] **Expanded Dataset**: Add more species to the detection model.
- [ ] **API Endpoint**: Expose the detection logic as a RESTful API.

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request if you have suggestions for improvements.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

**Bu Ali**
- GitHub: [@BuAli353](https://github.com/BuAli353)

---

<div align="center">
    <i>Developed with ❤️ for Wildlife Safety & Education</i>
</div>
<img width="1197" height="836" alt="Project_image (Edit)" src="https://github.com/user-attachments/assets/c8b171f8-3cd5-4468-b839-1abb4c027f7b" />

