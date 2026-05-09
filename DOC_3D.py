import customtkinter as ctk
from tkinter import filedialog, messagebox
import zipfile
import json
import os
import platform
import locale
import webbrowser
from pathlib import Path

# --- VERSIÓN DE LA APP ---
APP_VERSION = "v1.0.0"
GITHUB_URL = "https://github.com/Dakros66/DOC-3D-Profile-Inspector"

# --- DICCIONARIO DE IDIOMAS ---
TRANSLATIONS = {
    "en": {
        "title": "DOC 3D\nPROFILE INSPECTOR",
        "step1": "1. BUILD YOUR PROFILE",
        "printer": "⚙️ Printer",
        "process": "📏 Process (Quality/Infill)",
        "filament": "🧵 Filament (Material)",
        "step2": "2. MAKERWORLD FILE",
        "btn_load": "Select .3MF file",
        "filter": "Basic Filter (Hide Advanced)",
        "btn_analyze": "ANALYZE CHANGES",
        "status_wait": "Waiting for files...",
        "status_3mf_ok": "✅ 3MF file loaded",
        "status_auto_mat": "🎯 Material auto-selected: {}",
        "res_title": "Analysis Results",
        "res_welcome": "Welcome. Build your profile and load a .3mf to start.",
        "res_no_diff": "✅ No differences detected.",
        "res_no_basic": "No critical basic changes.\nDisable 'Basic Filter' to see advanced settings.",
        "res_showing": "Showing {} differences",
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
        "creator": "CREATOR: {}",
        "your_u1": "YOUR U1: {}",
        "not_found": "Not found",
        "inherited": "Inherited from Slicer",
        "internal_base": "Internal base value",
        "err_load_3mf": "Error processing 3MF:\n{}",
        "warn_load_first": "Please load a .3mf file first.",
        "all_perfect": "All perfect",
        "no_changes": "No changes detected",
        "tag_user": "[USER]",
        "tag_system": "[SYSTEM]"
    },
    "es": {
        "title": "DOC 3D\nPROFILE INSPECTOR",
        "step1": "1. CONSTRUYE TU PERFIL",
        "printer": "⚙️ Impresora",
        "process": "📏 Proceso (Calidad/Relleno)",
        "filament": "🧵 Filamento (Material)",
        "step2": "2. ARCHIVO MAKERWORLD",
        "btn_load": "Seleccionar archivo .3MF",
        "filter": "Filtro Básico (Ocultar Avanzados)",
        "btn_analyze": "ANALIZAR CAMBIOS",
        "status_wait": "Esperando archivos...",
        "status_3mf_ok": "✅ Archivo 3MF cargado",
        "status_auto_mat": "🎯 Material auto-seleccionado: {}",
        "res_title": "Resultados del Análisis",
        "res_welcome": "Bienvenido. Construye tu perfil y carga un .3mf para empezar.",
        "res_no_diff": "✅ No hay diferencias detectadas.",
        "res_no_basic": "No hay cambios básicos vitales.\nDesactiva el 'Filtro Básico' para ver ajustes internos.",
        "res_showing": "Mostrando {} diferencias",
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
        "creator": "CREADOR: {}",
        "your_u1": "TU U1: {}",
        "not_found": "No encontrados",
        "inherited": "Heredado del Slicer",
        "internal_base": "Valor base interno",
        "err_load_3mf": "Error al procesar 3MF:\n{}",
        "warn_load_first": "Por favor, carga primero un archivo .3mf.",
        "all_perfect": "Todo perfecto",
        "no_changes": "Sin cambios detectados",
        "tag_user": "[USUARIO]",
        "tag_system": "[SISTEMA]"
    },
    "fr": {
        "title": "DOC 3D\nPROFILE INSPECTOR",
        "step1": "1. CRÉEZ VOTRE PROFIL",
        "printer": "⚙️ Imprimante",
        "process": "📏 Processus (Qualité/Remplissage)",
        "filament": "🧵 Filament (Matériau)",
        "step2": "2. FICHIER MAKERWORLD",
        "btn_load": "Sélectionner un fichier .3MF",
        "filter": "Filtre Basique (Masquer Avancé)",
        "btn_analyze": "ANALYSER LES CHANGEMENTS",
        "status_wait": "En attente de fichiers...",
        "status_3mf_ok": "✅ Fichier 3MF chargé",
        "status_auto_mat": "🎯 Matériau auto-sélectionné: {}",
        "res_title": "Résultats de l'Analyse",
        "res_welcome": "Bienvenue. Créez votre profil et chargez un .3mf pour commencer.",
        "res_no_diff": "✅ Aucune différence détectée.",
        "res_no_basic": "Aucun changement de base critique.\nDésactivez le 'Filtre Basique' pour voir les paramètres avancés.",
        "res_showing": "Affichage de {} différences",
        "cat_quality": "✨ Qualité",
        "cat_strength": "💪 Résistance",
        "cat_support": "🚧 Supports",
        "cat_adhesion": "🧲 Adhésion",
        "cat_material": "🔥 Matériau/Ventilation",
        "cat_speed": "⚡ Vitesse",
        "cat_advanced": "⚙️ Avancé",
        "col_param": "Paramètre à changer",
        "col_mw": "Valeur dans .3MF",
        "col_u1": "Votre U1 (Base)",
        "creator": "CRÉATEUR: {}",
        "your_u1": "VOTRE U1: {}",
        "not_found": "Introuvable",
        "inherited": "Hérité du Slicer",
        "internal_base": "Valeur de base interne",
        "err_load_3mf": "Erreur lors du traitement du 3MF:\n{}",
        "warn_load_first": "Veuillez d'abord charger un fichier .3mf.",
        "all_perfect": "Tout est parfait",
        "no_changes": "Aucun changement",
        "tag_user": "[UTILISATEUR]",
        "tag_system": "[SYSTÈME]"
    },
    "de": {
        "title": "DOC 3D\nPROFILE INSPECTOR",
        "step1": "1. PROFIL ERSTELLEN",
        "printer": "⚙️ Drucker",
        "process": "📏 Prozess (Qualität/Füllung)",
        "filament": "🧵 Filament (Material)",
        "step2": "2. MAKERWORLD DATEI",
        "btn_load": ".3MF-Datei auswählen",
        "filter": "Basisfilter (Erweitert ausblenden)",
        "btn_analyze": "ÄNDERUNGEN ANALYSIEREN",
        "status_wait": "Warten auf Dateien...",
        "status_3mf_ok": "✅ 3MF-Datei geladen",
        "status_auto_mat": "🎯 Material automatisch ausgewählt: {}",
        "res_title": "Analyseergebnisse",
        "res_welcome": "Willkommen. Erstellen Sie Ihr Profil und laden Sie eine .3mf.",
        "res_no_diff": "✅ Keine Unterschiede festgestellt.",
        "res_no_basic": "Keine kritischen Basisänderungen.\nDeaktivieren Sie den 'Basisfilter' für erweiterte Einstellungen.",
        "res_showing": "Zeige {} Unterschiede",
        "cat_quality": "✨ Qualität",
        "cat_strength": "💪 Festigkeit",
        "cat_support": "🚧 Stützen",
        "cat_adhesion": "🧲 Haftung",
        "cat_material": "🔥 Material/Kühlung",
        "cat_speed": "⚡ Geschwindigkeit",
        "cat_advanced": "⚙️ Erweitert",
        "col_param": "Zu ändernder Parameter",
        "col_mw": "Wert in .3MF",
        "col_u1": "Dein U1 (Basis)",
        "creator": "ERSTELLER: {}",
        "your_u1": "DEIN U1: {}",
        "not_found": "Nicht gefunden",
        "inherited": "Vom Slicer geerbt",
        "internal_base": "Interner Basiswert",
        "err_load_3mf": "Fehler bei der 3MF-Verarbeitung:\n{}",
        "warn_load_first": "Bitte laden Sie zuerst eine .3mf-Datei.",
        "all_perfect": "Alles perfekt",
        "no_changes": "Keine Änderungen",
        "tag_user": "[BENUTZER]",
        "tag_system": "[SYSTEM]"
    },
    "zh": {
        "title": "DOC 3D\nPROFILE INSPECTOR",
        "step1": "1. 构建您的配置文件",
        "printer": "⚙️ 打印机",
        "process": "📏 工艺 (质量/填充)",
        "filament": "🧵 耗材 (材料)",
        "step2": "2. MAKERWORLD 文件",
        "btn_load": "选择 .3MF 文件",
        "filter": "基本过滤器 (隐藏高级)",
        "btn_analyze": "分析更改",
        "status_wait": "等待文件...",
        "status_3mf_ok": "✅ 3MF 文件已加载",
        "status_auto_mat": "🎯 自动选择材料: {}",
        "res_title": "分析结果",
        "res_welcome": "欢迎。构建您的配置文件并加载 .3mf 以开始。",
        "res_no_diff": "✅ 未检测到差异。",
        "res_no_basic": "没有关键的基本更改。\n禁用“基本过滤器”以查看高级设置。",
        "res_showing": "显示 {} 个差异",
        "cat_quality": "✨ 质量",
        "cat_strength": "💪 强度",
        "cat_support": "🚧 支撑",
        "cat_adhesion": "🧲 附着力",
        "cat_material": "🔥 材料/冷却",
        "cat_speed": "⚡ 速度",
        "cat_advanced": "⚙️ 高级",
        "col_param": "要更改的参数",
        "col_mw": ".3MF 中的值",
        "col_u1": "您的 U1 (基础)",
        "creator": "创建者: {}",
        "your_u1": "您的 U1: {}",
        "not_found": "未找到",
        "inherited": "继承自切片软件",
        "internal_base": "内部基础值",
        "err_load_3mf": "处理 3MF 错误:\n{}",
        "warn_load_first": "请先加载 .3mf 文件。",
        "all_perfect": "一切完美",
        "no_changes": "未检测到更改",
        "tag_user": "[用户]",
        "tag_system": "[系统]"
    }
}

LANG_MAP = {"English": "en", "Español": "es", "Français": "fr", "Deutsch": "de", "中文": "zh"}
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

        # --- IDIOMA DEL SISTEMA ---
        self.current_lang = self.detect_system_language()

        # Configuración de la ventana
        self.title(f"DOC 3D Profile Inspector - {APP_VERSION}")
        self.geometry("1300x850") 
        self.configure(fg_color=BG_MAIN)
        self.minsize(1100, 750)

        self.valores_base_orca = {
            "sparse_infill_density": "15%",
            "sparse_infill_pattern": "grid",
            "wall_loops": "2",
            "top_shell_layers": "3",
            "bottom_shell_layers": "3",
            "layer_height": "0.2",
            "initial_layer_height": "0.2",
            "seam_position": "aligned",
            "seam_gap": "15%",
            "elefant_foot_compensation": "0",
            "support_type": "normal(auto)",
            "support_style": "default",
            "brim_type": "outer_only",
            "brim_width": "5",
            "ironing_type": "no_ironing",
            "print_sequence": "by_layer",
            "default_acceleration": "10000",
            "travel_speed": "500",
            "enable_support": "0", 
            "draft_shield": "disabled",
            "wall_generator": "arachne",
            "reduce_infill_retraction": "1"
        }

        self.makerworld_data = None
        self.perfiles_dict = {"machine": {}, "process": {}, "filament": {}}
        self.diccionario_rutas_global = {}
        self.diferencias_actuales = []
        
        self.archivo_favoritos = os.path.join(Path.home(), ".doc3d_inspector_favs.json")
        self.favoritos = self.cargar_favoritos()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=420) 
        self.grid_columnconfigure(1, weight=1)

        self.buscar_perfiles_automaticamente()
        self.crear_sidebar()
        self.crear_panel_principal()

    def T(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

    def detect_system_language(self):
        try:
            loc = locale.getdefaultlocale()[0]
            if loc:
                code = loc[:2].lower()
                if code in TRANSLATIONS:
                    return code
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
        self.switch_filtro.configure(text=self.T("filter"))
        self.btn_analizar.configure(text=self.T("btn_analyze"))
        
        if self.makerworld_data:
            self.lbl_status.configure(text=self.T("status_3mf_ok"))
        else:
            self.lbl_status.configure(text=self.T("status_wait"))

        for tipo, dd in [("machine", self.dd_maquina), ("process", self.dd_proceso), ("filament", self.dd_filamento)]:
            sel = dd.get()
            dd.configure(values=self.get_sorted_keys(tipo))
            if sel in ["No encontrados", "Not found", "Introuvable", "Nicht gefunden", "未找到"]:
                dd.set(self.T("not_found"))

        if self.diferencias_actuales:
            self.renderizar_resultados()
        else:
            self.header_label.configure(text=self.T("res_title"))
            self.render_empty_state(self.T("res_welcome"))

    def abrir_github(self):
        webbrowser.open(GITHUB_URL)

    # --- SISTEMA DE FAVORITOS ---
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
        if ruta_vinculada and ruta_vinculada in self.favoritos[tipo]:
            btn.configure(text="⭐", text_color=ACCENT_ORANGE)
        else:
            btn.configure(text="☆", text_color=TEXT_MUTED)

    def encontrar_ruta_por_nombre(self, nombre_mostrado, tipo):
        for original, ruta in self.perfiles_dict[tipo].items():
            limpio_orig = original.replace("[USER]", "").replace("[SYSTEM]", "").strip()
            limpio_most = nombre_mostrado.replace(self.T("tag_user"), "").replace(self.T("tag_system"), "").strip()
            if limpio_orig == limpio_most:
                return ruta
        return None

    # --- MOTOR DE BÚSQUEDA Y ARCHIVOS ---
    def buscar_perfiles_automaticamente(self):
        home = str(Path.home())
        rutas_a_escanear = []
        
        if platform.system() == "Darwin":
            rutas_a_escanear = [
                os.path.join(home, "Library/Application Support/Snapmaker_Orca/system/Snapmaker"),
                os.path.join(home, "Library/Application Support/Snapmaker_Orca/user/default"),
                "/Applications/Snapmaker Orca.app/Contents/Resources/profiles",
                "/Applications/Snapmaker_Orca.app/Contents/Resources/profiles",
                "/Applications/OrcaSlicer.app/Contents/Resources/profiles"
            ]
        else:
            appdata = os.getenv('APPDATA', '')
            archivos_programa = os.environ.get("PROGRAMFILES", "C:\\Program Files")
            rutas_a_escanear = [
                os.path.join(appdata, "Snapmaker_Orca/system/Snapmaker"),
                os.path.join(appdata, "Snapmaker_Orca/user/default"),
                os.path.join(archivos_programa, "Snapmaker Orca/resources/profiles"),
                os.path.join(archivos_programa, "OrcaSlicer/resources/profiles")
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
                            except Exception: pass 

    def get_sorted_keys(self, tipo):
        nombres_internos = list(self.perfiles_dict[tipo].keys())
        
        nombres_mostrados = []
        rutas = []
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

    # --- INTERFAZ DE USUARIO ---
    def crear_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_SIDEBAR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=self.T("title"), font=ctk.CTkFont(size=24, weight="bold"), text_color=SNAPMAKER_TEAL)
        self.logo_label.grid(row=0, column=0, padx=30, pady=(30, 20))

        self.lbl_step1 = ctk.CTkLabel(self.sidebar_frame, text=self.T("step1"), font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_step1.grid(row=1, column=0, padx=30, pady=(5, 5), sticky="w")
        
        # --- MÁQUINA ---
        self.lbl_printer = ctk.CTkLabel(self.sidebar_frame, text=self.T("printer"), font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_printer.grid(row=2, column=0, padx=30, pady=(5, 0), sticky="w")
        frm_maq = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        frm_maq.grid(row=3, column=0, padx=30, pady=(2, 5), sticky="ew")
        
        self.dd_maquina = ctk.CTkComboBox(frm_maq, values=self.get_sorted_keys("machine"), fg_color=BG_CARD, border_color=BG_CARD, button_color=SNAPMAKER_TEAL, button_hover_color=SNAPMAKER_TEAL_HOVER, height=40, command=lambda c: self.actualizar_estado_boton_fav(c, "machine", self.btn_fav_maq))
        self.dd_maquina.pack(side="left", fill="x", expand=True)
        self.dd_maquina._entry.bind("<KeyRelease>", lambda e: self.filtrar_combobox(e, self.dd_maquina, "machine"))
        
        self.btn_fav_maq = ctk.CTkButton(frm_maq, text="☆", width=40, height=40, fg_color=BG_CARD, hover_color="#4F4F56", text_color=TEXT_MUTED, font=ctk.CTkFont(size=18), command=lambda: self.toggle_fav("machine", self.dd_maquina, self.btn_fav_maq))
        self.btn_fav_maq.pack(side="right", padx=(5, 0))

        # --- PROCESO ---
        self.lbl_process = ctk.CTkLabel(self.sidebar_frame, text=self.T("process"), font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_process.grid(row=4, column=0, padx=30, pady=(5, 0), sticky="w")
        frm_pro = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        frm_pro.grid(row=5, column=0, padx=30, pady=(2, 5), sticky="ew")
        
        self.dd_proceso = ctk.CTkComboBox(frm_pro, values=self.get_sorted_keys("process"), fg_color=BG_CARD, border_color=BG_CARD, button_color=SNAPMAKER_TEAL, button_hover_color=SNAPMAKER_TEAL_HOVER, height=40, command=lambda c: self.actualizar_estado_boton_fav(c, "process", self.btn_fav_pro))
        self.dd_proceso.pack(side="left", fill="x", expand=True)
        self.dd_proceso._entry.bind("<KeyRelease>", lambda e: self.filtrar_combobox(e, self.dd_proceso, "process"))

        self.btn_fav_pro = ctk.CTkButton(frm_pro, text="☆", width=40, height=40, fg_color=BG_CARD, hover_color="#4F4F56", text_color=TEXT_MUTED, font=ctk.CTkFont(size=18), command=lambda: self.toggle_fav("process", self.dd_proceso, self.btn_fav_pro))
        self.btn_fav_pro.pack(side="right", padx=(5, 0))

        # --- FILAMENTO ---
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

        self.lbl_step2 = ctk.CTkLabel(self.sidebar_frame, text=self.T("step2"), font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_step2.grid(row=8, column=0, padx=30, pady=(10, 8), sticky="w")
        
        self.btn_load_3mf = ctk.CTkButton(self.sidebar_frame, text=self.T("btn_load"), command=self.cargar_3mf, fg_color="transparent", border_width=2, border_color=SNAPMAKER_TEAL, text_color=TEXT_MAIN, hover_color=BG_CARD, height=45, font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_load_3mf.grid(row=9, column=0, padx=30, pady=(0, 20), sticky="ew")

        self.switch_filtro = ctk.CTkSwitch(self.sidebar_frame, text=self.T("filter"), command=self.renderizar_resultados, progress_color=SNAPMAKER_TEAL, font=ctk.CTkFont(size=14, weight="bold"))
        self.switch_filtro.grid(row=10, column=0, padx=30, pady=(0, 20), sticky="w")
        self.switch_filtro.select()

        self.btn_analizar = ctk.CTkButton(self.sidebar_frame, text=self.T("btn_analyze"), command=self.ejecutar_comparacion, fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER, height=60, font=ctk.CTkFont(size=18, weight="bold"))
        self.btn_analizar.grid(row=11, column=0, padx=30, pady=10, sticky="ew")

        self.lbl_status = ctk.CTkLabel(self.sidebar_frame, text=self.T("status_wait"), font=ctk.CTkFont(size=13), text_color=TEXT_MUTED)
        self.lbl_status.grid(row=12, column=0, padx=30, pady=10)

        # --- FOOTER (VERSIÓN Y GITHUB) ---
        self.sidebar_frame.grid_rowconfigure(13, weight=1) # Empuja el footer hacia abajo
        
        self.footer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.footer_frame.grid(row=14, column=0, padx=30, pady=20, sticky="ew")
        
        self.lbl_version = ctk.CTkLabel(self.footer_frame, text=APP_VERSION, font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_version.pack(side="left")
        
        self.btn_github = ctk.CTkButton(self.footer_frame, text="GitHub ↗", width=70, height=28, fg_color=BG_CARD, hover_color="#4F4F56", font=ctk.CTkFont(size=12, weight="bold"), command=self.abrir_github)
        self.btn_github.pack(side="right")

    def crear_panel_principal(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.header_label = ctk.CTkLabel(self.header_frame, text=self.T("res_title"), font=ctk.CTkFont(size=28, weight="bold"))
        self.header_label.pack(side="left")

        self.lang_menu = ctk.CTkOptionMenu(
            self.header_frame, values=list(LANG_MAP.keys()), 
            command=self.change_language, width=120, 
            fg_color=BG_CARD, button_color=BG_CARD, button_hover_color="#4F4F56"
        )
        self.lang_menu.set(INV_LANG_MAP[self.current_lang])
        self.lang_menu.pack(side="right")

        self.content_container = ctk.CTkFrame(self.main_frame, fg_color=BG_SIDEBAR, corner_radius=12)
        self.content_container.grid(row=1, column=0, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.render_empty_state(self.T("res_welcome"))

    def render_empty_state(self, msg):
        for w in self.content_container.winfo_children(): w.destroy()
        lbl = ctk.CTkLabel(self.content_container, text=msg, text_color=TEXT_MUTED, font=ctk.CTkFont(size=16))
        lbl.grid(row=0, column=0, pady=100)

    # --- LÓGICA DE DATOS Y HERENCIA ---
    def cargar_3mf(self):
        ruta = filedialog.askopenfilename(filetypes=[("3MF", "*.3mf")])
        if ruta:
            try:
                self.makerworld_data = self.extraer_datos_3mf(ruta)
                self.btn_load_3mf.configure(text=f"✓ {os.path.basename(ruta)[:20]}...")
                self.lbl_status.configure(text=self.T("status_3mf_ok"))
                self.autodetectar_material()
            except Exception as e: messagebox.showerror("Error", self.T("err_load_3mf").format(e))

    def extraer_datos_3mf(self, ruta_3mf):
        datos = {}
        with zipfile.ZipFile(ruta_3mf, 'r') as z:
            for name in z.namelist():
                if ("Metadata/" in name or "Config/" in name) and (name.endswith('.json') or name.endswith('.config')):
                    try: datos.update(json.loads(z.read(name).decode('utf-8')))
                    except: pass
        return datos

    def aplanar_diccionario(self, d, prefix=''):
        items = {}
        for k, v in d.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict): items.update(self.aplanar_diccionario(v, new_key))
            else: items[new_key] = v
        return items

    def autodetectar_material(self):
        if not self.makerworld_data: return
        mw_plano = self.aplanar_diccionario(self.makerworld_data)
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
        if not self.makerworld_data:
            messagebox.showwarning("Atención", self.T("warn_load_first"))
            return

        snap_p = self.fusionar_perfil_snapmaker()
        mw_p = self.aplanar_diccionario(self.makerworld_data)

        self.diferencias_actuales = []
        basura_interna = ['id', 'name', 'printer', 'version', 'compatible', 'from', 'setting_id', 'instantiation', 'gcode', 'machine', 'default_', 'time_']

        for k, v_mw in mw_p.items():
            if any(x in k.lower() for x in basura_interna): continue
            
            valor_rescate = self.valores_base_orca.get(k, self.T("internal_base"))
            v_snap = snap_p.get(k, valor_rescate)
            
            if str(v_mw) != str(v_snap):
                if v_snap == "Heredado del Slicer": v_snap = self.T("inherited")
                
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
                    
                    ctk.CTkLabel(fila, text=clean_name, font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_MAIN, anchor="w").pack(side="left", padx=15, fill="x", expand=True)
                    ctk.CTkLabel(fila, text=str(item["v_mw"]), font=ctk.CTkFont(size=14, weight="bold"), text_color=ACCENT_ORANGE, width=150, anchor="w").pack(side="left", padx=10)
                    ctk.CTkLabel(fila, text=str(item["v_snap"]), font=ctk.CTkFont(size=13), text_color=SNAPMAKER_TEAL, width=150, anchor="w").pack(side="left", padx=15)

if __name__ == "__main__":
    app = ProfessionalCompareApp()
    app.mainloop()
