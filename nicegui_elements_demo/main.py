import os
import logging
import uvicorn
import importlib.metadata as metadata
from nicegui import ui
from nicegui import app as nice_app
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s")
logger = logging.getLogger(__name__)

ui.colors(primary='#4f46e5')  # Optional: Setzt die Primärfarbe

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "bg-white",
                "text": "text-gray-900",
                "primary": "bg-blue-500 hover:bg-blue-700",
                "secondary": "bg-gray-500 hover:bg-gray-700",
                "accent": "bg-purple-500 hover:bg-purple-700",
                "card": "bg-white shadow-lg",
                "input": "border border-gray-300 rounded px-4 py-2",
                "select": "border border-gray-300 rounded px-4 py-2",
                "button": "bg-blue-500 hover:bg-blue-700 text-white"
            },
            "dark": {
                "bg": "bg-gray-900",
                "text": "text-white",
                "primary": "bg-blue-600 hover:bg-blue-800",
                "secondary": "bg-gray-600 hover:bg-gray-800",
                "accent": "bg-purple-600 hover:bg-purple-800",
                "card": "bg-gray-800 shadow-lg",
                "input": "border border-gray-600 bg-gray-700 text-white rounded px-4 py-2",
                "select": "border border-gray-600 bg-gray-700 text-white rounded px-4 py-2",
                "button": "bg-blue-600 hover:bg-blue-800 text-white"
            },
            "yellow": {
                "bg": "bg-yellow-50",
                "text": "text-yellow-900",
                "primary": "bg-yellow-500 hover:bg-yellow-700",
                "secondary": "bg-amber-500 hover:bg-amber-700",
                "accent": "bg-orange-500 hover:bg-orange-700",
                "card": "bg-yellow-100 shadow-lg",
                "input": "border border-yellow-300 rounded px-4 py-2",
                "select": "border border-yellow-300 rounded px-4 py-2",
                "button": "bg-yellow-500 hover:bg-yellow-700 text-yellow-900"
            }
        }

    def get_theme(self, theme_name=None):
        """Gibt das ausgewählte Theme oder das aktuelle Theme zurück"""
        return self.themes.get(theme_name or self.current_theme, self.themes["light"])

    def set_theme(self, theme_name):
        """Setzt das aktuelle Theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False

    def get_available_themes(self):
        """Gibt eine Liste aller verfügbaren Themes zurück"""
        return list(self.themes.keys())

theme_manager = ThemeManager()

# Konfigurationsvariablen
STORAGE_SECRET = os.getenv('STORAGE_SECRET', 'your-secret-key')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

# Erstellen einer FastAPI-Anwendung
app = FastAPI()

@app.get("/")
async def root():
    logger.debug("FastAPI Root-Route '/' wurde aufgerufen")
    return RedirectResponse(url="/demo_start")

# Hinzufügen der CORS-Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ersetze "*" durch spezifische IPs, wenn nötig
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.debug("Registriere NiceGUI mit FastAPI")
ui.run_with(
    app,
    title='MyNiceGuiDemo',
    storage_secret=STORAGE_SECRET,
    favicon='🎲',
    dark=False,
    tailwind=True
)


#########################################################################


@ui.page('/')
@ui.page('/demo_start')
def demo_start():
    # Einfache Benutzeroberfläche erstellen
    ui.label("Willkommen zur NiceGUI Elemente Demo App!").classes("text-2xl font-bold")
    ui.button("Klick mich!", on_click=lambda: ui.notify("Button wurde gedrückt!"))

    # Link für /demo_theme in einem neuen Tab
    ui.link(
        "Öffne /demo_theme in neuem Tab",
        '/demo_theme',  # Ziel-Link
        new_tab=True
    ).classes("mt-4 inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded")

    # Link für /demo_styling in einem neuen Tab
    ui.link(
        "Öffne /demo_styling in neuem Tab",
        '/demo_styling',  # Ziel-Link
        new_tab=True
    ).classes("mt-4 inline-block bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded")

    # Link für /demo_compare in einem neuen Tab
    ui.link(
        "Öffne /demo_compare in neuem Tab",
        '/demo_compare',  # Ziel-Link
        new_tab=True
    ).classes("mt-4 inline-block bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded")

    # Link für /demo_screen_quasar in einem neuen Tab
    ui.link(
        "Öffne /demo_screen_quasar in neuem Tab",
        '/demo_screen_quasar',  # Ziel-Link
        new_tab=True
    ).classes("mt-4 inline-block bg-pink-500 hover:bg-pink-700 text-white font-bold py-2 px-4 rounded")

    # Link für /demo_screen_html in einem neuen Tab
    ui.link(
        "Öffne /demo_screen_html in neuem Tab",
        '/demo_screen_html',  # Ziel-Link
        new_tab=True
    ).classes("mt-4 inline-block bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded")


#########################################################################


@ui.page('/demo_theme')
def demo_theme():
    logger.debug("Lade Dashboard Theme-Seite")

    def create_content():
        # Lösche vorherige Inhalte
        container.clear()

        theme = theme_manager.get_theme()

        with container:
            # Header
            with ui.card().classes(f'w-full {theme["card"]}'):
                ui.label("Demo").classes(f'text-2xl font-bold {theme["text"]}')

                # Theme Selector
                ui.select(
                    options=list(theme_manager.themes.keys()),
                    value=theme_manager.current_theme,
                    label="Theme",
                    on_change=lambda e: change_theme(e.value)
                ).classes('w-48')

            # Content
            with ui.card().classes(f'w-full mt-4 {theme["card"]}'):
                ui.label("Inhalt").classes(f'text-xl {theme["text"]}')
                ui.button(
                    "Test Button",
                    on_click=lambda: ui.notify("Button geklickt!")
                ).classes(f'{theme["button"]} px-4 py-2 rounded')

    def change_theme(new_theme):
        logger.debug(f"Ändere Theme auf {new_theme}")
        if theme_manager.set_theme(new_theme):
            create_content()
            ui.notify(f"Theme auf {new_theme} geändert")

    # Hauptcontainer
    container = ui.column().classes('w-full p-4')

    # Initialer Content
    create_content()


#########################################################################


@ui.page('/demo_compare')
def demo_compare():
    logger.debug("Lade Demo Compare-Seite (mit Erklärungen)")

    def create_content():
        container.clear()
        
        with container:
            with ui.card().classes("bg-white shadow rounded p-4 w-full"):
                ui.label("Demo Compare - Vergleich Tailwind & Quasar").classes(
                    "text-2xl font-bold text-gray-800"
                )
                ui.label(
                    """
                    In dieser Version zeigen wir Unterschiede zwischen der Verwendung von Quasar- und TailwindCSS-Komponenten.
                    """
                ).classes("text-lg text-gray-600 mt-2")

            # Hilfeseite mit Vergleich
            ui.label("Unterschiede zwischen Quasar und Tailwind").classes("text-xl text-gray-800 font-bold mt-4")
            ui.html(
                """
                <div class="bg-gray-50 rounded shadow mt-4 p-4">
                    <p class="text-gray-600">
                        <strong>Quasar-Komponenten:</strong>
                    </p>
                    <ul class="list-disc ml-6 text-gray-600">
                        <li>Werden über NiceGUI's ui.button() erstellt</li>
                        <li>Styling erfolgt über .props() und .classes()</li>
                        <li>Haben eigene Theme-Logik</li>
                        <li>Bieten zusätzliche eingebaute Funktionalitäten</li>
                    </ul>
                    
                    <p class="text-gray-600 mt-4">
                        <strong>Tailwind-Komponenten:</strong>
                    </p>
                    <ul class="list-disc ml-6 text-gray-600">
                        <li>Werden als reines HTML gerendert</li>
                        <li>Styling erfolgt ausschließlich über CSS-Klassen</li>
                        <li>Volle Kontrolle über das Aussehen</li>
                        <li>Einfach in andere Projekte zu übernehmen</li>
                    </ul>
                </div>
                """
            )

            # Vergleich von Buttons
            with ui.tabs().classes("w-full mt-4") as tabs:
                ui.tab("Quasar Buttons")
                ui.tab("Tailwind Buttons")

            with ui.tab_panels(tabs):
                # Quasar Buttons
                with ui.tab_panel("Quasar Buttons").classes("p-4"):
                    with ui.column().classes("space-y-6"):
                        # Primary Button Beispiel
                        with ui.card().classes("p-4"):
                            ui.label("Primary Button (Quasar)").classes("font-bold mb-2")
                            with ui.row().classes("items-center gap-4"):
                                ui.button("Quasar Primary Button").props("color=primary")
                                with ui.column().classes("flex-1"):
                                    ui.label("Python-Code:").classes("text-sm text-gray-600")
                                    ui.html('''
                                        <pre class="bg-gray-100 p-2 rounded text-sm">
ui.button("Quasar Primary Button").props("color=primary")</pre>
                                    ''')

                        # Danger Button Beispiel
                        with ui.card().classes("p-4"):
                            ui.label("Danger Button (Quasar)").classes("font-bold mb-2")
                            with ui.row().classes("items-center gap-4"):
                                ui.button("Quasar Danger Button").props("color=red")
                                with ui.column().classes("flex-1"):
                                    ui.label("Python-Code:").classes("text-sm text-gray-600")
                                    ui.html('''
                                        <pre class="bg-gray-100 p-2 rounded text-sm">
ui.button("Quasar Danger Button").props("color=red")</pre>
                                    ''')

                # Tailwind Buttons
                with ui.tab_panel("Tailwind Buttons").classes("p-4"):
                    with ui.column().classes("space-y-6"):
                        # Primary Button Beispiel
                        with ui.card().classes("p-4"):
                            ui.label("Primary Button (Tailwind)").classes("font-bold mb-2")
                            with ui.row().classes("items-center gap-4"):
                                ui.html('''
                                    <button class="bg-blue-500 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700">
                                        Tailwind Primary Button
                                    </button>
                                ''')
                                with ui.column().classes("flex-1"):
                                    ui.label("HTML-Code:").classes("text-sm text-gray-600")
                                    ui.html('''
                                        <pre class="bg-gray-100 p-2 rounded text-sm">
&lt;button class="bg-blue-500 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700"&gt;
    Tailwind Primary Button
&lt;/button&gt;</pre>
                                    ''')
                                    ui.label("Python-Code mit NiceGUI:").classes("text-sm text-gray-600 mt-2")
                                    ui.html('''
                                        <pre class="bg-gray-100 p-2 rounded text-sm">
ui.html("""
    &lt;button class="bg-blue-500 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700"&gt;
        Tailwind Primary Button
    &lt;/button&gt;
""")</pre>
                                    ''')

                        # Danger Button Beispiel
                        with ui.card().classes("p-4"):
                            ui.label("Danger Button (Tailwind)").classes("font-bold mb-2")
                            with ui.row().classes("items-center gap-4"):
                                ui.html('''
                                    <button class="bg-red-500 text-white px-6 py-3 rounded-lg shadow hover:bg-red-700">
                                        Tailwind Danger Button
                                    </button>
                                ''')
                                with ui.column().classes("flex-1"):
                                    ui.label("HTML-Code:").classes("text-sm text-gray-600")
                                    ui.html('''
                                        <pre class="bg-gray-100 p-2 rounded text-sm">
&lt;button class="bg-red-500 text-white px-6 py-3 rounded-lg shadow hover:bg-red-700"&gt;
    Tailwind Danger Button
&lt;/button&gt;</pre>
                                    ''')
                                    ui.label("Python-Code mit NiceGUI:").classes("text-sm text-gray-600 mt-2")
                                    ui.html('''
                                        <pre class="bg-gray-100 p-2 rounded text-sm">
ui.html("""
    &lt;button class="bg-red-500 text-white px-6 py-3 rounded-lg shadow hover:bg-red-700"&gt;
        Tailwind Danger Button
    &lt;/button&gt;
""")</pre>
                                    ''')

    container = ui.column().classes("w-full p-4")
    create_content()


#########################################################################


@ui.page('/demo_screen_quasar')
def demo_screen_quasar():
    # Tailwind und JavaScript für Viewport-Erkennung
    ui.add_head_html('''
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @media (min-width: 768px) {
                .desktop-nav {
                    display: flex !important;
                }
                .mobile-nav-btn {
                    display: none !important;
                }
            }
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                function updateViewport() {
                    const width = window.innerWidth;
                    const height = window.innerHeight;
                    const widthLabel = document.getElementById('width-label');
                    const heightLabel = document.getElementById('height-label');
                    if (widthLabel && heightLabel) {
                        widthLabel.textContent = `Width: ${width}px`;
                        heightLabel.textContent = `Height: ${height}px`;
                    }

                    // Update screen size indicator
                    const indicators = document.querySelectorAll('.screen-indicator');
                    indicators.forEach(ind => ind.style.display = 'none');
                    
                    if (width >= 1536) {
                        document.getElementById('2xl-screen').style.display = 'block';
                    } else if (width >= 1280) {
                        document.getElementById('xl-screen').style.display = 'block';
                    } else if (width >= 1024) {
                        document.getElementById('lg-screen').style.display = 'block';
                    } else if (width >= 768) {
                        document.getElementById('md-screen').style.display = 'block';
                    } else if (width >= 640) {
                        document.getElementById('sm-screen').style.display = 'block';
                    } else {
                        document.getElementById('mobile-screen').style.display = 'block';
                    }
                }
                updateViewport();
                window.addEventListener('resize', updateViewport);
            });
        </script>
    ''')

    logger.debug("Lade Dashboard Screen-Seite (Responsive Testing)")

    def create_responsive_content():
        container.clear()

        with container:
            # Navbar - Basis Quasar
            with ui.row().classes('w-full bg-gray-800 text-white p-4'):
                with ui.row().classes('w-full flex items-center justify-between'):
                    # Logo
                    ui.label("ResponsiveApp Nicegui using Quasar").classes('text-xl font-bold')

                    # Desktop Navigation
                    with ui.row().classes('desktop-nav hidden items-center space-x-6') as desktop_nav:
                        ui.link('Home', '#').classes('text-white hover:text-gray-300')
                        ui.link('About', '#').classes('text-white hover:text-gray-300')
                        ui.link('Services', '#').classes('text-white hover:text-gray-300')
                        ui.link('Contact', '#').classes('text-white hover:text-gray-300')
                    
                    # Hamburger Menu Button
                    with ui.button().classes('mobile-nav-btn text-white') as menu_btn:
                        ui.icon('menu').classes('text-2xl')
                        def toggle_mobile_menu():
                            mobile_menu.visible = not mobile_menu.visible
                            mobile_menu.classes(remove='hidden' if mobile_menu.visible else 'block')
                            mobile_menu.classes(add='block' if mobile_menu.visible else 'hidden')
                        menu_btn.on_click(toggle_mobile_menu)

            # Mobile Navigation Menu - Basis Quasar
            with ui.column().classes('w-full bg-gray-700 text-white hidden') as mobile_menu:
                ui.link('Home', '#').classes('p-4 hover:bg-gray-600 w-full')
                ui.link('About', '#').classes('p-4 hover:bg-gray-600 w-full')
                ui.link('Services', '#').classes('p-4 hover:bg-gray-600 w-full')
                ui.link('Contact', '#').classes('p-4 hover:bg-gray-600 w-full')

            # Image Gallery - Basis Quasar
            with ui.card().classes('mt-4 p-4 bg-white rounded-lg shadow'):
                ui.label('Responsive Grid').classes('text-xl font-bold text-gray-800 mb-4')
                with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4'):
                    for i in range(8):
                        with ui.card().classes('p-4 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow'):
                            # Zufallsbild ohne seed - ändert sich bei jedem Laden
                            ui.image(f'https://picsum.photos/400/300?random={i}').classes('w-full h-48 object-cover rounded-lg mb-3')
                            ui.label(f'Card {i+1}').classes('font-bold text-gray-700')
                            ui.label('Resize to see changes').classes('text-sm text-gray-500')

            # Responsive Table - Basis Quasar
            with ui.card().classes('mt-4 p-4 bg-white rounded-lg shadow overflow-hidden'):
                ui.label('Responsive Table').classes('text-xl font-bold text-gray-800 mb-4')

                # Verwaltung der Tabellendaten
                resp_columns = [
                    {'name': 'header1', 'label': 'Header 1', 'field': 'header1', 'sortable': True},
                    {'name': 'header2', 'label': 'Header 2', 'field': 'header2', 'sortable': True},
                    {'name': 'header3', 'label': 'Header 3', 'field': 'header3', 'sortable': True},
                    {'name': 'header4', 'label': 'Header 4', 'field': 'header4', 'sortable': True}
                ]

                resp_rows = [
                    {'header1': 'Data 1-1', 'header2': 'Data 1-2', 'header3': 'Data 1-3', 'header4': 'Data 1-4'},
                    {'header1': 'Data 2-1', 'header2': 'Data 2-2', 'header3': 'Data 2-3', 'header4': 'Data 2-4'},
                    {'header1': 'Data 3-1', 'header2': 'Data 3-2', 'header3': 'Data 3-3', 'header4': 'Data 3-4'}
                ]

                with ui.element('div').classes('overflow-x-auto'):
                    resp_table = ui.table(
                        columns=resp_columns,
                        rows=resp_rows,
                        row_key='header1'
                    ).classes('min-w-full divide-y divide-gray-200')

                    with ui.row().classes('mt-4 space-x-4'):
                        def add_resp_row():
                            new_row = {col['field']: f'New Data {len(resp_rows)+1}-{i+1}' 
                                      for i, col in enumerate(resp_columns)}
                            resp_rows.append(new_row)
                            resp_table.rows = resp_rows
                            resp_table.update()

                        def remove_resp_row():
                            if resp_rows:
                                resp_rows.pop()
                                resp_table.rows = resp_rows
                                resp_table.update()

                        def add_resp_column():
                            new_col_name = f'header{len(resp_columns)+1}'
                            resp_columns.append({
                                'name': new_col_name,
                                'label': f'Header {len(resp_columns)+1}',
                                'field': new_col_name,
                                'sortable': True
                            })
                            for row in resp_rows:
                                row[new_col_name] = f'New Col Data {len(resp_columns)}'
                            resp_table.columns = resp_columns
                            resp_table.update()

                        def remove_resp_column():
                            if len(resp_columns) > 1:
                                removed_col = resp_columns.pop()
                                for row in resp_rows:
                                    row.pop(removed_col['field'], None)
                                resp_table.columns = resp_columns
                                resp_table.update()

                        ui.button('Add Row', on_click=add_resp_row).classes(
                            'px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600')
                        ui.button('Remove Row', on_click=remove_resp_row).classes(
                            'px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600')
                        ui.button('Add Column', on_click=add_resp_column).classes(
                            'px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600')
                        ui.button('Remove Column', on_click=remove_resp_column).classes(
                            'px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600')

            # Excel-like Tabelle - Basis Quasar
            with ui.card().classes('mt-4 p-4 bg-white rounded-lg shadow'):
                ui.label('Excel-like Table').classes('text-xl font-bold text-gray-800 mb-4')
                
                columns = [
                    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
                    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
                    {'name': 'city', 'label': 'City', 'field': 'city', 'sortable': True},
                    {'name': 'occupation', 'label': 'Occupation', 'field': 'occupation', 'sortable': True}
                ]

                rows = [
                    {'name': 'John Doe', 'age': 30, 'city': 'New York', 'occupation': 'Engineer'},
                    {'name': 'Jane Smith', 'age': 25, 'city': 'London', 'occupation': 'Designer'},
                    {'name': 'Bob Johnson', 'age': 35, 'city': 'Paris', 'occupation': 'Manager'},
                    {'name': 'Alice Brown', 'age': 28, 'city': 'Berlin', 'occupation': 'Developer'}
                ]

                # Filter-State und Originaldaten
                original_rows = rows.copy()
                filter_inputs = {}

                # Filter-Zeile erstellen
                with ui.row().classes('w-full gap-4 mb-4'):
                    for col in columns:
                        filter_inputs[col['field']] = ui.input(
                            placeholder=f'Filter {col["label"]}'
                        ).classes('px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500')

                with ui.element('div').classes('overflow-x-auto'):
                    table = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key='name'
                    ).classes('min-w-full border-collapse border border-gray-200')

                    # Filter-Funktion
                    def apply_filters():
                        filtered_rows = original_rows.copy()
                        for field, input_elem in filter_inputs.items():
                            if input_elem.value:
                                filtered_rows = [
                                    row for row in filtered_rows
                                    if str(row[field]).lower().startswith(str(input_elem.value).lower())
                                ]
                        table.rows = filtered_rows
                        table.update()

                    # Filter-Handler für alle Inputs
                    for input_elem in filter_inputs.values():
                        input_elem.on('change', apply_filters)

                    with ui.row().classes('mt-4 space-x-4'):
                        def add_row():
                            new_row = {col['field']: '' for col in columns}
                            new_row['name'] = f'New Entry {len(original_rows)}'
                            original_rows.append(new_row)
                            apply_filters()  # Wende aktuelle Filter an

                        def remove_last_row():
                            if len(original_rows) > 0:
                                original_rows.pop()
                                apply_filters()  # Wende aktuelle Filter an

                        def add_column():
                            new_col_name = f'column_{len(columns)}'
                            new_col = {
                                'name': new_col_name,
                                'label': f'New Column {len(columns)}',
                                'field': new_col_name,
                                'sortable': True
                            }
                            columns.append(new_col)
                            
                            # Neue Spalte zu allen Zeilen hinzufügen
                            for row in original_rows:
                                row[new_col_name] = ''
                            
                            # Neuen Filter hinzufügen
                            filter_inputs[new_col_name] = ui.input(
                                placeholder=f'Filter {new_col["label"]}'
                            ).classes('px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500')
                            filter_inputs[new_col_name].on('change', apply_filters)
                            
                            table.columns = columns
                            apply_filters()

                        def remove_last_column():
                            if len(columns) > 1:
                                removed_col = columns.pop()
                                # Spalte aus allen Zeilen entfernen
                                for row in original_rows:
                                    row.pop(removed_col['field'], None)
                                
                                # Filter entfernen
                                if removed_col['field'] in filter_inputs:
                                    filter_inputs[removed_col['field']].delete()
                                    del filter_inputs[removed_col['field']]
                                
                                table.columns = columns
                                apply_filters()

                        # Clear Filter Button hinzufügen
                        def clear_filters():
                            for input_elem in filter_inputs.values():
                                input_elem.value = ''
                            table.rows = original_rows
                            table.update()

                        ui.button('Add Row', on_click=add_row).classes(
                            'px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600')
                        ui.button('Remove Row', on_click=remove_last_row).classes(
                            'px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600')
                        ui.button('Add Column', on_click=add_column).classes(
                            'px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600')
                        ui.button('Remove Column', on_click=remove_last_column).classes(
                            'px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600')
                        ui.button('Clear Filters', on_click=clear_filters).classes(
                            'px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600')

            # Contact Form - Basis Quasar
            with ui.card().classes('mt-4 p-4 bg-white rounded-lg shadow'):
                ui.label('Contact Form').classes('text-xl font-bold text-gray-800 mb-4')
                with ui.element('div').classes('space-y-4'):
                    with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-4'):
                        ui.input(placeholder='Name').classes('w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500')
                        ui.input(placeholder='Email').classes('w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500')
                    ui.textarea(placeholder='Message').classes('w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500')
                    ui.button('Send Message').classes('w-full md:w-auto px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors')

            # Screen Size Display - Basis Tailwind-CSS/HTML
            with ui.card().classes('mt-4 p-4 bg-blue-100'):
                ui.label('Aktuelle Bildschirmgröße (HTML):').classes('font-bold')
                with ui.element('div').classes('mt-2'):
                    ui.html('''
                        <div id="mobile-screen" class="screen-indicator">Mobile (<640px)</div>
                        <div id="sm-screen" class="screen-indicator">SM (640px - 767px)</div>
                        <div id="md-screen" class="screen-indicator">MD (768px - 1023px)</div>
                        <div id="lg-screen" class="screen-indicator">LG (1024px - 1279px)</div>
                        <div id="xl-screen" class="screen-indicator">XL (1280px - 1535px)</div>
                        <div id="2xl-screen" class="screen-indicator">2XL (≥1536px)</div>
                    ''')

            # Viewport Size Display - Basis Tailwind-CSS/HTML
            ui.html('''
                <div class="fixed bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg">
                    <div class="font-bold text-gray-700">Viewport Size (HTML)</div>
                    <div class="flex space-x-2">
                        <span id="width-label" class="text-sm text-gray-600">Width: --</span>
                        <span class="text-sm text-gray-600">×</span>
                        <span id="height-label" class="text-sm text-gray-600">Height: --</span>
                    </div>
                </div>
            ''')

    # Hauptcontainer
    container = ui.column().classes('w-full min-h-screen bg-gray-100')
    create_responsive_content()


#########################################################################


@ui.page('/demo_screen_html')
def demo_screen_html():
    # Tailwind und JavaScript für Viewport-Erkennung
    ui.add_head_html('''
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @media (min-width: 768px) {
                .desktop-nav { display: block !important; }
                .mobile-nav-btn { display: none !important; }
                .mobile-menu { display: none !important; }
            .nicegui-table {
                border: 1px solid #e5e7eb;
            }
            .nicegui-table th {
                background-color: #f9fafb;
                padding: 12px;
                border: 1px solid #e5e7eb;
                font-weight: 600;
            }
            .nicegui-table td {
                padding: 12px;
                border: 1px solid #e5e7eb;
            }
            .nicegui-table tr:hover {
                background-color: #f3f4f6;
            }
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                function updateViewport() {
                    const width = window.innerWidth;
                    const height = window.innerHeight;
                    const widthLabel = document.getElementById('width-label');
                    const heightLabel = document.getElementById('height-label');
                    if (widthLabel && heightLabel) {
                        widthLabel.textContent = `Width: ${width}px`;
                        heightLabel.textContent = `Height: ${height}px`;
                    }

                    // Update screen size indicator
                    const indicators = document.querySelectorAll('.screen-indicator');
                    indicators.forEach(ind => ind.style.display = 'none');
                    
                    if (width >= 1536) {
                        document.getElementById('2xl-screen').style.display = 'block';
                    } else if (width >= 1280) {
                        document.getElementById('xl-screen').style.display = 'block';
                    } else if (width >= 1024) {
                        document.getElementById('lg-screen').style.display = 'block';
                    } else if (width >= 768) {
                        document.getElementById('md-screen').style.display = 'block';
                    } else if (width >= 640) {
                        document.getElementById('sm-screen').style.display = 'block';
                    } else {
                        document.getElementById('mobile-screen').style.display = 'block';
                    }
                }
                updateViewport();
                window.addEventListener('resize', updateViewport);
            });
        </script>
    ''')

    # JavaScript im Body
    ui.add_body_html('''
        <script>
            function toggleMobileMenu() {
                const mobileMenu = document.getElementById('mobile-menu');
                mobileMenu.classList.toggle('hidden');
            }

            window.addEventListener('resize', function() {
                if (window.innerWidth >= 768) {
                    const mobileMenu = document.getElementById('mobile-menu');
                    mobileMenu.classList.add('hidden');
                }
            });
        </script>
    ''')

    logger.debug("Lade Dashboard Screen-Seite (Responsive Testing)")

    # Hauptcontainer für Navigation
    nav_html = '''
        <nav class="w-full bg-gray-800 text-white">
            <!-- Desktop & Mobile Navigation Container -->
            <div class="px-4 py-3">
                <div class="flex items-center justify-between">
                    <!-- Logo/Title -->
                    <div class="text-xl font-bold">
                        ResponsiveApp Nicegui using Tailwind-CSS/HTML
                    </div>

                    <!-- Desktop Navigation -->
                    <div class="desktop-nav hidden md:flex items-center space-x-6">
                        <a href="#" class="text-white hover:text-gray-300 transition-colors">Home</a>
                        <a href="#" class="text-white hover:text-gray-300 transition-colors">About</a>
                        <a href="#" class="text-white hover:text-gray-300 transition-colors">Services</a>
                        <a href="#" class="text-white hover:text-gray-300 transition-colors">Contact</a>
                    </div>

                    <!-- Mobile Menu Button -->
                    <button class="mobile-nav-btn md:hidden text-white hover:text-gray-300" 
                            onclick="toggleMobileMenu()">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                  d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Mobile Navigation Menu -->
            <div id="mobile-menu" class="hidden md:hidden bg-gray-700">
                <a href="#" class="block px-4 py-3 text-white hover:bg-gray-600 transition-colors">Home</a>
                <a href="#" class="block px-4 py-3 text-white hover:bg-gray-600 transition-colors">About</a>
                <a href="#" class="block px-4 py-3 text-white hover:bg-gray-600 transition-colors">Services</a>
                <a href="#" class="block px-4 py-3 text-white hover:bg-gray-600 transition-colors">Contact</a>
            </div>
        </nav>
    '''

    def create_responsive_content():
        container.clear()

        with container:
            # Navbar - Basis Tailwind-CSS/HTML
            ui.html(nav_html)

            # Image Gallery - Basis Tailwind-CSS/HTML
            with ui.card().classes('mt-4 p-4 bg-white rounded-lg shadow'):
                ui.label('Responsive Grid').classes('text-xl font-bold text-gray-800 mb-4')
                
                grid_html = '''
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                '''
                
                # Generiere 8 Image Cards
                for i in range(8):
                    grid_html += f'''
                        <div class="p-4 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300 ease-in-out">
                            <img src="https://picsum.photos/400/300?random={i}" 
                                 class="w-full h-48 object-cover rounded-lg mb-3"
                                 alt="Random image {i+1}">
                            <h3 class="font-bold text-gray-700">Card {i+1}</h3>
                            <p class="text-sm text-gray-500">Resize to see changes</p>
                        </div>
                    '''
                
                grid_html += '</div>'
                
                ui.html(grid_html)

            # Responsive Table - Basis Tailwind-CSS/HTML
            with ui.card().classes('mt-4 p-4 bg-white rounded-lg shadow overflow-hidden'):
                ui.label('Responsive Table').classes('text-xl font-bold text-gray-800 mb-4')

            # State für die HTML-Tabelle
            table_state = {
                'headers': ['Header 1', 'Header 2', 'Header 3', 'Header 4'],
                'rows': [
                    ['Data 1-1', 'Data 1-2', 'Data 1-3', 'Data 1-4'],
                    ['Data 2-1', 'Data 2-2', 'Data 2-3', 'Data 2-4'],
                    ['Data 3-1', 'Data 3-2', 'Data 3-3', 'Data 3-4']
                ]
            }

            def generate_table_html():
                # Header generieren
                headers_html = f'''
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        {table_state['headers'][0]}
                    </th>
                '''
                
                for i, header in enumerate(table_state['headers'][1:], 1):
                    headers_html += f'''
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase table-cell">
                            {header}
                        </th>
                    '''

                # Zeilen generieren
                rows_html = ''
                for row in table_state['rows']:
                    # Erste Spalte
                    cells_html = f'''
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {row[0]}
                        </td>
                    '''
                    
                    # Weitere Spalten
                    for cell in row[1:]:
                        cells_html += f'''
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 table-cell">
                                {cell}
                            </td>
                        '''
                    
                    rows_html += f'<tr class="hover:bg-gray-50">{cells_html}</tr>'

                return f'''
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>{headers_html}</tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                {rows_html}
                            </tbody>
                        </table>
                    </div>
                '''

            table_container = ui.html()

            def update_table():
                table_container.set_content(generate_table_html())

            with ui.row().classes('mt-4 space-x-4'):
                def add_row():
                    new_row = [f'Data {len(table_state["rows"])+1}-{i+1}' 
                              for i in range(len(table_state["headers"]))]
                    table_state['rows'].append(new_row)
                    update_table()

                def remove_row():
                    if table_state['rows']:
                        table_state['rows'].pop()
                        update_table()

                def add_column():
                    col_index = len(table_state['headers'])
                    table_state['headers'].append(f'Header {col_index + 1}')
                    
                    for i, row in enumerate(table_state['rows']):
                        row.append(f'Data {i+1}-{col_index + 1}')
                    
                    update_table()

                def remove_column():
                    if len(table_state['headers']) > 1:
                        table_state['headers'].pop()
                        for row in table_state['rows']:
                            row.pop()
                        update_table()

                ui.button('Add Row', on_click=add_row).classes(
                    'px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600')
                ui.button('Remove Row', on_click=remove_row).classes(
                    'px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600')
                ui.button('Add Column', on_click=add_column).classes(
                    'px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600')
                ui.button('Remove Column', on_click=remove_column).classes(
                    'px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600')

            # Initiale Tabellenaktualisierung
            update_table()

            # Excel-like Tabelle - Basis Tailwind-CSS/HTML
            with ui.card().classes('mt-4 p-4 bg-white rounded-lg shadow'):
                ui.label('Excel-like Table').classes('text-xl font-bold text-gray-800 mb-4')
                
            # Erweiterter State für die HTML-Tabelle
            html_table_state = {
                'columns': [
                    {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
                    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
                    {'name': 'city', 'label': 'City', 'field': 'city', 'sortable': True},
                    {'name': 'occupation', 'label': 'Occupation', 'field': 'occupation', 'sortable': True}
                ],
                'rows': [
                    {'name': 'John Doe', 'age': 30, 'city': 'New York', 'occupation': 'Engineer'},
                    {'name': 'Jane Smith', 'age': 25, 'city': 'London', 'occupation': 'Designer'},
                    {'name': 'Bob Johnson', 'age': 35, 'city': 'Paris', 'occupation': 'Manager'},
                    {'name': 'Alice Brown', 'age': 28, 'city': 'Berlin', 'occupation': 'Developer'}
                ],
                'sort_column': '',
                'sort_direction': 'asc',
                'filters': {}
            }

            # Filter-Inputs erstellen
            filter_inputs = {}
            with ui.row().classes('w-full gap-4 mb-4'):
                for col in html_table_state['columns']:
                    filter_inputs[col['field']] = ui.input(
                        placeholder=f'Filter {col["label"]}'
                    ).classes('px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500')

            # Sortier-Buttons erstellen
            sort_buttons = {}
            with ui.row().classes('w-full gap-4 mb-4'):
                for col in html_table_state['columns']:
                    if col.get('sortable'):
                        sort_buttons[col['field']] = ui.button(
                            f'Sort by {col["label"]}',
                            icon='arrow_upward'
                        ).classes('px-2 py-1 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded')

            def generate_excel_table_html():
                # Gefilterte und sortierte Zeilen
                filtered_rows = html_table_state['rows']
                
                # Filtern
                for field, input_elem in filter_inputs.items():
                    if input_elem.value:
                        filtered_rows = [row for row in filtered_rows 
                                       if str(row[field]).lower().startswith(str(input_elem.value).lower())]
                
                # Sortieren
                if html_table_state['sort_column']:
                    reverse = html_table_state['sort_direction'] == 'desc'
                    filtered_rows = sorted(
                        filtered_rows,
                        key=lambda x: str(x[html_table_state['sort_column']]),
                        reverse=reverse
                    )

                # Header generieren
                headers_html = '<tr>'
                for col in html_table_state['columns']:
                    sort_indicator = ''
                    if col['field'] == html_table_state['sort_column']:
                        sort_indicator = '↑' if html_table_state['sort_direction'] == 'asc' else '↓'
                    headers_html += f'''
                        <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            {col['label']} {sort_indicator}
                        </th>
                    '''
                headers_html += '</tr>'

                # Zeilen HTML generieren
                rows_html = ''
                for row in filtered_rows:
                    cells_html = ''
                    for col in html_table_state['columns']:
                        cells_html += f'''
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                <input type="text" 
                                       value="{row[col['field']]}"
                                       class="w-full bg-transparent border-0 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 rounded-md"
                                >
                            </td>
                        '''
                    rows_html += f'<tr class="hover:bg-gray-50">{cells_html}</tr>'

                return f'''
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200 border border-gray-200">
                            <thead class="bg-gray-50">
                                {headers_html}
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                {rows_html}
                            </tbody>
                        </table>
                    </div>
                '''

            table_container = ui.html()

            def update_excel_table():
                table_container.set_content(generate_excel_table_html())

            # Filter-Handler
            for field, input_elem in filter_inputs.items():
                input_elem.on('change', lambda: update_excel_table())

            # Sort-Handler
            def create_sort_handler(column):
                def handler():
                    if html_table_state['sort_column'] == column:
                        html_table_state['sort_direction'] = 'desc' if html_table_state['sort_direction'] == 'asc' else 'asc'
                    else:
                        html_table_state['sort_column'] = column
                        html_table_state['sort_direction'] = 'asc'
                    update_excel_table()
                return handler

            for field, button in sort_buttons.items():
                button.on('click', create_sort_handler(field))

            with ui.row().classes('mt-4 space-x-4'):
                def add_excel_row():
                    new_row = {col['field']: f'New {col["field"]} {len(html_table_state["rows"])}' 
                              for col in html_table_state['columns']}
                    html_table_state['rows'].append(new_row)
                    update_excel_table()

                def remove_excel_row():
                    if html_table_state['rows']:
                        html_table_state['rows'].pop()
                        update_excel_table()

                def add_excel_column():
                    new_col_name = f'column_{len(html_table_state["columns"])}'
                    new_col = {
                        'name': new_col_name,
                        'label': f'New Column {len(html_table_state["columns"])}',
                        'field': new_col_name,
                        'sortable': True
                    }
                    html_table_state['columns'].append(new_col)
                    
                    # Neuen Filter hinzufügen
                    filter_inputs[new_col_name] = ui.input(
                        placeholder=f'Filter {new_col["label"]}'
                    ).classes('px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500')
                    filter_inputs[new_col_name].on('change', lambda: update_excel_table())
                    
                    # Neuen Sort-Button hinzufügen
                    sort_buttons[new_col_name] = ui.button(
                        f'Sort by {new_col["label"]}',
                        icon='arrow_upward'
                    ).classes('px-2 py-1 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded')
                    sort_buttons[new_col_name].on('click', create_sort_handler(new_col_name))
                    
                    # Daten aktualisieren
                    for row in html_table_state['rows']:
                        row[new_col_name] = f'New Value {len(html_table_state["columns"])}'
                    
                    update_excel_table()

                def remove_excel_column():
                    if len(html_table_state['columns']) > 1:
                        removed_col = html_table_state['columns'].pop()
                        # Filter und Sort-Button entfernen
                        if removed_col['field'] in filter_inputs:
                            filter_inputs[removed_col['field']].delete()
                            del filter_inputs[removed_col['field']]
                        if removed_col['field'] in sort_buttons:
                            sort_buttons[removed_col['field']].delete()
                            del sort_buttons[removed_col['field']]
                        # Daten aktualisieren
                        for row in html_table_state['rows']:
                            row.pop(removed_col['field'], None)
                        update_excel_table()

                ui.button('Add Row', on_click=add_excel_row).classes(
                    'px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600')
                ui.button('Remove Row', on_click=remove_excel_row).classes(
                    'px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600')
                ui.button('Add Column', on_click=add_excel_column).classes(
                    'px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600')
                ui.button('Remove Column', on_click=remove_excel_column).classes(
                    'px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600')

            # Initiale Tabellenaktualisierung
            update_excel_table()

            # Contact Form - Basis Tailwind-CSS/HTML
            with ui.card().classes('mt-4 p-4 bg-white rounded-lg shadow'):
                ui.label('Contact Form').classes('text-xl font-bold text-gray-800 mb-4')
                
                form_html = '''
                    <form class="space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <input type="text" 
                                   placeholder="Name" 
                                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none">
                            
                            <input type="email" 
                                   placeholder="Email" 
                                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none">
                        </div>
                        
                        <textarea placeholder="Message" 
                                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none min-h-[100px]">
                        </textarea>
                        
                        <button type="button" 
                                class="w-full md:w-auto px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
                            Send Message
                        </button>
                    </form>
                '''
                
                ui.html(form_html)

            # Screen Size Display - Basis Tailwind-CSS/HTML
            with ui.card().classes('mt-4 p-4 bg-blue-100'):
                ui.label('Aktuelle Bildschirmgröße:').classes('font-bold')
                with ui.element('div').classes('mt-2'):
                    ui.html('''
                        <div id="mobile-screen" class="screen-indicator">Mobile (<640px)</div>
                        <div id="sm-screen" class="screen-indicator">SM (640px - 767px)</div>
                        <div id="md-screen" class="screen-indicator">MD (768px - 1023px)</div>
                        <div id="lg-screen" class="screen-indicator">LG (1024px - 1279px)</div>
                        <div id="xl-screen" class="screen-indicator">XL (1280px - 1535px)</div>
                        <div id="2xl-screen" class="screen-indicator">2XL (≥1536px)</div>
                    ''')

            # Viewport Size Display - Basis Tailwind-CSS/HTML
            ui.html('''
                <div class="fixed bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg">
                    <div class="font-bold text-gray-700">Viewport Size</div>
                    <div class="flex space-x-2">
                        <span id="width-label" class="text-sm text-gray-600">Width: --</span>
                        <span class="text-sm text-gray-600">×</span>
                        <span id="height-label" class="text-sm text-gray-600">Height: --</span>
                    </div>
                </div>
            ''')

    # Hauptcontainer
    container = ui.element('div').classes('w-full min-h-screen bg-gray-100')
    create_responsive_content()


#########################################################################

@ui.page('/demo_styling')
def demo_styling():
    logger.debug("Lade Demo Styling Seite (Tailwind-CSS / HTML)")

    # Element-Typen und ihre Styling-Optionen
    ELEMENT_TYPES = {
        "Button": {
            "preview": """<button class="{classes}">Button Text</button>""",
            "options": {
                "colors": [
                    "bg-blue-500 text-white",
                    "bg-red-500 text-white",
                    "bg-green-500 text-white",
                    "bg-yellow-500 text-black",
                    "bg-purple-500 text-white",
                    "bg-pink-500 text-white"
                ],
                "sizes": ["p-2", "p-4", "p-6"],
                "font_sizes": ["text-sm", "text-base", "text-lg", "text-xl", "text-2xl"],
                "font_weights": ["font-normal", "font-medium", "font-semibold", "font-bold"],
                "font_families": ["font-sans", "font-serif", "font-mono"],
                "border_radius": ["rounded-none", "rounded-sm", "rounded", "rounded-lg", "rounded-full"],
                "shadows": ["shadow-none", "shadow-sm", "shadow", "shadow-md", "shadow-lg"],
                "animations": ["none", "animate-pulse", "animate-bounce", "hover:scale-105 transition-transform"]
            }
        },
        "Input": {
            "preview": """<input type="text" class="{classes}" placeholder="Eingabefeld">""",
            "options": {
                "colors": ["bg-white", "bg-gray-50", "bg-blue-50"],
                "border_colors": ["border-gray-300", "border-blue-300", "border-red-300"],
                "border_styles": ["border", "border-2", "border-dashed"],
                "padding": ["p-2", "p-3", "p-4"],
                "width": ["w-full", "w-64", "w-48", "w-32"],
                "focus_effects": [
                    "focus:ring-2 focus:ring-blue-500",
                    "focus:border-blue-500",
                    "focus:shadow-outline"
                ],
                "states": ["hover:border-blue-500", "disabled:bg-gray-100"]
            }
        },
        "Checkbox": {
            "preview": """
            <div class="flex items-center">
                <input type="checkbox" class="{classes}">
                <span class="ml-2">Checkbox Label</span>
            </div>
            """,
            "options": {
                "sizes": ["w-4 h-4", "w-5 h-5", "w-6 h-6"],
                "colors": ["text-blue-600", "text-red-600", "text-green-600"],
                "border_colors": ["border-gray-300", "border-blue-300"],
                "focus_effects": ["focus:ring-2", "focus:ring-offset-2"],
                "hover_effects": ["hover:border-blue-500"]
            }
        },
        "Radio": {
            "preview": """
            <div class="flex items-center">
                <input type="radio" class="{classes}">
                <span class="ml-2">Radio Label</span>
            </div>
            """,
            "options": {
                "sizes": ["w-4 h-4", "w-5 h-5", "w-6 h-6"],
                "colors": ["text-blue-600", "text-red-600", "text-green-600"],
                "border_colors": ["border-gray-300", "border-blue-300"],
                "focus_effects": ["focus:ring-2", "focus:ring-offset-2"],
                "hover_effects": ["hover:border-blue-500"]
            }
        },
        "Toggle": {
            "preview": """
            <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" class="sr-only peer">
                <div class="{classes}"></div>
                <span class="ml-3">Toggle Switch</span>
            </label>
            """,
            "options": {
                "base_classes": [
                    "w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all",
                    "w-14 h-7 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all"
                ],
                "colors": [
                    "peer-checked:bg-blue-600",
                    "peer-checked:bg-green-600",
                    "peer-checked:bg-red-600"
                ],
                "focus_effects": ["peer-focus:ring-4", "peer-focus:outline-none"]
            }
        },
        "Navigation": {
            "preview": """
            <nav class="{classes}">
                <a href="#" class="px-4 py-2">Home</a>
                <a href="#" class="px-4 py-2">About</a>
                <a href="#" class="px-4 py-2">Contact</a>
            </nav>
            """,
            "options": {
                "layout": ["flex", "flex flex-col", "inline-flex"],
                "colors": ["bg-white", "bg-gray-100", "bg-blue-500"],
                "text_colors": ["text-gray-600", "text-white"],
                "spacing": ["space-x-4", "space-y-2"],
                "padding": ["p-2", "p-4"],
                "border_styles": ["border-b", "border-r", "border-none"],
                "shadows": ["shadow-none", "shadow-sm", "shadow"]
            }
        },
        "Tabs": {
            "preview": """
            <div class="{classes}">
                <button class="px-4 py-2 bg-white">Tab 1</button>
                <button class="px-4 py-2">Tab 2</button>
                <button class="px-4 py-2">Tab 3</button>
            </div>
            """,
            "options": {
                "layout": ["flex", "inline-flex"],
                "colors": ["bg-gray-100", "bg-blue-100"],
                "active_tab": ["bg-white", "bg-blue-500 text-white"],
                "border_styles": ["border-b", "rounded-t"],
                "spacing": ["space-x-1", "space-x-2"],
                "hover_effects": ["hover:bg-gray-50", "hover:text-blue-600"]
            }
        },
        "Message": {
            "preview": """
            <div class="{classes}">
                <p>This is a message text</p>
            </div>
            """,
            "options": {
                "types": [
                    "bg-blue-100 text-blue-700",
                    "bg-red-100 text-red-700",
                    "bg-green-100 text-green-700",
                    "bg-yellow-100 text-yellow-700"
                ],
                "padding": ["p-2", "p-4"],
                "border_radius": ["rounded", "rounded-lg"],
                "border_styles": ["border-l-4", "border"],
                "icons": ["with-icon", "no-icon"]
            }
        },
        "Card": {
            "preview": """
            <div class="{classes}">
                <h3 class="text-lg font-bold mb-2">Card Title</h3>
                <p>Card content goes here.</p>
            </div>
            """,
            "options": {
                "colors": [
                    "bg-white",
                    "bg-gray-50",
                    "bg-gray-100",
                    "bg-blue-50",
                    "bg-red-50"
                ],
                "border_colors": [
                    "border-gray-200",
                    "border-blue-200",
                    "border-red-200",
                    "border-green-200"
                ],
                "border_widths": ["border", "border-2", "border-4"],
                "padding": ["p-2", "p-4", "p-6", "p-8"],
                "border_radius": ["rounded-none", "rounded-sm", "rounded", "rounded-lg"],
                "shadows": ["shadow-none", "shadow-sm", "shadow", "shadow-md", "shadow-lg"],
                "width": ["w-full", "w-1/2", "w-1/3", "w-1/4"]
            }
        },
        "Notification": {
            "preview": """
            <div class="{classes}">
                <strong>Title</strong>
                <p>Notification content</p>
            </div>
            """,
            "options": {
                "types": [
                    "bg-white border-l-4 border-blue-500",
                    "bg-white border-l-4 border-red-500",
                    "bg-white border-l-4 border-green-500"
                ],
                "padding": ["p-4", "p-6"],
                "shadows": ["shadow-md", "shadow-lg"],
                "animations": ["animate-slide-in", "animate-fade"]
            }
        },
        "Loading": {
            "preview": """
            <div class="{classes}">
                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            </div>
            """,
            "options": {
                "sizes": ["h-4 w-4", "h-8 w-8", "h-12 w-12"],
                "colors": ["text-blue-600", "text-gray-600", "text-white"],
                "types": ["spinner", "dots", "bar"],
                "animations": ["animate-spin", "animate-pulse"]
            }
        },
        "Modal": {
            "preview": """
            <div class="{classes}">
                <div class="bg-white p-4 rounded-lg">
                    <h3 class="text-lg font-bold">Modal Title</h3>
                    <p>Modal content goes here</p>
                </div>
            </div>
            """,
            "options": {
                "backdrop": [
                    "bg-black bg-opacity-50",
                    "bg-gray-500 bg-opacity-75"
                ],
                "position": ["fixed inset-0", "absolute inset-x-0 top-0"],
                "animations": ["animate-fade-in", "animate-slide-up"],
                "width": ["max-w-md", "max-w-lg", "max-w-xl"],
                "padding": ["p-4", "p-6"]
            }
        },
        "Accordion": {
            "preview": """
            <div class="{classes}">
                <div class="border-b">
                    <button class="w-full text-left py-4">Section 1</button>
                    <div class="pb-4">Content 1</div>
                </div>
            </div>
            """,
            "options": {
                "colors": ["bg-white", "bg-gray-50"],
                "border_styles": ["border", "border-t-0"],
                "text_colors": ["text-gray-900", "text-blue-600"],
                "hover_effects": ["hover:bg-gray-50"],
                "transitions": ["transition-all duration-200"]
            }
        },
        "Table": {
            "preview": """
            <table class="{classes}">
                <thead class="thead-classes">
                    <tr>
                        <th class="px-4 py-2 header-cell-classes">Header 1</th>
                        <th class="px-4 py-2 header-cell-classes">Header 2</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="row-classes">
                        <td class="px-4 py-2 cell-classes">Data 1</td>
                        <td class="px-4 py-2 cell-classes">Data 2</td>
                    </tr>
                </tbody>
            </table>
            """,
            "options": {
                "table_layout": ["w-full", "min-w-full"],
                "table_borders": [
                    "border-collapse border border-gray-300",
                    "border-separate border border-gray-300"
                ],
                "row_style": ["even:bg-gray-50", "odd:bg-gray-50"],
                "row_hover": ["hover:bg-gray-100"],
                "header_style": ["bg-gray-100", "bg-gray-200"],
                "cell_padding": ["px-4 py-2", "px-6 py-3"]
            }
        }
    }

    def create_content():
        container.clear()
        theme = theme_manager.get_theme()
        
        with container:
            with ui.card().classes(f'w-full {theme["card"]} p-4'):
                ui.label("Nicegui Tailwind-CSS / HTML Elements Styling Demo").classes(f'text-2xl font-bold {theme["text"]}')
                ui.label("Wähle ein Element und passe dessen Styling an").classes(f'text-lg {theme["text"]} mb-4')
                
                # Theme Selector
                ui.select(
                    options=list(theme_manager.themes.keys()),
                    value=theme_manager.current_theme,
                    label="Theme wählen",
                    on_change=lambda e: change_theme_full(e.value)
                ).classes('w-48 mb-8')
                # Element-Typ Selector und Styling-Bereich
                def update_styling_options(e):
                    options_container.clear()
                    preview_container.clear()
                    
                    selected_element = e.value
                    element_config = ELEMENT_TYPES[selected_element]
                    
                    with options_container:
                        current_classes = {}
                        
                        def update_preview():
                            preview_container.clear()
    
                            # Kombiniere alle ausgewählten Klassen
                            all_classes = " ".join(current_classes.values())
    
                            with preview_container:
                                with ui.card().classes(f'{theme["card"]} p-4 mt-4'):
                                    ui.label("Preview:").classes("font-bold mb-4")
                                    ui.html(element_config["preview"].format(classes=all_classes))
        
                                with ui.card().classes(f'{theme["card"]} p-4 mt-4'):
                                    ui.label("Generated Code:").classes("font-bold mb-2")
            
                                    # Generate NiceGUI code based on element type
                                    nicegui_code = ""
                                    if selected_element == "Button":
                                        nicegui_code = f'ui.button("Button Text").classes("{all_classes}")'
            
                                    elif selected_element == "Input":
                                        nicegui_code = f'ui.input(placeholder="Eingabefeld").classes("{all_classes}")'
            
                                    elif selected_element == "Checkbox":
                                        nicegui_code = f'''with ui.row().classes("flex items-center"):
    ui.checkbox().classes("{all_classes}")
    ui.label("Checkbox Label").classes("ml-2")'''
            
                                    elif selected_element == "Radio":
                                        nicegui_code = f'''with ui.row().classes("flex items-center"):
    ui.radio().classes("{all_classes}")
    ui.label("Radio Label").classes("ml-2")'''
            
                                    elif selected_element == "Toggle":
                                        nicegui_code = f'''with ui.row().classes("flex items-center"):
    ui.toggle().classes("{all_classes}")
    ui.label("Toggle Switch").classes("ml-3")'''
            
                                    elif selected_element == "Navigation":
                                        nicegui_code = f'''with ui.row().classes("{all_classes}"):
    ui.link("Home", "/").classes("px-4 py-2")
    ui.link("About", "/about").classes("px-4 py-2")
    ui.link("Contact", "/contact").classes("px-4 py-2")'''
            
                                    elif selected_element == "Tabs":
                                        nicegui_code = f'''with ui.tabs().classes("{all_classes}"):
    ui.tab("Tab 1")
    ui.tab("Tab 2")
    ui.tab("Tab 3")'''
            
                                    elif selected_element == "Message":
                                        nicegui_code = f'''with ui.card().classes("{all_classes}"):
    ui.label("This is a message text")'''
            
                                    elif selected_element == "Card":
                                        nicegui_code = f'''with ui.card().classes("{all_classes}"):
    ui.label("Card Title").classes("text-lg font-bold mb-2")
    ui.label("Card content goes here.")'''
            
                                    elif selected_element == "Notification":
                                        nicegui_code = f'''with ui.card().classes("{all_classes}"):
    ui.label("Title").classes("font-bold")
    ui.label("Notification content")'''
            
                                    elif selected_element == "Loading":
                                        nicegui_code = f'ui.spinner().classes("{all_classes}")'
            
                                    elif selected_element == "Modal":
                                        nicegui_code = f'''def show_modal():
    with ui.dialog().classes("{all_classes}") as dialog:
        with ui.card():
            ui.label("Modal Title").classes("text-lg font-bold")
            ui.label("Modal content goes here")
            with ui.row().classes("justify-end"):
                ui.button("Close", on_click=dialog.close)

ui.button("Open Modal", on_click=show_modal)'''
            
                                    elif selected_element == "Accordion":
                                        nicegui_code = f'''with ui.expansion().classes("{all_classes}"):
    with ui.expansion_title():
        ui.label("Section 1")
    with ui.expansion_content():
        ui.label("Content 1")'''
            
                                    elif selected_element == "Table":
                                        nicegui_code = f'''ui.table(
    columns=[
        {"name": "header1", "label": "Header 1", "field": "header1"},
        {"name": "header2", "label": "Header 2", "field": "header2"}
    ],
    rows=[
        {"header1": "Data 1", "header2": "Data 2"}
    ]
).classes("{all_classes}")'''

                                    ui.html(f"""<pre class="bg-gray-100 p-2 rounded"><code>{nicegui_code}</code></pre>""")

                        
                        # Erstelle Styling-Optionen basierend auf der Element-Konfiguration
                        with ui.card().classes(f'{theme["card"]} p-4'):
                            ui.label("Styling-Optionen").classes("font-bold mb-4")
                            
                            with ui.grid().classes('grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'):
                                for option_category, values in element_config["options"].items():
                                    with ui.card().classes(f'{theme["card"]} p-4'):
                                        ui.label(option_category.replace('_', ' ').title()).classes('font-bold mb-2')
                                        current_classes[option_category] = values[0]
                                        
                                        ui.select(
                                            options=values,
                                            value=values[0],
                                            label=option_category.replace('_', ' ').title(),
                                            on_change=lambda e, cat=option_category: (
                                                current_classes.update({cat: e.value}),
                                                update_preview()
                                            )
                                        ).classes(f'{theme["select"]} w-full')
                        
                        update_preview()

                # Element-Typ Selector
                ui.select(
                    options=list(ELEMENT_TYPES.keys()),
                    value="Button",
                    label="Element-Typ",
                    on_change=update_styling_options
                ).classes(f'{theme["select"]} w-64 mb-4')

                # Container für Styling-Optionen
                options_container = ui.column().classes('w-full mt-4')
                
                # Container für Preview und Code
                preview_container = ui.column().classes('w-full')

                # Initial styling für Button anzeigen
                mock_event = type('Event', (), {'value': 'Button'})()
                update_styling_options(mock_event)

    def change_theme_full(new_theme):
        logger.debug(f"Ändere Theme auf {new_theme}")
        if theme_manager.set_theme(new_theme):
            create_content()
            ui.notify(f"Theme wurde auf {new_theme} geändert")

    # Hauptcontainer
    container = ui.column().classes('w-full p-4')
    
    # Initialer Content
    create_content()


#########################################################################

def log_installed_packages():
    logger.info("Installierte Pakete und Versionen:")
    installed_packages = {dist.metadata["Name"].lower(): dist.version for dist in metadata.distributions()}

    # Direkte Ausgabe der wichtigen Pakete
    important_packages = ['fastapi', 'nicegui']
    for package in important_packages:
        if package in installed_packages:
            logger.info(f"{package}: Version {installed_packages[package]}")

# Call log_installed_packages directly
log_installed_packages()

if __name__ == '__main__':
    logger.debug("Starte Uvicorn Server")
    uvicorn.run(app, host=HOST, port=PORT)
