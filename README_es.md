# 🔍 DOC 3D Profile Inspector

*Read this in other languages: [English](README.md)*

**DOC 3D Profile Inspector** es una herramienta profesional de escritorio diseñada para analizar y comparar archivos de impresión 3D `.3mf` (como los descargados de MakerWorld o Printables) con tus perfiles locales de **Snapmaker Orca / Orca Slicer**.

Cuando importas un archivo `.3mf`, muchos ajustes personalizados del creador original (alturas de capa, número de muros, patrones de relleno, soportes) se pierden o son sobreescritos por tus perfiles predeterminados. Esta app soluciona ese problema resolviendo todo el árbol de herencia y mostrándote exactamente qué debes ajustar.

---

## ✨ Características Principales

* 🧠 **Resolución de Herencia Slicer:** Rastrea automáticamente los parámetros hasta los ajustes base de "fábrica", asegurando que veas las diferencias reales.
* 🎯 **Autodetección de Material:** Analiza los metadatos del `.3mf` y preselecciona el mejor perfil de filamento de tu biblioteca local.
* 📊 **Vista de Datos por Pestañas:** Tablas compactas y organizadas agrupadas por categorías (Calidad, Resistencia, Soportes, Velocidad, etc.).
* 🛡️ **Filtro Inteligente:** Por defecto, oculta el "ruido" (G-code interno y parámetros del sistema) para centrarse en lo que realmente afecta a la calidad de impresión.
* ⭐ **Sistema de Favoritos:** Marca con una estrella tus perfiles de Impresora, Proceso y Filamento más usados para mantenerlos siempre arriba.
* 🌍 **Localización Instantánea:** Detecta el idioma del sistema automáticamente (Soporta Español, Inglés, Francés, Alemán y Chino).
* 🔍 **Buscador en Desplegables:** Filtrado en tiempo real al escribir para encontrar el perfil adecuado en segundos.

---

## 🚀 Guía de Instalación (Paso a Paso)

### 🍎 Para usuarios de Mac (macOS)
1.  **Descarga:** Haz clic en el botón verde **Code** y selecciona **Download ZIP**. Descomprímelo en tu Escritorio.
2.  **Instala Python:** Descarga la última versión desde [python.org](https://www.python.org/downloads/macos/) y ejecuta el instalador.
3.  **Configura la Librería:** Abre la **Terminal** (Cmd + Espacio, escribe "Terminal") y ejecuta:
    ```bash
    pip3 install customtkinter
    ```
4.  **Inicia:** En la terminal, entra en la carpeta e inicia la app:
    ```bash
    cd Desktop/DOC-3D-Profile-Inspector-main
    python3 app.py
    ```

### 🪟 Para usuarios de Windows
1.  **Descarga:** Haz clic en el botón verde **Code** y selecciona **Download ZIP**. Descomprime la carpeta.
2.  **Instala Python:** Descarga la última versión desde [python.org](https://www.python.org/downloads/windows/).  
    ⚠️ **IMPORTANTE:** Marca la casilla **"Add Python to PATH"** al inicio de la instalación.
3.  **Configura la Librería:** Abre el **Símbolo del Sistema** (Tecla Win, escribe "cmd") y ejecuta:
    ```cmd
    pip install customtkinter
    ```
4.  **Inicia:** Haz doble clic en `app.py` o ejecútalo desde la consola:
    ```cmd
    python app.py
    ```

---

## 🛠️ ¿Cómo se usa?
1.  **Construye tu Perfil:** Selecciona tu Impresora, Proceso (Calidad) y Filamento en el panel izquierdo.
2.  **Carga el .3MF:** Haz clic en "Seleccionar archivo .3MF" y elige tu modelo descargado.
3.  **Analiza:** Pulsa el botón gigante de **ANALIZAR CAMBIOS**.
4.  **Revisa y Aplica:** Mira los valores naranjas en las pestañas. Abre tu Slicer y ajusta esos parámetros a mano para obtener la impresión perfecta.

---

## 📄 Licencia
Este proyecto está bajo la **Licencia MIT**

---
*Creado para la comunidad de Impresión 3D por Dakros66
