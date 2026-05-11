import customtkinter as ctk
from tkinter import filedialog, messagebox
import zipfile
import json
import os
import platform
import locale
import webbrowser
import re
import xml.etree.ElementTree as ET
import posixpath
from pathlib import Path

# --- CONFIGURACIÓN DE VERSIÓN ---
APP_VERSION = "v1.1.0"
GITHUB_URL = "https://github.com/Dakros66/DOC-3D-Profile-Inspector"

# --- CONSTANTES DEL CONVERSOR (De tu app.py original) ---
TARGET_FILAMENTS = 4
DEFAULT_FILAMENT_PROFILE = 'Snapmaker PLA SnapSpeed @U1'
FILAMENT_PROFILES_FILE = 'filament_types.3mf'

# --- CONFIGURACIÓN DE ESTILO ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

SNAPMAKER_TEAL = "#00A396"
SNAPMAKER_TEAL_HOVER = "#00857A"
BG_MAIN = "#18181B"      
BG_SIDEBAR = "#27272A"   
BG_CARD = "#3F3F46"      
BG_ROW_ALT = "#323238"   
TEXT_MUTED = "#A1A1AA"   
TEXT_MAIN = "#FAFAFA"    
ACCENT_ORANGE = "#FACC15"

# --- DICCIONARIO DE IDIOMAS ---
TRANSLATIONS = {
    "en": {
        "title": "DOC 3D\nPROFILE INSPECTOR",
        "step1": "1. BUILD YOUR PROFILE",
        "printer": "⚙️ Printer",
        "process": "📏 Process (Quality)",
        "filament": "🧵 Filament",
        "step2": "2. MAKERWORLD FILE",
        "btn_load": "Select .3MF file",
        "plate": "Select Plate",
        "filter": "Basic Filter (Hide Advanced)",
        "btn_analyze": "ANALYZE CHANGES",
        "btn_export": "Export to TXT",
        "status_wait": "Waiting for files...",
        "status_3mf_ok": "✅ 3MF loaded",
        "status_auto_mat": "🎯 Mat. auto-selected: {}",
        "res_title": "Project Details",
        "res_welcome": "Welcome. Build your profile and load a .3mf to start.",
        "res_no_diff": "✅ No differences detected.",
        "res_no_basic": "No critical basic changes.\nDisable 'Basic Filter' to see advanced settings.",
        "res_showing": "Showing {} differences",
        "info_print": "⏱️ Time: {} | ⚖️ Weight: {}",
        "cat_quality": "✨ Quality",
        "cat_strength": "💪 Strength",
        "cat_support": "🚧 Supports",
        "cat_adhesion": "🧲 Adhesion",
        "cat_material": "🔥 Material/Cooling",
        "cat_speed": "⚡ Speed",
        "cat_advanced": "⚙️ Advanced",
        "col_param": "Parameter to change",
        "col_mw": "Value in .3MF",
        "col_u1": "Your U1 (Base)",
        "not_found": "Not found",
        "inherited": "Inherited from Slicer",
        "internal_base": "Internal base value",
        "err_load_3mf": "Error processing 3MF:\n{}",
        "warn_load_first": "Please load a .3mf file first.",
        "all_perfect": "All perfect",
        "no_changes": "No changes detected",
        "tag_user": "[USER]",
        "tag_system": "[SYSTEM]",
        "export_success": "Report exported successfully!",
        "tooltip_default": "Hover over a parameter to see its description here.",
        "tooltip_advanced_desc": "Technical parameter. Usually left as inherited unless specific calibration is needed.",
        "attention": "Attention",
        "error": "Error",
        "export_title": "Export",
        "default_plate": "Default Plate",
        "plate_num": "Plate {}",
        "mac_paths_note": "* Auto-paths fully tested on macOS",
        "txt_report_title": "=== DOC 3D PROFILE INSPECTOR REPORT ===",
        "txt_plate": "Plate",
        "txt_printer": "Printer",
        "txt_process": "Process",
        "txt_filament": "Filament",
        "txt_change_to": "- Change TO (MakerWorld):",
        "txt_current": "- Current (Your U1):",
        "txt_none": "None",
        "not_sliced": "Not Sliced",
        "tab_inspector": "🔍 Inspector",
        "tab_converter": "🛠️ U1 Converter",
        "conv_title": "Smart Conversion to Snapmaker U1",
        "conv_desc": "1. Bambu Lab critical settings will be wiped.\n2. Snapmaker U1 Master Template will be injected.\n3. Checked parameters will be kept from original creator.",
        "conv_btn": "💾 Generate Adapted .3MF",
        "conv_success": "Adapted .3mf generated successfully!",
        "conv_filaments": "Detected AMS Filaments (Auto-mapping to Extruders 1-4):",
        "conv_no_filaments": "No filaments detected. Load a .3mf file."
    },
    "es": {
        "title": "DOC 3D\nPROFILE INSPECTOR",
        "step1": "1. CONSTRUYE TU PERFIL",
        "printer": "⚙️ Impresora",
        "process": "📏 Proceso (Calidad)",
        "filament": "🧵 Filamento",
        "step2": "2. ARCHIVO MAKERWORLD",
        "btn_load": "Seleccionar .3MF",
        "plate": "Seleccionar Placa",
        "filter": "Filtro Básico (Ocultar Avanzados)",
        "btn_analyze": "ANALIZAR CAMBIOS",
        "btn_export": "Exportar a TXT",
        "status_wait": "Esperando archivos...",
        "status_3mf_ok": "✅ Archivo 3MF cargado",
        "status_auto_mat": "🎯 Mat. auto-seleccionado: {}",
        "res_title": "Detalles del Proyecto",
        "res_welcome": "Bienvenido. Construye tu perfil y carga un .3mf para empezar.",
        "res_no_diff": "✅ No hay diferencias detectadas.",
        "res_no_basic": "No hay cambios básicos vitales.\nDesactiva el 'Filtro Básico' para ver ajustes internos.",
        "res_showing": "Mostrando {} diferencias",
        "info_print": "⏱️ Tiempo: {} | ⚖️ Peso: {}",
        "cat_quality": "✨ Calidad",
        "cat_strength": "💪 Resistencia",
        "cat_support": "🚧 Soportes",
        "cat_adhesion": "🧲 Adherencia",
        "cat_material": "🔥 Material/Viento",
        "cat_speed": "⚡ Velocidad",
        "cat_advanced": "⚙️ Avanzado",
        "col_param": "Parámetro a cambiar",
        "col_mw": "Valor en el .3MF",
        "col_u1": "Tu U1 (Base)",
        "not_found": "No encontrados",
        "inherited": "Heredado del Slicer",
        "internal_base": "Valor base interno",
        "err_load_3mf": "Error al procesar 3MF:\n{}",
        "warn_load_first": "Por favor, carga primero un archivo .3mf.",
        "all_perfect": "Todo perfecto",
        "no_changes": "Sin cambios",
        "tag_user": "[USUARIO]",
        "tag_system": "[SISTEMA]",
        "export_success": "¡Reporte exportado con éxito!",
        "tooltip_default": "Pasa el ratón sobre un parámetro para ver su descripción aquí.",
        "tooltip_advanced_desc": "Parámetro técnico. Normalmente se mantiene heredado salvo que requiera calibración específica.",
        "attention": "Atención",
        "error": "Error",
        "export_title": "Exportar",
        "default_plate": "Placa Única",
        "plate_num": "Placa {}",
        "mac_paths_note": "* Rutas automáticas testeadas en macOS",
        "txt_report_title": "=== REPORTE DE DOC 3D PROFILE INSPECTOR ===",
        "txt_plate": "Placa",
        "txt_printer": "Impresora",
        "txt_process": "Proceso",
        "txt_filament": "Filamento",
        "txt_change_to": "- Cambiar A (MakerWorld):",
        "txt_current": "- Actual (Tu U1):",
        "txt_none": "Ninguno",
        "not_sliced": "Sin Laminar",
        "tab_inspector": "🔍 Inspector",
        "tab_converter": "🛠️ Conversor U1",
        "conv_title": "Conversión Inteligente a Snapmaker U1",
        "conv_desc": "1. Los ajustes críticos de Bambu Lab serán eliminados.\n2. Se inyectará la Plantilla Maestra de Snapmaker U1.\n3. Los parámetros marcados se conservarán del creador original.",
        "conv_btn": "💾 Generar .3MF Adaptado",
        "conv_success": "¡Archivo .3mf adaptado generado con éxito!",
        "conv_filaments": "Filamentos AMS Detectados (Mapeo a Extrusores 1-4):",
        "conv_no_filaments": "Carga un archivo .3mf para ver los filamentos."
    }
}

TOOLTIPS = {
    "layer_height": {"es": "Altura de cada capa. Menor valor = más detalle pero más tiempo de impresión.", "en": "Height of each layer. Lower value = more detail but longer print time."},
    "wall_loops": {"es": "Número de perímetros o paredes exteriores. Aumentarlo mejora la resistencia.", "en": "Number of outer wall loops. Increasing it improves part strength."},
    "sparse_infill_density": {"es": "Porcentaje de relleno interior de la pieza.", "en": "Percentage of internal infill density."},
    "sparse_infill_pattern": {"es": "Forma geométrica del relleno interior (Giroide, Rejilla, etc).", "en": "Geometric pattern of the internal infill (Gyroid, Grid, etc)."},
    "support_type": {"es": "Tipo de soporte (Normal o Árbol).", "en": "Type of support structures (Normal or Tree)."},
    "brim_type": {"es": "Borde de adherencia a la cama. Útil para evitar warping (que se levanten las esquinas).", "en": "Bed adhesion brim. Useful to prevent warping at the corners."},
    "top_shell_layers": {"es": "Número de capas sólidas en la parte superior de la pieza.", "en": "Number of solid layers on the top of the print."},
    "bottom_shell_layers": {"es": "Número de capas sólidas en la base de la pieza.", "en": "Number of solid layers at the bottom of the print."},
    "seam_position": {"es": "Posición de la costura (donde empieza y acaba cada capa).", "en": "Seam position (where each layer starts and ends)."},
    "ironing_type": {"es": "Alisado. La boquilla plancha la última capa para un acabado liso.", "en": "Ironing. The nozzle irons the top surface for a smooth finish."}
}

CONVERTER_PARAMS = {
    "quality": ["layer_height", "initial_layer_height", "seam_position", "ironing_type", "ironing_flow", "ironing_speed", "wall_generator", "elefant_foot_compensation", "precision"],
    "strength": ["wall_loops", "top_shell_layers", "bottom_shell_layers", "sparse_infill_density", "sparse_infill_pattern", "infill_combination", "infill_wall_overlap"],
    "support": ["enable_support", "support_type", "support_style", "support_top_z_distance", "support_bottom_z_distance", "support_interface_layers", "support_interface_spacing", "support_expansion"],
    "adhesion": ["brim_type", "brim_width", "draft_shield"],
    "temperature": ["nozzle_temperature", "nozzle_temperature_initial_layer", "hot_plate_temp", "hot_plate_temp_initial_layer", "temperature_vitrification", "chamber_temperature"]
}

LANG_MAP = {"English": "en", "Español": "es"}
INV_LANG_MAP = {v: k for k, v in LANG_MAP.items()}


class ProfessionalCompareApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Iniciar sin generar warnings de locale depreciado
        self.current_lang = self.detect_system_language()
        
        self.title(f"DOC 3D Profile Inspector - {APP_VERSION}")
        self.geometry("1450x900")
        
        # Color del panel definido de forma segura
        self.configure(fg_color=BG_MAIN)
        self.minsize(1200, 800)

        self.valores_base_orca = {
            "sparse_infill_density": "15%", "sparse_infill_pattern": "grid", "wall_loops": "2",
            "top_shell_layers": "3", "bottom_shell_layers": "3", "layer_height": "0.2",
            "initial_layer_height": "0.2", "seam_position": "aligned", "seam_gap": "15%",
            "elefant_foot_compensation": "0", "support_type": "normal(auto)", "support_style": "default",
            "brim_type": "outer_only", "brim_width": "5", "ironing_type": "no_ironing",
            "print_sequence": "by_layer", "default_acceleration": "10000", "travel_speed": "500",
            "enable_support": "0", "draft_shield": "disabled", "wall_generator": "arachne",
            "reduce_infill_retraction": "1"
        }

        self.placas_data = {}     
        self.info_placas = {}
        self.ruta_3mf_actual = None
        self.detected_filaments = []
        self.available_filaments = self.load_filament_profiles()

        self.perfiles_dict = {"machine": {}, "process": {}, "filament": {}}
        self.diccionario_rutas_global = {}
        self.diferencias_actuales = []
        
        self.archivo_favoritos = os.path.join(Path.home(), ".doc3d_inspector_favs.json")
        self.favoritos = self.cargar_favoritos()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=440) 
        self.grid_columnconfigure(1, weight=1)

        self.buscar_perfiles_automaticamente()
        self.crear_sidebar()
        self.crear_panel_principal()

    def T(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

    def detect_system_language(self):
        try:
            # Solución del Deprecation Warning
            loc = locale.getlocale()[0]
            if not loc:
                loc = os.environ.get('LANG', 'en')
            if loc and loc[:2].lower() in TRANSLATIONS: 
                return loc[:2].lower()
        except: pass
        return 'en' 

    def change_language(self, selected_language_name):
        self.current_lang = LANG_MAP[selected_language_name]
        self.retranslate_ui()

    def get_tooltip(self, param_name):
        base_name = param_name.split('.')[-1].lower()
        if base_name in TOOLTIPS:
            return TOOLTIPS[base_name].get(self.current_lang, TOOLTIPS[base_name].get("en"))
        return f"{self.T('cat_advanced')} ({base_name}) - {self.T('tooltip_advanced_desc')}"

    # --- LÓGICA DE CARGA DE FILAMENTOS ---
    def load_filament_profiles(self):
        filaments = []
        try:
            if os.path.exists(FILAMENT_PROFILES_FILE):
                with zipfile.ZipFile(FILAMENT_PROFILES_FILE, 'r') as z:
                    settings = json.loads(z.read('Metadata/project_settings.config').decode('utf-8'))
                    for t, sid in zip(settings.get('filament_type', []), settings.get('filament_settings_id', [])):
                        filaments.append({'type': t, 'settings_id': sid})
        except: pass
        if not filaments:
            filaments = [
                {'type': 'PLA',  'settings_id': DEFAULT_FILAMENT_PROFILE},
                {'type': 'PETG', 'settings_id': 'Snapmaker PETG HF'},
                {'type': 'ABS',  'settings_id': 'Generic ABS'},
                {'type': 'TPU',  'settings_id': 'Generic TPU'},
            ]
        return filaments

    def normalize_color(self, color: str) -> str:
        if not color: return '#000000'
        c = color.lstrip('#')
        if len(c) == 8: c = c[:6]
        if len(c) != 6: return '#000000'
        try: int(c, 16)
        except ValueError: return '#000000'
        return f'#{c.upper()}'

    def parse_bambu_filaments(self, filepath: str) -> list[dict]:
        filaments = []
        try:
            with zipfile.ZipFile(filepath, 'r') as z:
                names = z.namelist()
                if 'Metadata/slice_info.config' in names:
                    xml_str = z.read('Metadata/slice_info.config').decode('utf-8')
                    if "<?xml" in xml_str or "<config>" in xml_str:
                        root = ET.fromstring(xml_str)
                        for fil in root.findall('.//filament'):
                            filaments.append({
                                'id':    fil.get('id'),
                                'color': self.normalize_color(fil.get('color', '')),
                                'type':  fil.get('type') or 'PLA',
                            })
                if not filaments and 'Metadata/project_settings.config' in names:
                    cfg = json.loads(z.read('Metadata/project_settings.config').decode('utf-8'))
                    colors = cfg.get('filament_colour', [])
                    types  = cfg.get('filament_type', [])
                    for i, color in enumerate(colors):
                        filaments.append({
                            'id':    str(i + 1),
                            'color': self.normalize_color(color),
                            'type':  types[i] if i < len(types) else 'PLA',
                        })
        except: pass
        return filaments

    def autodetectar_material(self):
        placa_actual = self.dd_plates.get()
        if not placa_actual or placa_actual not in self.placas_data: return
        mw_plano = self.aplanar_diccionario(self.placas_data[placa_actual])
        material_detectado = None
        for clave, valor in mw_plano.items():
            if 'filament_type' in clave:
                if isinstance(valor, list) and len(valor) > 0: material_detectado = str(valor[0]).upper()
                elif isinstance(valor, str): material_detectado = valor.upper()
                break
        if material_detectado:
            opciones = self.dd_filamento.cget("values")
            coincidencias = [opcion for opcion in opciones if material_detectado in opcion.upper()]
            if coincidencias:
                coincidencia = next((opc for opc in coincidencias if "SNAPMAKER" in opc.upper()), coincidencias[0])
                self.dd_filamento.set(coincidencia)
                self.actualizar_estado_boton_fav(coincidencia, "filament", self.btn_fav_fil)
                self.lbl_status.configure(text=self.T("status_auto_mat").format(material_detectado))

    # --- UI Y TRADUCCIONES ---
    def retranslate_ui(self):
        self.logo_label.configure(text=self.T("title"))
        self.lbl_step1.configure(text=self.T("step1"))
        self.lbl_printer.configure(text=self.T("printer"))
        self.lbl_process.configure(text=self.T("process"))
        self.lbl_filament.configure(text=self.T("filament"))
        self.lbl_step2.configure(text=self.T("step2"))
        self.btn_load_3mf.configure(text=self.T("btn_load"))
        self.lbl_plate.configure(text=self.T("plate"))
        self.switch_filtro.configure(text=self.T("filter"))
        self.btn_analyze.configure(text=self.T("btn_analyze"))
        self.btn_export.configure(text=self.T("btn_export"))
        self.lbl_tooltip.configure(text=self.T("tooltip_default"))
        self.lbl_note.configure(text=self.T("mac_paths_note"))
        
        if self.placas_data: self.lbl_status.configure(text=self.T("status_3mf_ok"))
        else: self.lbl_status.configure(text=self.T("status_wait"))

        for tipo, dd in [("machine", self.dd_maquina), ("process", self.dd_proceso), ("filament", self.dd_filamento)]:
            sel = dd.get()
            dd.configure(values=self.get_sorted_keys(tipo))
            if sel in ["No encontrados", "Not found"]: dd.set(self.T("not_found"))

        self.main_tabview._segmented_button._buttons_dict[self.T("tab_inspector")].configure(text=self.T("tab_inspector"))
        self.main_tabview._segmented_button._buttons_dict[self.T("tab_converter")].configure(text=self.T("tab_converter"))

        if self.diferencias_actuales: self.renderizar_resultados()
        else:
            self.header_label.configure(text=self.T("res_title"))
            self.render_empty_state(self.T("res_welcome"))

    def abrir_github(self): webbrowser.open(GITHUB_URL)

    def valores_son_iguales(self, val1, val2):
        v1 = str(val1).strip().lower()
        v2 = str(val2).strip().lower()
        if v1 == v2: return True
        bool_map = {"true": "1", "false": "0", "on": "1", "off": "0", "yes": "1", "no": "0"}
        if bool_map.get(v1, v1) == bool_map.get(v2, v2): return True
        _v1 = v1.replace("%", "")
        _v2 = v2.replace("%", "")
        try:
            if float(_v1) == float(_v2): return True
        except: pass
        return False

    def cargar_favoritos(self):
        if os.path.exists(self.archivo_favoritos):
            try:
                with open(self.archivo_favoritos, 'r') as f: return json.load(f)
            except: pass
        return {"machine": [], "process": [], "filament": []}

    def guardar_favoritos(self):
        try:
            with open(self.archivo_favoritos, 'w') as f: json.dump(self.favoritos, f)
        except: pass

    def toggle_fav(self, tipo, combobox, btn):
        seleccion_actual = combobox.get().replace("⭐ ", "")
        if not seleccion_actual or seleccion_actual == self.T("not_found"): return
        ruta_vinculada = self.encontrar_ruta_por_nombre(seleccion_actual, tipo)
        if not ruta_vinculada: return
        if ruta_vinculada in self.favoritos[tipo]:
            self.favoritos[tipo].remove(ruta_vinculada)
            btn.configure(text="☆", text_color=TEXT_MUTED)
        else:
            self.favoritos[tipo].append(ruta_vinculada)
            btn.configure(text="⭐", text_color=ACCENT_ORANGE)
        self.guardar_favoritos()
        nueva_lista = self.get_sorted_keys(tipo)
        combobox.configure(values=nueva_lista)
        nuevo_texto = f"⭐ {seleccion_actual}" if ruta_vinculada in self.favoritos[tipo] else seleccion_actual
        combobox.set(nuevo_texto)

    def actualizar_estado_boton_fav(self, choice, tipo, btn):
        clean_choice = choice.replace("⭐ ", "")
        ruta_vinculada = self.encontrar_ruta_por_nombre(clean_choice, tipo)
        if ruta_vinculada and ruta_vinculada in self.favoritos[tipo]: btn.configure(text="⭐", text_color=ACCENT_ORANGE)
        else: btn.configure(text="☆", text_color=TEXT_MUTED)

    def encontrar_ruta_por_nombre(self, nombre_mostrado, tipo):
        for original, ruta in self.perfiles_dict[tipo].items():
            limpio_orig = original.replace("[USER]", "").replace("[SYSTEM]", "").strip()
            limpio_most = nombre_mostrado.replace(self.T("tag_user"), "").replace(self.T("tag_system"), "").strip()
            if limpio_orig == limpio_most: return ruta
        return None

    def buscar_perfiles_automaticamente(self):
        home = str(Path.home())
        rutas_a_escanear = []
        if platform.system() == "Darwin":
            rutas_a_escanear = [
                os.path.join(home, "Library/Application Support/Snapmaker_Orca/system/Snapmaker"),
                os.path.join(home, "Library/Application Support/Snapmaker_Orca/user/default"),
                "/Applications/Snapmaker Orca.app/Contents/Resources/profiles",
                "/Applications/OrcaSlicer.app/Contents/Resources/profiles"
            ]
        else:
            appdata = os.getenv('APPDATA', '')
            prog_files = os.environ.get("PROGRAMFILES", "C:\\Program Files")
            prog_files86 = os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")
            rutas_a_escanear = [
                os.path.join(appdata, "Snapmaker_Orca/system/Snapmaker"),
                os.path.join(appdata, "Snapmaker_Orca/user/default"),
                os.path.join(appdata, "OrcaSlicer/user/default"),
                os.path.join(prog_files, "Snapmaker Orca/resources/profiles"),
                os.path.join(prog_files, "OrcaSlicer/resources/profiles"),
                os.path.join(prog_files86, "Snapmaker Orca/resources/profiles"),
                "D:\\Program Files\\Snapmaker Orca\\resources\\profiles",
                "D:\\Program Files\\OrcaSlicer\\resources\\profiles"
            ]
        
        for ruta_base in rutas_a_escanear:
            if os.path.exists(ruta_base):
                for root, dirs, files in os.walk(ruta_base):
                    for file in files:
                        if file.endswith('.json'):
                            ruta_absoluta = os.path.join(root, file)
                            nombre_sin_ext = file.replace('.json', '')
                            self.diccionario_rutas_global[nombre_sin_ext] = ruta_absoluta
                            try:
                                with open(ruta_absoluta, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                    tipo = data.get("type", "unknown")
                                    if tipo in ["machine", "process", "filament"] and not nombre_sin_ext.startswith("fdm_"):
                                        nombre_original = data.get("name", nombre_sin_ext)
                                        categoria = "[USER]" if "user/default" in root else "[SYSTEM]"
                                        nombre_interno = f"{categoria} {nombre_original}"
                                        self.perfiles_dict[tipo][nombre_interno] = ruta_absoluta
                            except: pass 

    def get_sorted_keys(self, tipo):
        nombres_internos = list(self.perfiles_dict[tipo].keys())
        nombres_mostrados = []
        for n in nombres_internos:
            ruta = self.perfiles_dict[tipo][n]
            n_traducido = n.replace("[USER]", self.T("tag_user")).replace("[SYSTEM]", self.T("tag_system"))
            nombres_mostrados.append((n_traducido, ruta))

        favs = sorted([n for n, r in nombres_mostrados if r in self.favoritos[tipo]])
        usuarios = sorted([n for n, r in nombres_mostrados if self.T("tag_user") in n and r not in self.favoritos[tipo]])
        sistemas = sorted([n for n, r in nombres_mostrados if self.T("tag_system") in n and r not in self.favoritos[tipo]])
        
        resultado = [f"⭐ {f}" for f in favs] + usuarios + sistemas
        return resultado if resultado else [self.T("not_found")]

    def filtrar_combobox(self, event, combobox, tipo):
        texto = combobox.get().lower().replace("⭐ ", "")
        lista_completa = self.get_sorted_keys(tipo)
        filtrados = [x for x in lista_completa if texto in x.lower()]
        combobox.configure(values=filtrados)

    # --- ESTRUCTURA DE INTERFAZ ---
    def crear_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_SIDEBAR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=self.T("title"), font=ctk.CTkFont(size=26, weight="bold"), text_color=SNAPMAKER_TEAL)
        self.logo_label.grid(row=0, column=0, padx=30, pady=(30, 20))

        self.lbl_step1 = ctk.CTkLabel(self.sidebar_frame, text=self.T("step1"), font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_step1.grid(row=1, column=0, padx=30, pady=(5, 5), sticky="w")
        
        # MÁQUINA
        self.lbl_printer = ctk.CTkLabel(self.sidebar_frame, text=self.T("printer"), font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_printer.grid(row=2, column=0, padx=30, pady=(5, 0), sticky="w")
        frm_maq = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        frm_maq.grid(row=3, column=0, padx=30, pady=(2, 5), sticky="ew")
        self.dd_maquina = ctk.CTkComboBox(frm_maq, values=self.get_sorted_keys("machine"), fg_color=BG_CARD, border_color=BG_CARD, button_color=SNAPMAKER_TEAL, button_hover_color=SNAPMAKER_TEAL_HOVER, height=40, command=lambda c: self.actualizar_estado_boton_fav(c, "machine", self.btn_fav_maq))
        self.dd_maquina.pack(side="left", fill="x", expand=True)
        self.dd_maquina._entry.bind("<KeyRelease>", lambda e: self.filtrar_combobox(e, self.dd_maquina, "machine"))
        self.btn_fav_maq = ctk.CTkButton(frm_maq, text="☆", width=40, height=40, fg_color=BG_CARD, hover_color="#4F4F56", text_color=TEXT_MUTED, font=ctk.CTkFont(size=18), command=lambda: self.toggle_fav("machine", self.dd_maquina, self.btn_fav_maq))
        self.btn_fav_maq.pack(side="right", padx=(5, 0))

        # PROCESO
        self.lbl_process = ctk.CTkLabel(self.sidebar_frame, text=self.T("process"), font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_process.grid(row=4, column=0, padx=30, pady=(5, 0), sticky="w")
        frm_pro = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        frm_pro.grid(row=5, column=0, padx=30, pady=(2, 5), sticky="ew")
        self.dd_proceso = ctk.CTkComboBox(frm_pro, values=self.get_sorted_keys("process"), fg_color=BG_CARD, border_color=BG_CARD, button_color=SNAPMAKER_TEAL, button_hover_color=SNAPMAKER_TEAL_HOVER, height=40, command=lambda c: self.actualizar_estado_boton_fav(c, "process", self.btn_fav_pro))
        self.dd_proceso.pack(side="left", fill="x", expand=True)
        self.dd_proceso._entry.bind("<KeyRelease>", lambda e: self.filtrar_combobox(e, self.dd_proceso, "process"))
        self.btn_fav_pro = ctk.CTkButton(frm_pro, text="☆", width=40, height=40, fg_color=BG_CARD, hover_color="#4F4F56", text_color=TEXT_MUTED, font=ctk.CTkFont(size=18), command=lambda: self.toggle_fav("process", self.dd_proceso, self.btn_fav_pro))
        self.btn_fav_pro.pack(side="right", padx=(5, 0))

        # FILAMENTO
        self.lbl_filament = ctk.CTkLabel(self.sidebar_frame, text=self.T("filament"), font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_filament.grid(row=6, column=0, padx=30, pady=(5, 0), sticky="w")
        frm_fil = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        frm_fil.grid(row=7, column=0, padx=30, pady=(2, 20), sticky="ew")
        self.dd_filamento = ctk.CTkComboBox(frm_fil, values=self.get_sorted_keys("filament"), fg_color=BG_CARD, border_color=BG_CARD, button_color=SNAPMAKER_TEAL, button_hover_color=SNAPMAKER_TEAL_HOVER, height=40, command=lambda c: self.actualizar_estado_boton_fav(c, "filament", self.btn_fav_fil))
        self.dd_filamento.pack(side="left", fill="x", expand=True)
        self.dd_filamento._entry.bind("<KeyRelease>", lambda e: self.filtrar_combobox(e, self.dd_filamento, "filament"))
        self.btn_fav_fil = ctk.CTkButton(frm_fil, text="☆", width=40, height=40, fg_color=BG_CARD, hover_color="#4F4F56", text_color=TEXT_MUTED, font=ctk.CTkFont(size=18), command=lambda: self.toggle_fav("filament", self.dd_filamento, self.btn_fav_fil))
        self.btn_fav_fil.pack(side="right", padx=(5, 0))

        if self.dd_maquina.get(): self.actualizar_estado_boton_fav(self.dd_maquina.get(), "machine", self.btn_fav_maq)
        if self.dd_proceso.get(): self.actualizar_estado_boton_fav(self.dd_proceso.get(), "process", self.btn_fav_pro)
        if self.dd_filamento.get(): self.actualizar_estado_boton_fav(self.dd_filamento.get(), "filament", self.btn_fav_fil)

        # CARGA DE ARCHIVO
        self.lbl_step2 = ctk.CTkLabel(self.sidebar_frame, text=self.T("step2"), font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_step2.grid(row=8, column=0, padx=30, pady=(10, 8), sticky="w")
        
        self.btn_load_3mf = ctk.CTkButton(self.sidebar_frame, text=self.T("btn_load"), command=self.cargar_3mf, fg_color="transparent", border_width=2, border_color=SNAPMAKER_TEAL, text_color=TEXT_MAIN, hover_color=BG_CARD, height=45, font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_load_3mf.grid(row=9, column=0, padx=30, pady=(0, 10), sticky="ew")

        self.lbl_plate = ctk.CTkLabel(self.sidebar_frame, text=self.T("plate"), font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_plate.grid(row=10, column=0, padx=30, pady=(5, 0), sticky="w")
        self.dd_plates = ctk.CTkOptionMenu(self.sidebar_frame, values=["---"], fg_color=BG_CARD, button_color=SNAPMAKER_TEAL, button_hover_color=SNAPMAKER_TEAL_HOVER, dynamic_resizing=False, command=self.cambiar_placa)
        self.dd_plates.grid(row=11, column=0, padx=30, pady=(0, 20), sticky="ew")

        self.switch_filtro = ctk.CTkSwitch(self.sidebar_frame, text=self.T("filter"), command=self.renderizar_resultados, progress_color=SNAPMAKER_TEAL, font=ctk.CTkFont(size=14, weight="bold"))
        self.switch_filtro.grid(row=12, column=0, padx=30, pady=(0, 20), sticky="w")
        self.switch_filtro.select()

        self.btn_analyze = ctk.CTkButton(self.sidebar_frame, text=self.T("btn_analyze"), command=self.ejecutar_comparacion, fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER, height=60, font=ctk.CTkFont(size=18, weight="bold"))
        self.btn_analyze.grid(row=13, column=0, padx=30, pady=10, sticky="ew")

        self.lbl_status = ctk.CTkLabel(self.sidebar_frame, text=self.T("status_wait"), font=ctk.CTkFont(size=13), text_color=TEXT_MUTED)
        self.lbl_status.grid(row=14, column=0, padx=30, pady=10)

        # FOOTER
        self.sidebar_frame.grid_rowconfigure(15, weight=1) 
        self.footer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.footer_frame.grid(row=16, column=0, padx=30, pady=20, sticky="ew")
        self.lbl_note = ctk.CTkLabel(self.footer_frame, text=self.T("mac_paths_note"), font=ctk.CTkFont(size=10, slant="italic"), text_color=TEXT_MUTED)
        self.lbl_note.pack(side="top", pady=(0,5))
        self.lbl_version = ctk.CTkLabel(self.footer_frame, text=APP_VERSION, font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_version.pack(side="left")
        self.btn_github = ctk.CTkButton(self.footer_frame, text="GitHub ↗", width=70, height=28, fg_color=BG_CARD, hover_color="#4F4F56", font=ctk.CTkFont(size=12, weight="bold"), command=self.abrir_github)
        self.btn_github.pack(side="right")

    def crear_panel_principal(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_frame.grid_rowconfigure(2, weight=1) 
        self.main_frame.grid_columnconfigure(0, weight=1)

        # HEADER GLOBAL
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_label = ctk.CTkLabel(self.header_frame, text=self.T("res_title"), font=ctk.CTkFont(size=28, weight="bold"))
        self.header_label.pack(side="left")
        self.lang_menu = ctk.CTkOptionMenu(self.header_frame, values=list(LANG_MAP.keys()), command=self.change_language, width=120, fg_color=BG_CARD, button_color=BG_CARD, button_hover_color="#4F4F56")
        self.lang_menu.set(INV_LANG_MAP[self.current_lang])
        self.lang_menu.pack(side="right")

        self.btn_export = ctk.CTkButton(self.header_frame, text=self.T("btn_export"), command=self.exportar_txt, fg_color="transparent", border_width=1, text_color=TEXT_MUTED, hover_color=BG_CARD, width=120)
        self.btn_export.pack(side="right", padx=15)

        # BARRA INFO PLACA
        self.info_bar = ctk.CTkFrame(self.main_frame, fg_color=BG_SIDEBAR, height=40, corner_radius=8)
        self.info_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.info_bar.pack_propagate(False)
        self.lbl_info_print = ctk.CTkLabel(self.info_bar, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color=SNAPMAKER_TEAL)
        self.lbl_info_print.pack(side="left", padx=20)

        # PESTAÑAS PRINCIPALES
        self.main_tabview = ctk.CTkTabview(self.main_frame, fg_color="transparent", segmented_button_selected_color=SNAPMAKER_TEAL, segmented_button_selected_hover_color=SNAPMAKER_TEAL_HOVER)
        self.main_tabview.grid(row=2, column=0, sticky="nsew")
        
        tab_insp = self.main_tabview.add(self.T("tab_inspector"))
        tab_conv = self.main_tabview.add(self.T("tab_converter"))

        # --- PESTAÑA 1: INSPECTOR ---
        tab_insp.grid_rowconfigure(0, weight=1)
        tab_insp.grid_columnconfigure(0, weight=1)
        
        self.content_container = ctk.CTkFrame(tab_insp, fg_color=BG_SIDEBAR, corner_radius=12)
        self.content_container.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.tooltip_frame = ctk.CTkFrame(tab_insp, fg_color=BG_CARD, height=40, corner_radius=8)
        self.tooltip_frame.grid(row=1, column=0, sticky="ew")
        self.tooltip_frame.pack_propagate(False)
        self.lbl_tooltip = ctk.CTkLabel(self.tooltip_frame, text=self.T("tooltip_default"), font=ctk.CTkFont(size=13, slant="italic"), text_color=TEXT_MAIN)
        self.lbl_tooltip.pack(side="left", padx=20)

        # --- PESTAÑA 2: CONVERSOR ---
        tab_conv.grid_columnconfigure(0, weight=1)
        tab_conv.grid_rowconfigure(0, weight=1)
        
        conv_scroll = ctk.CTkScrollableFrame(tab_conv, fg_color="transparent")
        conv_scroll.grid(row=0, column=0, sticky="nsew")
        
        conv_card = ctk.CTkFrame(conv_scroll, fg_color=BG_SIDEBAR, corner_radius=12)
        conv_card.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(conv_card, text=self.T("conv_title"), font=ctk.CTkFont(size=22, weight="bold"), text_color=SNAPMAKER_TEAL).pack(pady=(30, 10))
        ctk.CTkLabel(conv_card, text=self.T("conv_desc"), font=ctk.CTkFont(size=14), text_color=TEXT_MUTED, wraplength=700, justify="center").pack(pady=(0, 20), padx=40)

        self.filaments_container = ctk.CTkFrame(conv_card, fg_color=BG_CARD, corner_radius=8)
        self.filaments_container.pack(fill="x", padx=40, pady=10)
        self.lbl_filaments_title = ctk.CTkLabel(self.filaments_container, text=self.T("conv_no_filaments"), font=ctk.CTkFont(weight="bold"))
        self.lbl_filaments_title.pack(pady=10)
        self.filaments_list_frame = ctk.CTkFrame(self.filaments_container, fg_color="transparent")
        self.filaments_list_frame.pack(pady=(0, 10))

        checks_frame = ctk.CTkFrame(conv_card, fg_color="transparent")
        checks_frame.pack(pady=20)

        self.chk_quality = ctk.CTkCheckBox(checks_frame, text=self.T("cat_quality"), font=ctk.CTkFont(size=16, weight="bold"), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_quality.grid(row=0, column=0, padx=30, pady=15, sticky="w")
        self.chk_quality.select()

        self.chk_strength = ctk.CTkCheckBox(checks_frame, text=self.T("cat_strength"), font=ctk.CTkFont(size=16, weight="bold"), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_strength.grid(row=0, column=1, padx=30, pady=15, sticky="w")
        self.chk_strength.select()

        self.chk_support = ctk.CTkCheckBox(checks_frame, text=self.T("cat_support"), font=ctk.CTkFont(size=16, weight="bold"), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_support.grid(row=1, column=0, padx=30, pady=15, sticky="w")
        self.chk_support.select()

        self.chk_adhesion = ctk.CTkCheckBox(checks_frame, text=self.T("cat_adhesion"), font=ctk.CTkFont(size=16, weight="bold"), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_adhesion.grid(row=1, column=1, padx=30, pady=15, sticky="w")
        self.chk_adhesion.select()

        self.chk_temp = ctk.CTkCheckBox(checks_frame, text=self.T("cat_material"), font=ctk.CTkFont(size=16, weight="bold"), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_temp.grid(row=2, column=0, columnspan=2, pady=15)
        
        self.btn_convert = ctk.CTkButton(conv_card, text=self.T("conv_btn"), command=self.exportar_3mf_adaptado, fg_color=ACCENT_ORANGE, text_color=BG_MAIN, hover_color="#EAB308", height=50, font=ctk.CTkFont(size=16, weight="bold"))
        self.btn_convert.pack(pady=40)

        self.render_empty_state(self.T("res_welcome"))

    def render_empty_state(self, msg):
        for w in self.content_container.winfo_children(): w.destroy()
        lbl = ctk.CTkLabel(self.content_container, text=msg, text_color=TEXT_MUTED, font=ctk.CTkFont(size=16))
        lbl.pack(expand=True)

    def set_tooltip(self, event, text):
        self.lbl_tooltip.configure(text=text, text_color=ACCENT_ORANGE)

    def clear_tooltip(self, event):
        self.lbl_tooltip.configure(text=self.T("tooltip_default"), text_color=TEXT_MAIN)

    def actualizar_ui_filamentos(self):
        for w in self.filaments_list_frame.winfo_children(): w.destroy()
        if not self.detected_filaments:
            self.lbl_filaments_title.configure(text=self.T("conv_no_filaments"))
            return
        self.lbl_filaments_title.configure(text=self.T("conv_filaments"))
        for i, fil in enumerate(self.detected_filaments[:TARGET_FILAMENTS]):
            row = ctk.CTkFrame(self.filaments_list_frame, fg_color="transparent")
            row.pack(pady=5, fill="x")
            color_box = ctk.CTkFrame(row, fg_color=fil['color'], width=24, height=24, corner_radius=4)
            color_box.pack(side="left", padx=(0, 15))
            ctk.CTkLabel(row, text=f"Extruder {i+1}: {fil['type']}", font=ctk.CTkFont(weight="bold")).pack(side="left")

    def cargar_3mf(self):
        ruta = filedialog.askopenfilename(filetypes=[("3MF", "*.3mf")])
        if ruta:
            try:
                self.ruta_3mf_actual = ruta
                self.extraer_datos_3mf(ruta)
                self.btn_load_3mf.configure(text=f"✓ {os.path.basename(ruta)[:20]}...")
                self.lbl_status.configure(text=self.T("status_3mf_ok"))
                
                self.detected_filaments = self.parse_bambu_filaments(ruta)
                self.actualizar_ui_filamentos()

                if self.info_placas:
                    nombres_placas = list(self.info_placas.keys())
                    self.dd_plates.configure(values=nombres_placas)
                    self.dd_plates.set(nombres_placas[0])
                    self.cambiar_placa(nombres_placas[0])
                    self.autodetectar_material()
            except Exception as e: messagebox.showerror(self.T("error"), self.T("err_load_3mf").format(e))

    def _parse_time_weight(self, data_dict):
        t_sec = data_dict.get("prediction", data_dict.get("print_time", data_dict.get("estimated_time", "")))
        w_g = 0
        if "filament_weights" in data_dict and isinstance(data_dict["filament_weights"], list):
            w_g = sum(float(x) for x in data_dict["filament_weights"] if x)
        elif "filament_weight" in data_dict and isinstance(data_dict["filament_weight"], str) and "," in data_dict["filament_weight"]:
            w_g = sum(float(x) for x in data_dict["filament_weight"].split(",") if x.strip())
        else:
            val = data_dict.get("weight", data_dict.get("filament_weight", data_dict.get("cost", "")))
            try: w_g = float(val) if val else 0
            except: w_g = 0
        try:
            t_sec = float(t_sec)
            if t_sec <= 0: raise ValueError
            h, r = divmod(t_sec, 3600)
            m, _ = divmod(r, 60)
            t_str = f"{int(h)}h {int(m)}m" if h > 0 else f"{int(m)}m"
        except: t_str = self.T("not_sliced")
        try:
            if w_g <= 0: raise ValueError
            w_str = f"{float(w_g):.1f}g"
        except: w_str = self.T("not_sliced")
        return t_str, w_str

    def extraer_datos_3mf(self, ruta_3mf):
        self.placas_data = {}
        self.info_placas = {}
        datos_globales = {}
        plate_catalog = {} 

        with zipfile.ZipFile(ruta_3mf, 'r') as z:
            for name in z.namelist():
                if ("Metadata/" in name or "Config/" in name) and (name.endswith('.json') or name.endswith('.config')):
                    if "plate_" in name or "slice_info" in name: continue
                    try: datos_globales.update(json.loads(z.read(name).decode('utf-8', errors='ignore')))
                    except: pass
            
            for name in z.namelist():
                if "slice_info" in name:
                    try:
                        content = z.read(name).decode('utf-8', errors='ignore')
                        if "<?xml" in content or "<config>" in content or "<plate" in content:
                            plates_xml = re.findall(r'<plate\b[^>]*>(.*?)</plate>', content, re.DOTALL)
                            for p_xml in plates_xml:
                                metas = re.findall(r'<metadata\s+key="([^"]+)"\s+value="([^"]*)"', p_xml)
                                p_data = {k: v for k, v in metas}
                                p_id = p_data.get('plater_id', p_data.get('plate_index', p_data.get('index', '')))
                                p_name = p_data.get('plater_name', p_data.get('plate_name', p_data.get('name', '')))
                                if not p_name: p_name = self.T("plate_num").format(p_id)
                                if p_id:
                                    plate_catalog[str(p_id)] = p_name
                                    t, w = self._parse_time_weight(p_data)
                                    self.info_placas[p_name] = {"time": t, "weight": w}
                        else:
                            info = json.loads(content)
                            p_list = info.get("plate_info", [])
                            if not p_list:
                                for k, v in info.items():
                                    if isinstance(v, dict) and "plate_info" in v:
                                        p_list = v["plate_info"]
                                        break
                            for p in p_list:
                                p_id = str(p.get("plate_index", p.get("plate", p.get("plater_id", ""))))
                                p_name = p.get("plate_name", p.get("plater_name", ""))
                                if p_id: 
                                    if not p_name: p_name = self.T("plate_num").format(p_id)
                                    plate_catalog[str(p_id)] = p_name
                                    t, w = self._parse_time_weight(p)
                                    self.info_placas[p_name] = {"time": t, "weight": w}
                    except: pass
                    break 

            for name in z.namelist():
                match = re.search(r'plate_(\d+)', name)
                if match:
                    p_id = str(match.group(1))
                    if p_id not in plate_catalog:
                        plate_catalog[p_id] = self.T("plate_num").format(p_id)

            if plate_catalog:
                for p_id in sorted(plate_catalog.keys(), key=lambda x: int(x) if x.isdigit() else x):
                    p_name = plate_catalog[p_id]
                    p_data = {}
                    posibles_nombres = [f"Metadata/plate_{p_id}.json", f"Config/plate_{p_id}.json", f"plate_{p_id}.json"]
                    for fname in posibles_nombres:
                        if fname in z.namelist():
                            try:
                                p_data = json.loads(z.read(fname).decode('utf-8', errors='ignore'))
                                break
                            except: pass
                    placa_final = datos_globales.copy()
                    placa_final.update(p_data)
                    unique_name = p_name
                    if unique_name in self.placas_data: unique_name = f"{p_name} ({p_id})"
                    self.placas_data[unique_name] = placa_final
                    if unique_name not in self.info_placas:
                        self.info_placas[unique_name] = {"time": self.T("not_sliced"), "weight": self.T("not_sliced")}
            else:
                self.placas_data[self.T("default_plate")] = datos_globales
                self.info_placas[self.T("default_plate")] = {"time": self.T("not_sliced"), "weight": self.T("not_sliced")}

    def cambiar_placa(self, nombre_placa):
        info = self.info_placas.get(nombre_placa, {"time": self.T("not_sliced"), "weight": self.T("not_sliced")})
        self.lbl_info_print.configure(text=self.T("info_print").format(info["time"], info["weight"]))
        if self.diferencias_actuales: self.ejecutar_comparacion()

    def aplanar_diccionario(self, d, prefix=''):
        items = {}
        for k, v in d.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict): items.update(self.aplanar_diccionario(v, new_key))
            else: items[new_key] = v
        return items

    def cargar_json_con_herencia(self, ruta_archivo, visitados=None):
        if visitados is None: visitados = set()
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f: data = json.load(f)
        except: return {}

        perfil_combinado = {}
        if "inherits" in data:
            padre = data["inherits"]
            if padre not in visitados:
                visitados.add(padre)
                ruta_padre = self.diccionario_rutas_global.get(padre)
                if ruta_padre: perfil_combinado.update(self.cargar_json_con_herencia(ruta_padre, visitados))
        perfil_combinado.update(data)
        return perfil_combinado

    def fusionar_perfil_snapmaker(self):
        perfil_completo = {}
        for dd, tipo in [(self.dd_maquina, "machine"), (self.dd_filamento, "filament"), (self.dd_proceso, "process")]:
            seleccion = dd.get().replace("⭐ ", "")
            if seleccion and seleccion != self.T("not_found"):
                ruta = self.encontrar_ruta_por_nombre(seleccion, tipo)
                if ruta:
                    datos = self.cargar_json_con_herencia(ruta)
                    perfil_completo.update(self.aplanar_diccionario(datos))
        return perfil_completo

    def categorizar_parametro(self, param):
        p = param.lower()
        if any(x in p for x in ['support', 'raft']): return "cat_support"
        if any(x in p for x in ['brim', 'skirt', 'bed_adhesion']): return "cat_adhesion"
        if any(x in p for x in ['infill', 'wall', 'shell', 'top_surface', 'bottom_surface', 'thickness']): return "cat_strength"
        if any(x in p for x in ['layer_height', 'seam', 'line_width', 'elefant', 'ironing']): return "cat_quality"
        if any(x in p for x in ['speed', 'accel', 'jerk']): return "cat_speed"
        if any(x in p for x in ['temp', 'fan', 'cooling', 'retract']): return "cat_material"
        return "cat_advanced"

    def es_parametro_clave(self, param):
        claves = ['layer_height', 'wall_loops', 'sparse_infill_density', 'sparse_infill_pattern', 'top_shell_layers', 'bottom_shell_layers', 'support_type', 'support_style', 'brim_type', 'print_sequence', 'ironing_type']
        return any(clave in param.lower() for clave in claves)

    def ejecutar_comparacion(self):
        placa_actual = self.dd_plates.get()
        if not placa_actual or placa_actual not in self.placas_data:
            messagebox.showwarning(self.T("attention"), self.T("warn_load_first"))
            return

        snap_p = self.fusionar_perfil_snapmaker()
        mw_p = self.aplanar_diccionario(self.placas_data[placa_actual])

        self.diferencias_actuales = []
        basura_interna = ['id', 'name', 'printer', 'version', 'compatible', 'from', 'setting_id', 'instantiation', 'gcode', 'machine', 'default_', 'time_']

        for k, v_mw in mw_p.items():
            if any(x in k.lower() for x in basura_interna): continue
            valor_rescate = self.valores_base_orca.get(k, self.T("internal_base"))
            v_snap = snap_p.get(k, valor_rescate)
            
            if not self.valores_son_iguales(v_mw, v_snap):
                if v_snap in ["Heredado del Slicer", "Inherited from Slicer"]: v_snap = self.T("inherited")
                self.diferencias_actuales.append({
                    "param": k, "v_mw": v_mw, "v_snap": v_snap, 
                    "categoria": self.categorizar_parametro(k), "es_clave": self.es_parametro_clave(k)
                })

        self.renderizar_resultados()

    def renderizar_resultados(self):
        for w in self.content_container.winfo_children(): w.destroy()

        if not self.diferencias_actuales:
            lbl = ctk.CTkLabel(self.content_container, text=self.T("res_no_diff"), text_color=TEXT_MUTED, font=ctk.CTkFont(size=16))
            lbl.pack(expand=True)
            return

        filtro_basico = self.switch_filtro.get() == 1
        grupos = {}
        items_mostrados = 0

        for item in self.diferencias_actuales:
            if filtro_basico and not item["es_clave"]: continue 
            cat = item["categoria"]
            if cat not in grupos: grupos[cat] = []
            grupos[cat].append(item)
            items_mostrados += 1

        if items_mostrados == 0:
            lbl = ctk.CTkLabel(self.content_container, text=self.T("res_no_basic"), text_color=TEXT_MUTED, font=ctk.CTkFont(size=16))
            lbl.pack(expand=True)
            return

        tabview = ctk.CTkTabview(self.content_container, fg_color="transparent", segmented_button_selected_color=SNAPMAKER_TEAL, segmented_button_selected_hover_color=SNAPMAKER_TEAL_HOVER)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)

        orden_categorias = ["cat_quality", "cat_strength", "cat_support", "cat_adhesion", "cat_material", "cat_speed", "cat_advanced"]
        
        for cat_key in orden_categorias:
            if cat_key in grupos:
                cat_nombre_traducido = self.T(cat_key)
                tabview.add(cat_nombre_traducido)
                scroll = ctk.CTkScrollableFrame(tabview.tab(cat_nombre_traducido), fg_color="transparent")
                scroll.pack(fill="both", expand=True)

                for item in grupos[cat_key]:
                    fila = ctk.CTkFrame(scroll, fg_color=BG_ROW_ALT, height=45, corner_radius=4)
                    fila.pack(fill="x", pady=2)
                    fila.pack_propagate(False)

                    clean_name = item["param"].split('.')[-1].replace('_', ' ').capitalize()
                    lbl_name = ctk.CTkLabel(fila, text=clean_name, font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_MAIN, anchor="w", cursor="hand2")
                    lbl_name.pack(side="left", padx=15, fill="x", expand=True)
                    lbl_name.bind("<Enter>", lambda e, p=item["param"]: self.set_tooltip(e, self.get_tooltip(p)))
                    lbl_name.bind("<Leave>", self.clear_tooltip)

                    ctk.CTkLabel(fila, text=str(item["v_mw"]), font=ctk.CTkFont(size=14, weight="bold"), text_color=ACCENT_ORANGE, width=150, anchor="w").pack(side="left", padx=10)
                    ctk.CTkLabel(fila, text=str(item["v_snap"]), font=ctk.CTkFont(size=13), text_color=SNAPMAKER_TEAL, width=150, anchor="w").pack(side="left", padx=15)

    def exportar_txt(self):
        if not self.diferencias_actuales: return
        f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")], title=self.T("export_title"))
        if not f: return
        try:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(f"{self.T('txt_report_title')}\n")
                placa_actual = self.dd_plates.get()
                if not placa_actual or placa_actual == "---": placa_actual = self.T('txt_none')
                file.write(f"{self.T('txt_plate')}: {placa_actual}\n")
                file.write(f"{self.T('txt_printer')}: {self.dd_maquina.get()}\n")
                file.write(f"{self.T('txt_process')}: {self.dd_proceso.get()}\n")
                file.write(f"{self.T('txt_filament')}: {self.dd_filamento.get()}\n")
                file.write("-" * 40 + "\n\n")
                filtro_basico = self.switch_filtro.get() == 1
                for item in self.diferencias_actuales:
                    if filtro_basico and not item["es_clave"]: continue
                    clean_name = item["param"].split('.')[-1]
                    file.write(f"[*] {clean_name}\n")
                    file.write(f"    {self.T('txt_change_to')} {item['v_mw']}\n")
                    file.write(f"    {self.T('txt_current')} {item['v_snap']}\n\n")
            messagebox.showinfo(self.T("export_title"), self.T("export_success"))
        except Exception as e:
            messagebox.showerror(self.T("error"), str(e))

    # --- LÓGICA DE EXPORTACIÓN 3MF (EL CONVERSOR) ---
    def exportar_3mf_adaptado(self):
        if not self.ruta_3mf_actual:
            messagebox.showwarning(self.T("attention"), self.T("warn_load_first"))
            return

        f_out = filedialog.asksaveasfilename(defaultextension=".3mf", filetypes=[("3MF file", "*.3mf")], title=self.T("export_title"))
        if not f_out: return

        allowed_keys = set()
        if self.chk_quality.get(): allowed_keys.update(CONVERTER_PARAMS["quality"])
        if self.chk_strength.get(): allowed_keys.update(CONVERTER_PARAMS["strength"])
        if self.chk_support.get(): allowed_keys.update(CONVERTER_PARAMS["support"])
        if self.chk_adhesion.get(): allowed_keys.update(CONVERTER_PARAMS["adhesion"])
        if self.chk_temp.get(): allowed_keys.update(CONVERTER_PARAMS["temperature"])

        maq_clean = self.dd_maquina.get().replace("⭐ ", "").replace(self.T("tag_user"), "").replace(self.T("tag_system"), "").strip()
        pro_clean = self.dd_proceso.get().replace("⭐ ", "").replace(self.T("tag_user"), "").replace(self.T("tag_system"), "").strip()

        printer_model = "Snapmaker U1"
        if "J1" in maq_clean: printer_model = "Snapmaker J1"
        elif "Artisan" in maq_clean: printer_model = "Snapmaker Artisan"

        all_transferable_keys = set(sum(CONVERTER_PARAMS.values(), []))

        user_colors = {}
        for fil in self.detected_filaments[:TARGET_FILAMENTS]:
            user_colors[fil['id']] = {'color': fil['color'], 'type': fil['type']}

        try:
            with zipfile.ZipFile(self.ruta_3mf_actual, 'r') as z:
                try: orig_settings = json.loads(z.read('Metadata/project_settings.config').decode('utf-8'))
                except: orig_settings = {}
        except Exception as e:
            messagebox.showerror(self.T("error"), f"Error reading original project: {e}")
            return

        diff = orig_settings.get('different_settings_to_system', [])
        has_support = any(isinstance(s, str) and 'enable_support' in s for s in diff)
        template = 'u1_template_supports.3mf' if has_support else 'u1_template.3mf'

        try:
            with zipfile.ZipFile(template, 'r') as z:
                u1_settings = json.loads(z.read('Metadata/project_settings.config').decode('utf-8'))
        except Exception:
            messagebox.showerror(self.T("error"), f"Faltan plantillas base ({template}). Ponlas en la misma carpeta que el programa.")
            return

        try:
            with zipfile.ZipFile(self.ruta_3mf_actual, 'r') as zin, \
                 zipfile.ZipFile(f_out, 'w', compression=zipfile.ZIP_DEFLATED) as zout:

                id_mapping = {}
                modified_slice_info = None
                modified_model_settings = None

                # 1. Modificar XML de slice_info.config
                if 'Metadata/slice_info.config' in zin.namelist():
                    xml_str = zin.read('Metadata/slice_info.config').decode('utf-8')
                    xml_str = re.sub(
                        r'key="printer_model_id" value="[^"]*"',
                        f'key="printer_model_id" value="{printer_model}"',
                        xml_str
                    )
                    if "<?xml" in xml_str or "<config>" in xml_str:
                        root = ET.fromstring(xml_str)
                        filaments_parent = root.find('.//plate')
                        if filaments_parent is None: filaments_parent = root

                        existing_nodes = filaments_parent.findall('filament')
                        new_id_counter = 1

                        for node in list(existing_nodes):
                            old_id = node.get('id')
                            if old_id not in user_colors:
                                filaments_parent.remove(node)
                            else:
                                conf = user_colors[old_id]
                                id_mapping[old_id] = str(new_id_counter)
                                node.set('id', str(new_id_counter))
                                node.set('color', conf['color'])
                                node.set('type', conf['type'])
                                new_id_counter += 1

                        while new_id_counter <= TARGET_FILAMENTS:
                            dummy = ET.SubElement(filaments_parent, 'filament')
                            dummy.set('id', str(new_id_counter))
                            dummy.set('type', 'PLA')
                            dummy.set('color', '#FFFFFFFF')
                            dummy.set('used_m', '0')
                            dummy.set('used_g', '0')
                            new_id_counter += 1

                        modified_slice_info = ET.tostring(root, encoding='utf-8', xml_declaration=True)
                    else:
                        modified_slice_info = xml_str.encode('utf-8')

                # 2. Modificar XML de model_settings.config
                if 'Metadata/model_settings.config' in zin.namelist():
                    model_root = ET.fromstring(zin.read('Metadata/model_settings.config').decode('utf-8'))
                    for meta in model_root.findall('.//metadata[@key="extruder"]'):
                        old_ext = meta.get('value')
                        if old_ext in id_mapping:
                            meta.set('value', id_mapping[old_ext])
                    modified_model_settings = ET.tostring(model_root, encoding='utf-8', xml_declaration=True)

                # 3. Modificar JSON de project_settings.config
                combined = u1_settings.copy()
                new_colors = []
                new_types = []

                for fil in self.detected_filaments:
                    fid = fil['id']
                    if fid not in user_colors: continue
                    color = user_colors[fid]['color']
                    ftype = user_colors[fid]['type']
                    color = (color + 'FF') if len(color) == 7 else color
                    new_colors.append(color.upper())
                    new_types.append(ftype)

                while len(new_colors) < TARGET_FILAMENTS:
                    new_colors.append('#FFFFFFFF')
                    new_types.append('PLA')

                combined['filament_colour'] = new_colors
                combined['filament_type'] = new_types

                profile_map = {f['type']: f['settings_id'] for f in self.available_filaments}
                default_profile = self.available_filaments[0]['settings_id'] if self.available_filaments else DEFAULT_FILAMENT_PROFILE
                combined['filament_settings_id'] = [profile_map.get(t, default_profile) for t in new_types]

                for key, val in combined.items():
                    if key.startswith('filament_') and isinstance(val, list) and 0 < len(val) != TARGET_FILAMENTS:
                        if len(val) < TARGET_FILAMENTS:
                            val.extend([val[-1]] * (TARGET_FILAMENTS - len(val)))
                        else:
                            combined[key] = val[:TARGET_FILAMENTS]

                # Inyectar perfil elegido de máquina y proceso
                if maq_clean and maq_clean != self.T("not_found"):
                    combined["printer_model"] = printer_model
                    combined["machine"] = [maq_clean] if isinstance(combined.get("machine"), list) else maq_clean
                if pro_clean and pro_clean != self.T("not_found"):
                    combined["process"] = pro_clean

                # Mantener los parámetros elegidos por el usuario desde el .3mf original
                for k in allowed_keys:
                    if k in orig_settings:
                        combined[k] = orig_settings[k]

                combined_bytes = json.dumps(combined, indent=4, ensure_ascii=False).encode('utf-8')

                # 4. Volcar todo al nuevo ZIP
                for item in zin.infolist():
                    safe_name = posixpath.normpath(item.filename).lstrip('/')
                    if safe_name.startswith('..'): continue

                    if item.filename == 'Metadata/project_settings.config':
                        zout.writestr(item, combined_bytes)
                    elif item.filename == 'Metadata/slice_info.config' and modified_slice_info:
                        zout.writestr(item, modified_slice_info)
                    elif item.filename == 'Metadata/model_settings.config' and modified_model_settings:
                        zout.writestr(item, modified_model_settings)
                    else:
                        zout.writestr(item, zin.read(item.filename))
            
            messagebox.showinfo(self.T("export_title"), self.T("conv_success"))
        except Exception as e:
            messagebox.showerror(self.T("error"), str(e))

if __name__ == "__main__":
    app = ProfessionalCompareApp()
    app.mainloop()
