import customtkinter as ctk
from tkinter import filedialog, messagebox
import zipfile
import json
import os
import platform
import locale
import webbrowser
import re
from pathlib import Path

# --- VERSIÓN DE LA APP ---
APP_VERSION = "v1.0.1"
GITHUB_URL = "https://github.com/Dakros66/DOC-3D-Profile-Inspector"

# --- DICCIONARIO DE IDIOMAS (Solo EN y ES) ---
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
        "res_title": "Analysis Results",
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
        "not_sliced": "Not Sliced"
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
        "res_title": "Resultados del Análisis",
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
        "not_sliced": "Sin Laminar"
    }
}

# --- TOOLTIPS ESPECÍFICOS ---
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

LANG_MAP = {"English": "en", "Español": "es"}
INV_LANG_MAP = {v: k for k, v in LANG_MAP.items()}

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

class ProfessionalCompareApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_lang = self.detect_system_language()

        self.title(f"DOC 3D Profile Inspector - {APP_VERSION}")
        self.geometry("1400x900") 
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

    def get_tooltip(self, param_name):
        base_name = param_name.split('.')[-1].lower()
        if base_name in TOOLTIPS:
            return TOOLTIPS[base_name].get(self.current_lang, TOOLTIPS[base_name].get("en"))
        return f"{self.T('cat_advanced')} ({base_name}) - {self.T('tooltip_advanced_desc')}"

    def detect_system_language(self):
        try:
            loc = locale.getdefaultlocale()[0]
            if loc and loc[:2].lower() in TRANSLATIONS: return loc[:2].lower()
        except: pass
        return 'en' 

    def change_language(self, selected_language_name):
        self.current_lang = LANG_MAP[selected_language_name]
        self.retranslate_ui()

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

        if self.diferencias_actuales: self.renderizar_resultados()
        else:
            self.header_label.configure(text=self.T("res_title"))
            self.render_empty_state(self.T("res_welcome"))

    def abrir_github(self):
        webbrowser.open(GITHUB_URL)

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

    # --- INTERFAZ ---
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

        # 3MF y PLACAS
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

        # HEADER
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

        # CONTENEDOR PRINCIPAL
        self.content_container = ctk.CTkFrame(self.main_frame, fg_color=BG_SIDEBAR, corner_radius=12)
        self.content_container.grid(row=2, column=0, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # TOOLTIP AREA 
        self.tooltip_frame = ctk.CTkFrame(self.main_frame, fg_color=BG_CARD, height=40, corner_radius=8)
        self.tooltip_frame.grid(row=3, column=0, sticky="ew", pady=(15, 0))
        self.tooltip_frame.pack_propagate(False)
        self.lbl_tooltip = ctk.CTkLabel(self.tooltip_frame, text=self.T("tooltip_default"), font=ctk.CTkFont(size=13, slant="italic"), text_color=TEXT_MAIN)
        self.lbl_tooltip.pack(side="left", padx=20)

        self.render_empty_state(self.T("res_welcome"))

    def render_empty_state(self, msg):
        for w in self.content_container.winfo_children(): w.destroy()
        lbl = ctk.CTkLabel(self.content_container, text=msg, text_color=TEXT_MUTED, font=ctk.CTkFont(size=16))
        lbl.grid(row=0, column=0, pady=100)

    def set_tooltip(self, event, text):
        self.lbl_tooltip.configure(text=text, text_color=ACCENT_ORANGE)

    def clear_tooltip(self, event):
        self.lbl_tooltip.configure(text=self.T("tooltip_default"), text_color=TEXT_MAIN)

    def cargar_3mf(self):
        ruta = filedialog.askopenfilename(filetypes=[("3MF", "*.3mf")])
        if ruta:
            try:
                self.extraer_datos_3mf(ruta)
                self.btn_load_3mf.configure(text=f"✓ {os.path.basename(ruta)[:20]}...")
                self.lbl_status.configure(text=self.T("status_3mf_ok"))
                
                if self.info_placas:
                    nombres_placas = list(self.info_placas.keys())
                    self.dd_plates.configure(values=nombres_placas)
                    self.dd_plates.set(nombres_placas[0])
                    self.cambiar_placa(nombres_placas[0])
                    self.autodetectar_material()
            except Exception as e: messagebox.showerror(self.T("error"), self.T("err_load_3mf").format(e))

    def extraer_datos_3mf(self, ruta_3mf):
        self.placas_data = {}
        self.info_placas = {}
        datos_globales = {}
        plate_catalog = {} 

        with zipfile.ZipFile(ruta_3mf, 'r') as z:
            # 1. Leer configs generales del proyecto
            for name in z.namelist():
                if ("Metadata/" in name or "Config/" in name) and (name.endswith('.json') or name.endswith('.config')):
                    if "plate_" in name or "slice_info" in name: 
                        continue
                    try: 
                        datos_globales.update(json.loads(z.read(name).decode('utf-8', errors='ignore')))
                    except: pass
            
            # 2. Extraer catálogo de placas y sus tiempos/pesos (si está laminado)
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
                                    plate_catalog[p_id] = p_name
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

            # 3. RASTREADOR INFALIBLE: Escanear miniaturas si el Slicer no creó slice_info
            for name in z.namelist():
                match = re.search(r'plate_(\d+)', name)
                if match:
                    p_id = str(match.group(1))
                    if p_id not in plate_catalog:
                        plate_catalog[p_id] = self.T("plate_num").format(p_id)

            # 4. Construir las placas
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
                    if unique_name in self.placas_data:
                        unique_name = f"{p_name} ({p_id})"
                        
                    self.placas_data[unique_name] = placa_final
                    
                    if unique_name not in self.info_placas:
                        self.info_placas[unique_name] = {"time": self.T("not_sliced"), "weight": self.T("not_sliced")}
            else:
                self.placas_data[self.T("default_plate")] = datos_globales
                self.info_placas[self.T("default_plate")] = {"time": self.T("not_sliced"), "weight": self.T("not_sliced")}

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

    def cambiar_placa(self, nombre_placa):
        info = self.info_placas.get(nombre_placa, {"time": self.T("not_sliced"), "weight": self.T("not_sliced")})
        self.lbl_info_print.configure(text=self.T("info_print").format(info["time"], info["weight"]))
        if self.diferencias_actuales: 
            self.ejecutar_comparacion()

    def aplanar_diccionario(self, d, prefix=''):
        items = {}
        for k, v in d.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict): items.update(self.aplanar_diccionario(v, new_key))
            else: items[new_key] = v
        return items

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
                if v_snap == "Heredado del Slicer" or v_snap == "Inherited from Slicer": 
                    v_snap = self.T("inherited")
                
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
            self.header_label.configure(text=self.T("no_changes"))
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
            self.header_label.configure(text=self.T("all_perfect"))
            return

        self.header_label.configure(text=self.T("res_showing").format(items_mostrados))
        
        tabview = ctk.CTkTabview(self.content_container, fg_color="transparent", segmented_button_selected_color=SNAPMAKER_TEAL, segmented_button_selected_hover_color=SNAPMAKER_TEAL_HOVER)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)

        orden_categorias = ["cat_quality", "cat_strength", "cat_support", "cat_adhesion", "cat_material", "cat_speed", "cat_advanced"]
        
        for cat_key in orden_categorias:
            if cat_key in grupos:
                cat_nombre_traducido = self.T(cat_key)
                tabview.add(cat_nombre_traducido)
                
                scroll = ctk.CTkScrollableFrame(tabview.tab(cat_nombre_traducido), fg_color="transparent")
                scroll.pack(fill="both", expand=True)

                header = ctk.CTkFrame(scroll, fg_color=BG_CARD, height=35, corner_radius=6)
                header.pack(fill="x", pady=(0, 5))
                header.pack_propagate(False)

                ctk.CTkLabel(header, text=self.T("col_param"), font=ctk.CTkFont(weight="bold", size=13), text_color=TEXT_MUTED, anchor="w").pack(side="left", padx=15, fill="x", expand=True)
                ctk.CTkLabel(header, text=self.T("col_mw"), font=ctk.CTkFont(weight="bold", size=13), text_color=TEXT_MUTED, width=150, anchor="w").pack(side="left", padx=10)
                ctk.CTkLabel(header, text=self.T("col_u1"), font=ctk.CTkFont(weight="bold", size=13), text_color=TEXT_MUTED, width=150, anchor="w").pack(side="left", padx=15)

                color_alterno = True
                for item in grupos[cat_key]:
                    bg = BG_ROW_ALT if color_alterno else "transparent"
                    color_alterno = not color_alterno

                    fila = ctk.CTkFrame(scroll, fg_color=bg, height=45, corner_radius=4)
                    fila.pack(fill="x", pady=2)
                    fila.pack_propagate(False)

                    clean_name = item["param"].split('.')[-1].replace('_', ' ').capitalize()
                    
                    lbl_name = ctk.CTkLabel(fila, text=clean_name, font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_MAIN, anchor="w", cursor="hand2")
                    lbl_name.pack(side="left", padx=15, fill="x", expand=True)
                    
                    lbl_name.bind("<Enter>", lambda e, p=item["param"]: self.set_tooltip(e, self.get_tooltip(p)))
                    lbl_name.bind("<Leave>", self.clear_tooltip)

                    ctk.CTkLabel(fila, text=str(item["v_mw"]), font=ctk.CTkFont(size=14, weight="bold"), text_color=ACCENT_ORANGE, width=150, anchor="w").pack(side="left", padx=10)
                    ctk.CTkLabel(fila, text=str(item["v_snap"]), font=ctk.CTkFont(size=13), text_color=SNAPMAKER_TEAL, width=150, anchor="w").pack(side="left", padx=15)

    # --- EXPORTAR REPORTE ---
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

if __name__ == "__main__":
    app = ProfessionalCompareApp()
    app.mainloop()
