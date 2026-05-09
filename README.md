# 🔍 DOC 3D Profile Inspector

*Read this in other languages: [Español](README_es.md)*

**DOC 3D Profile Inspector** is a professional desktop tool designed to analyze and compare `.3mf` 3D printing files (like those from MakerWorld or Printables) with your local **Snapmaker Orca / Orca Slicer** profiles.

When you import a `.3mf` file, many custom settings from the original creator (layer heights, wall counts, infill patterns, supports) are often lost or overwritten by your default profiles. This app solves that by resolving the full inheritance tree and showing you exactly what needs to be adjusted.

---

## ✨ Key Features

* 🧠 **Slicer Inheritance Resolution:** Automatically traces back parameters to the base "factory" settings, ensuring you see the real differences.
* 🎯 **Smart Material Auto-Detection:** Analyzes the `.3mf` metadata and pre-selects the best matching filament profile from your local library.
* 📊 **Tabbed Data View:** Organized, compact tables grouped by category (Quality, Strength, Supports, Speed, etc.).
* 🛡️ **Smart Filter:** By default, it hides noise (internal G-code and system parameters) to focus on what actually affects your print quality.
* ⭐ **Favorites System:** "Star" your most-used Machine, Process, and Filament profiles to keep them at the top of the list.
* 🌍 **Instant Localization:** Automatically detects system language (Supports English, Spanish, French, German, and Chinese).
* 🔍 **Searchable Dropdowns:** Real-time filtering in select menus to find the right profile in seconds.

---

## 🚀 Installation Guide (Step-by-Step)

### 🍎 For Mac Users (macOS)
1.  **Download:** Click the green **Code** button and select **Download ZIP**. Extract it to your Desktop.
2.  **Install Python:** Download the latest version from [python.org](https://www.python.org/downloads/macos/) and run the installer.
3.  **Setup Library:** Open the **Terminal** (Cmd + Space, type "Terminal") and run:
    ```bash
    pip3 install customtkinter
    ```
4.  **Launch:** In the terminal, enter the folder and start the app:
    ```bash
    cd Desktop/DOC-3D-Profile-Inspector-main
    python3 app.py
    ```

### 🪟 For Windows Users
1.  **Download:** Click the green **Code** button and select **Download ZIP**. Extract the folder.
2.  **Install Python:** Download the latest version from [python.org](https://www.python.org/downloads/windows/).  
    ⚠️ **IMPORTANT:** Check the box **"Add Python to PATH"** at the start of the installation.
3.  **Setup Library:** Open the **Command Prompt** (Press Win key, type "cmd") and run:
    ```cmd
    pip install customtkinter
    ```
4.  **Launch:** Double-click `app.py` or run via command prompt:
    ```cmd
    python app.py
    ```

---

## 🛠️ How to use it?
1.  **Build your Profile:** Select your Printer, Process (Quality), and Filament in the left panel.
2.  **Load the .3MF:** Click "Select .3MF file" and choose your downloaded model.
3.  **Analyze:** Hit the giant **ANALYZE CHANGES** button.
4.  **Review & Apply:** Check the tabs for orange values. Open your Slicer and manually match those settings to get the perfect print.

---

## 📄 License
This project is licensed under the **MIT License** 

---
*Created for the 3D Printing community by Dakros66 *
