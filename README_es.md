# 🔍 DOC 3D Profile Inspector

**DOC 3D Profile Inspector** es una herramienta de escritorio diseñada para analizar y comparar archivos de impresión 3D `.3mf` (como los descargados de MakerWorld) con tus perfiles locales de **Snapmaker Orca / Orca Slicer**. 

¿Alguna vez has importado un modelo increíble y al laminarlo se pierden todas las configuraciones secretas del creador (alturas de capa, tipo de relleno, soportes)? Esta app lee el archivo, busca en tus perfiles locales, resuelve el árbol de herencia del Slicer y te dice **exactamente qué parámetros debes cambiar** para imprimir la pieza tal y como la ideó su creador.

---

## ✨ Características Principales

* 🧠 **Resolución de Herencia Slicer:** No solo lee tus archivos `.json`, sino que entiende cómo Orca Slicer hereda los parámetros base desde el código interno del programa.
* 🎯 **Autodetección Inteligente:** Selecciona automáticamente el material adecuado en base a los metadatos del archivo `.3mf` importado.
* 📊 **Interfaz por Pestañas:** Olvídate de listas de texto interminables. Los resultados se agrupan en tablas visuales por categorías (Fuerza, Calidad, Soportes, etc.).
* 🛡️ **Filtro para "Humanos":** Por defecto, oculta los cientos de parámetros internos y de G-Code inútiles para mostrarte solo los ajustes vitales (capas, perímetros, densidades).
* ⭐ **Sistema de Favoritos:** Guarda tus perfiles de máquina, proceso y filamento más usados para tenerlos siempre a un clic.
* 🌍 **Multilenguaje:** Detecta el idioma de tu sistema operativo automáticamente (Soporte para Español, Inglés, Francés, Alemán y Chino).

---

## 🚀 Guía de Instalación (Para Principiantes)

¡No te preocupes si nunca has usado Python! Sigue estas instrucciones paso a paso según tu sistema operativo.

### 🍎 Para usuarios de Mac (macOS)

1. **Descarga el código:** Haz clic en el botón verde `<> Code` de arriba y selecciona **"Download ZIP"**. Descomprime la carpeta en tu escritorio.
2. **Instala Python:** Tu Mac ya suele traer Python, pero para asegurarnos de tener la versión correcta, descarga el instalador desde [python.org](https://www.python.org/downloads/macos/) e instálalo.
3. **Abre la Terminal:** Pulsa `Cmd + Espacio`, escribe `Terminal` y dale a Enter.
4. **Instala la librería gráfica:** En la terminal, copia, pega y ejecuta este comando:
   ```bash
   pip3 install customtkinter
