"""
Modern Corporate Tema - Koyu sidebar, mavi accent, yuvarlatilmis koseler.
"""

RENKLER = {
    # Yuzeyler
    "bg": "#f8fafc",              # ana arkaplan (acik gri)
    "bg_alt": "#f1f5f9",         # alternatif yuzey
    "card": "#ffffff",            # kart arkaplan
    "inset": "#e2e8f0",          # input arkaplan

    # Sidebar
    "sidebar": "#0f172a",         # koyu lacivert
    "sidebar_hover": "#1e293b",   # sidebar hover
    "sidebar_active": "#1e293b",  # aktif menu

    # Metin
    "text": "#1e293b",            # ana metin (slate 800)
    "text_dim": "#334155",        # ikincil metin (slate 700)
    "text_muted": "#64748b",      # soluk metin (slate 500)
    "text_subtle": "#94a3b8",     # placeholder (slate 400)
    "text_faint": "#cbd5e1",      # disabled (slate 300)

    # Cizgiler
    "border": "#e2e8f0",          # ana kenarlık (slate 200)
    "border_light": "#f1f5f9",    # ince kenarlık (slate 100)

    # Accent
    "primary": "#3b82f6",         # mavi accent (blue 500)
    "primary_dark": "#1d4ed8",    # koyu mavi (blue 700)
    "primary_light": "#dbeafe",   # acik mavi bg (blue 100)
    "primary_pale": "#eff6ff",    # en acik mavi (blue 50)

    # Durum
    "success": "#10b981",
    "success_pale": "#d1fae5",
    "warning": "#f59e0b",
    "warning_pale": "#fef3c7",
    "danger": "#ef4444",
    "danger_pale": "#fee2e2",

    # Tablo
    "table_header_bg": "#f8fafc",
    "table_header_text": "#64748b",
    "table_zebra": "#f8fafc",
    "table_row_hover": "#eff6ff",
}


ANA_STIL = f"""
/* GENEL ============================================================ */
QWidget {{
    background-color: {RENKLER['bg']};
    color: {RENKLER['text']};
    font-family: "Inter", "Segoe UI", "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {RENKLER['bg']};
}}

QToolTip {{
    background-color: {RENKLER['sidebar']};
    color: #ffffff;
    border: none;
    padding: 7px 12px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
}}

/* SIDEBAR ========================================================== */
#Sidebar {{
    background-color: {RENKLER['sidebar']};
    border: none;
}}

#Sidebar QLabel {{
    background: transparent;
    border: none;
}}

#MastheadBaslik {{
    color: #ffffff;
    background: transparent;
    border: none;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-weight: 800;
    font-size: 18px;
}}

#MastheadAlt {{
    color: {RENKLER['text_subtle']};
    background: transparent;
    border: none;
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
}}

#MenuBaslik {{
    color: {RENKLER['text_subtle']};
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    background: transparent;
    border: none;
}}

QPushButton#MenuButon {{
    background-color: transparent;
    color: {RENKLER['text_subtle']};
    text-align: left;
    padding-left: 24px;
    padding-right: 24px;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0;
    font-family: "Inter", sans-serif;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton#MenuButon:hover {{
    background-color: {RENKLER['sidebar_hover']};
    color: #ffffff;
}}

QPushButton#MenuButon:checked {{
    background-color: {RENKLER['sidebar_active']};
    color: #ffffff;
    font-weight: 700;
    border-left: 3px solid {RENKLER['primary']};
}}

#KullaniciKart {{
    background-color: {RENKLER['sidebar_hover']};
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
}}

#KullaniciKart QLabel {{
    background: transparent;
    border: none;
}}

#KullaniciAd {{
    color: #ffffff;
    font-weight: 700;
    font-size: 12px;
    font-family: "Inter", sans-serif;
}}

#KullaniciDurum {{
    color: {RENKLER['text_subtle']};
    font-size: 10px;
    font-family: "Inter", sans-serif;
    text-transform: uppercase;
    font-weight: 600;
}}

#PlanRozet {{
    background-color: {RENKLER['primary']};
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 3px 9px;
    font-size: 9px;
    font-weight: 800;
    font-family: "Inter", sans-serif;
    min-width: 50px;
}}

/* SAYFA BASLIKLARI ================================================ */
#SayfaBaslik {{
    color: {RENKLER['text']};
    background: transparent;
    border: none;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 32px;
    font-weight: 800;
}}

#SayfaAltBaslik {{
    color: {RENKLER['text_muted']};
    background: transparent;
    border: none;
    font-family: "Inter", sans-serif;
    font-size: 13px;
    font-weight: 400;
}}

#KicekerBaslik {{
    color: {RENKLER['primary']};
    background: transparent;
    border: none;
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
}}

/* KARTLAR ========================================================= */
#Kart {{
    background-color: {RENKLER['card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 8px;
}}

#Kart QLabel {{
    background: transparent;
    border: none;
}}

#KartBaslik {{
    color: {RENKLER['text']};
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 16px;
    font-weight: 700;
    background: transparent;
    border: none;
}}

#KartAltBaslik {{
    color: {RENKLER['text_muted']};
    font-family: "Inter", sans-serif;
    font-size: 12px;
    background: transparent;
    border: none;
}}

/* BUTONLAR ======================================================== */
QPushButton {{
    background-color: {RENKLER['card']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border']};
    padding: 6px 16px;
    min-height: 28px;
    border-radius: 6px;
    font-family: "Inter", sans-serif;
    font-size: 12px;
    font-weight: 600;
}}

QPushButton:hover {{
    background-color: {RENKLER['bg']};
    border: 1px solid {RENKLER['text_muted']};
}}

QPushButton:disabled {{
    background-color: {RENKLER['bg_alt']};
    color: {RENKLER['text_faint']};
    border: 1px solid {RENKLER['border_light']};
}}

/* Ic widget butonlarini sifirla (QSpinBox, QComboBox, QScrollBar vb.) */
QSpinBox QPushButton, QDoubleSpinBox QPushButton,
QDateTimeEdit QPushButton, QDateEdit QPushButton,
QCalendarWidget QPushButton {{
    background-color: transparent;
    border: none;
    border-radius: 0;
    padding: 0;
    min-height: 0;
    min-width: 0;
}}

QPushButton#PrimaryButon {{
    background-color: {RENKLER['primary']};
    color: #ffffff;
    border: 1px solid {RENKLER['primary']};
}}

QPushButton#PrimaryButon:hover {{
    background-color: {RENKLER['primary_dark']};
    border: 1px solid {RENKLER['primary_dark']};
}}

QPushButton#BasariButon {{
    background-color: {RENKLER['success']};
    color: #ffffff;
    border: 1px solid {RENKLER['success']};
}}

QPushButton#BasariButon:hover {{
    background-color: #059669;
    border: 1px solid #059669;
}}

QPushButton#IkincilButon {{
    background-color: {RENKLER['card']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['text']};
}}

QPushButton#IkincilButon:hover {{
    background-color: {RENKLER['text']};
    color: #ffffff;
}}

QPushButton#HayaletButon {{
    background-color: transparent;
    color: {RENKLER['text_muted']};
    border: 1px solid {RENKLER['border']};
}}

QPushButton#HayaletButon:hover {{
    background-color: {RENKLER['bg_alt']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['text_muted']};
}}

QPushButton#TehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['border']};
}}

QPushButton#TehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: #ffffff;
    border: 1px solid {RENKLER['danger']};
}}

QPushButton#KucukIkincilButon {{
    background-color: {RENKLER['card']};
    color: {RENKLER['primary']};
    border: 1px solid {RENKLER['primary']};
    padding-left: 12px;
    padding-right: 12px;
    font-size: 10px;
    font-weight: 700;
    border-radius: 4px;
}}

QPushButton#KucukIkincilButon:hover {{
    background-color: {RENKLER['primary']};
    color: #ffffff;
}}

QPushButton#KucukTehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['border']};
    padding-left: 12px;
    padding-right: 12px;
    font-size: 10px;
    font-weight: 700;
    border-radius: 4px;
}}

QPushButton#KucukTehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: #ffffff;
    border: 1px solid {RENKLER['danger']};
}}

/* FORM ALANLARI =================================================== */
QLineEdit, QSpinBox, QDateTimeEdit, QComboBox, QTextEdit {{
    background-color: {RENKLER['card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 6px;
    padding-left: 12px;
    padding-right: 12px;
    color: {RENKLER['text']};
    selection-background-color: {RENKLER['primary']};
    selection-color: #ffffff;
    font-family: "Inter", sans-serif;
    font-size: 13px;
}}

QLineEdit:focus, QSpinBox:focus, QDateTimeEdit:focus,
QComboBox:focus, QTextEdit:focus {{
    border: 1.5px solid {RENKLER['primary']};
    background-color: {RENKLER['card']};
}}

QLineEdit:hover, QSpinBox:hover, QDateTimeEdit:hover,
QComboBox:hover, QTextEdit:hover {{
    border: 1px solid {RENKLER['text_subtle']};
}}

#AramaInput {{
    background-color: {RENKLER['card']};
    border: 1px solid {RENKLER['border']};
    padding-left: 16px;
    padding-right: 16px;
    border-radius: 6px;
    font-family: "Inter", sans-serif;
    font-size: 13px;
    font-weight: 500;
}}

#AramaInput:focus {{
    border: 1.5px solid {RENKLER['primary']};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDateTimeEdit::up-button, QDateTimeEdit::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    background-color: transparent;
    border: none;
    border-left: 1px solid {RENKLER['border']};
    width: 24px;
    padding: 0;
}}

QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDateTimeEdit::up-button:hover, QDateTimeEdit::down-button:hover {{
    background-color: {RENKLER['bg_alt']};
}}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow, QDateTimeEdit::up-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid {RENKLER['text_muted']};
    width: 0;
    height: 0;
}}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow, QDateTimeEdit::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['text_muted']};
    width: 0;
    height: 0;
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['text_muted']};
    margin-right: 12px;
    width: 0;
    height: 0;
}}

QComboBox QAbstractItemView {{
    background-color: {RENKLER['card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 6px;
    selection-background-color: {RENKLER['primary_light']};
    selection-color: {RENKLER['primary_dark']};
    color: {RENKLER['text']};
    padding: 4px;
    outline: 0;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px 10px;
    border-radius: 4px;
    min-height: 22px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {RENKLER['bg_alt']};
}}

QLabel#FormEtiket {{
    color: {RENKLER['text_muted']};
    font-family: "Inter", sans-serif;
    font-size: 11px;
    font-weight: 600;
    background: transparent;
    border: none;
}}

/* TABLOLAR ======================================================== */
QTableWidget {{
    background-color: {RENKLER['card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 8px;
    gridline-color: transparent;
    color: {RENKLER['text']};
    selection-background-color: transparent;
    outline: 0;
    alternate-background-color: {RENKLER['table_zebra']};
}}

QTableWidget::item {{
    padding-left: 8px;
    padding-right: 8px;
    border: none;
    border-bottom: 1px solid {RENKLER['border_light']};
    background-color: transparent;
    color: {RENKLER['text']};
}}

QTableWidget::item:selected {{
    background-color: {RENKLER['primary_pale']};
    color: {RENKLER['text']};
}}

QTableWidget::item:hover {{
    background-color: {RENKLER['table_row_hover']};
}}

QHeaderView::section {{
    background-color: {RENKLER['table_header_bg']};
    color: {RENKLER['table_header_text']};
    padding-top: 12px;
    padding-bottom: 12px;
    padding-left: 14px;
    padding-right: 14px;
    border: none;
    border-bottom: 1px solid {RENKLER['border']};
    font-family: "Inter", sans-serif;
    font-weight: 600;
    font-size: 10px;
    text-transform: uppercase;
}}

QTableCornerButton::section {{
    background-color: {RENKLER['table_header_bg']};
    border: none;
}}

/* SCROLLBAR ======================================================= */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    border: none;
    margin: 4px 2px 4px 2px;
}}

QScrollBar::handle:vertical {{
    background: {RENKLER['text_faint']};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {RENKLER['text_subtle']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    border: none;
    margin: 2px 4px 2px 4px;
}}

QScrollBar::handle:horizontal {{
    background: {RENKLER['text_faint']};
    border-radius: 4px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {RENKLER['text_subtle']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: none;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* DIYALOG ========================================================= */
QDialog {{
    background-color: {RENKLER['bg']};
}}

QMessageBox {{
    background-color: {RENKLER['card']};
}}

QMessageBox QLabel {{
    color: {RENKLER['text']};
    font-family: "Inter", sans-serif;
    font-size: 13px;
    background: transparent;
    border: none;
}}

QMessageBox QPushButton {{
    min-width: 90px;
}}

/* ROZETLER ======================================================== */
QLabel#RozetBasari {{
    background-color: {RENKLER['success_pale']};
    color: {RENKLER['success']};
    border: none;
    border-radius: 4px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 700;
    min-width: 80px;
}}

QLabel#RozetUyari {{
    background-color: {RENKLER['warning_pale']};
    color: #b45309;
    border: none;
    border-radius: 4px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 700;
    min-width: 80px;
}}

QLabel#RozetTehlike {{
    background-color: {RENKLER['danger_pale']};
    color: {RENKLER['danger']};
    border: none;
    border-radius: 4px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 700;
    min-width: 80px;
}}

QLabel#RozetNotr {{
    background-color: {RENKLER['bg_alt']};
    color: {RENKLER['text_muted']};
    border: none;
    border-radius: 4px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 700;
    min-width: 80px;
}}

/* TABWIDGET ======================================================= */
QTabWidget::pane {{
    border: none;
    border-top: 1px solid {RENKLER['border']};
    background-color: {RENKLER['bg']};
}}

QTabBar::tab {{
    background-color: transparent;
    color: {RENKLER['text_muted']};
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 20px;
    font-family: "Inter", sans-serif;
    font-size: 12px;
    font-weight: 600;
}}

QTabBar::tab:selected {{
    color: {RENKLER['primary']};
    border-bottom: 2px solid {RENKLER['primary']};
}}

QTabBar::tab:hover {{
    color: {RENKLER['text']};
}}

/* DIGER =========================================================== */
QFrame#Ayirici {{
    background-color: {RENKLER['border']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}

QFrame#AyiriciInce {{
    background-color: {RENKLER['border_light']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}
"""
