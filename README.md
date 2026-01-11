# 🗳️ ONOE Voter Hub: One Nation One Election

**A neutral, data-driven educational platform designed to explain the "One Nation One Election" policy proposal in India.**

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Prototype-green?style=for-the-badge)

## 📖 Overview

The **ONOE Voter Hub** is a web application built to demystify the "One Nation One Election" proposal. It provides a comprehensive, interactive interface for voters to understand the potential impact of synchronizing Lok Sabha and State Assembly elections. 

The app features bilingual support (English & Hindi), financial simulations, myth-busting resources, and a knowledge quiz, making complex policy data accessible to the general public.

---

## ✨ Key Features

### 1. 🏠 **Educational Explainer**
   - **Bilingual Support:** Complete toggle between **English** and **Hindi**.
   - **Pros & Cons:** Balanced presentation of arguments (Cost Efficiency vs. Federalism concerns).
   - **Key Metrics:** Visualizes voter statistics and key policy definitions.

### 2. 📊 **Policy Impact Simulator**
   - **Interactive Modeling:** Users can adjust election frequency (1-5 years) and projected voter turnout.
   - **Cost Analysis:** Calculates estimated financial savings based on representative ECI data.
   - **Visualizations:** Generates dynamic bar charts comparing current costs vs. ONOE costs.
   - **Excel Export:** Download simulation results as an `.xlsx` report.

### 3. 🛡️ **Myth Buster**
   - **Searchable Database:** Instantly find facts to counter common myths (e.g., regarding EVMs, Federal Structure).
   - **Verified Sources:** All facts are backed by citations from the Law Commission, ECI, and NITI Aayog.
   - **Misinformation Reporting:** A prototype interface for users to upload screenshots of fake news.

### 4. 🧠 **Voter Quiz**
   - **Gamified Learning:** A 10-question interactive quiz to test policy knowledge.
   - **Instant Feedback:** Provides explanations and sources for every answer.
   - **Scoring System:** Tracks progress and offers a final score assessment.

---

## 🛠️ Tech Stack

- **Frontend/Backend:** [Streamlit](https://streamlit.io/) (Python)
- **Data Manipulation:** Pandas, NumPy
- **Visualization:** Matplotlib
- **I/O:** BytesIO (for Excel file handling)

---

## 🚀 Installation & Setup

Follow these steps to run the application locally.

### Prerequisites
Ensure you have **Python 3.7+** installed.

### 1. Clone the Repository

### 2. Create a Virtual Environment (Optional but Recommended)

### 3. Install Dependencies
You need `streamlit`, `pandas`, `matplotlib`, and `openpyxl` (for Excel export).

### 4. Run the Application
The app will open automatically in your default web browser at `http://localhost:8501`.

---

## 📂 Project Structure

onoe-voter-hub
│
├── app.py # Main application entry point
├── requirements.txt # List of dependencies
└── README.md # Project documentation

---

## 📸 Usage Guide

1. **Select Language:** Use the sidebar radio button to switch between English and Hindi.
2. **Navigate:** Choose a module (Simulator, Myth Buster, Quiz) from the sidebar menu.
3. **Simulate:** Go to the "Impact Simulator," select a state (e.g., Uttar Pradesh), and adjust the sliders to see how ONOE affects costs.
4. **Download:** Click "Download Report" in the simulator to save your findings.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 Disclaimer & Credits

- **Data Source:** This application uses **representative mock data** based on public reports (ECI, Law Commission, NITI Aayog) for educational simulation purposes. It is not an official government tool.
- **Developed By:** Team TECHVISION
- **Helpline:** Voter Helpline Toll Free Number - 1950

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.


