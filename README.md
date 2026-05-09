# 🔍 DOC 3D Profile Inspector

*Read this in other languages: [Español](README_es.md)*

**DOC 3D Profile Inspector** is a desktop tool designed to analyze and compare `.3mf` 3D printing files (like those downloaded from MakerWorld) with your local **Snapmaker Orca / Orca Slicer** profiles. 

Have you ever imported an amazing model only to lose all the creator's secret slicing configurations (layer heights, infill types, supports)? This app reads the file, searches your local profiles, resolves the Slicer's inheritance tree, and tells you **exactly which parameters you need to change** to print the part just as its creator intended.

---

## ✨ Key Features

* 🧠 **Slicer Inheritance Resolution:** It doesn't just read your `.json` files; it understands how Orca Slicer inherits base parameters directly from the software's internal source code.
* 🎯 **Smart Auto-Detection:** Automatically selects the appropriate material profile based on the imported `.3mf` metadata.
* 📊 **Tabbed Interface:** Forget about endless text lists. Results are neatly grouped into visual tables by category (Strength, Quality, Supports, etc.).
* 🛡️ **"Human" Filter:** By default, it hides hundreds of internal and useless G-Code parameters, showing you only the vital settings (layers, perimeters, densities).
* ⭐ **Favorites System:** Bookmark your most-used machine, process, and filament profiles to have them always one click away.
* 🌍 **Multilanguage:** Automatically detects your operating system's language (Supports English, Spanish, French, German, and Chinese).

---

## 🚀 Installation Guide (For Beginners)

Don't worry if you've never used Python! Follow these step-by-step instructions based on your operating system.

### 🍎 For Mac Users (macOS)

1. **Download the code:** Click the green `<> Code` button at the top and select **"Download ZIP"**. Extract the folder to your desktop.
2. **Install Python:** Your Mac usually comes with Python, but to ensure you have the right version, download the installer from [python.org](https://www.python.org/downloads/macos/) and install it.
3. **Open the Terminal:** Press `Cmd + Space`, type `Terminal`, and hit Enter.
4. **Install the GUI library:** In the terminal, copy, paste, and run this command:
   ```bash
   pip3 install customtkinter
