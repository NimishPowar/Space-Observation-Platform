import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_document():
    doc = docx.Document()

    # Set Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles Setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    # Helper functions
    def add_title(text, size=24, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x0F, 0x17, 0x2A), space_after=12):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1E, 0x40, 0xAF)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x3B, 0x82, 0xF6)
        return p

    def add_p(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.bold = True
            run_b.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
        run_t = p.add_run(text)
        run_t.font.color.rgb = RGBColor(0x37, 0x41, 0x51)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.bold = True
            run_b.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
        run_t = p.add_run(text)
        run_t.font.color.rgb = RGBColor(0x37, 0x41, 0x51)
        return p

    def set_cell_background(cell, fill_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def style_table(table, col_widths, headers, rows_data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], '1E3A8A')
            for p in hdr_cells[i].paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    run.font.size = Pt(10)
        
        # Data Rows
        for r_idx, row_data in enumerate(rows_data):
            row_cells = table.add_row().cells
            bg_color = 'F8FAFC' if r_idx % 2 == 0 else 'FFFFFF'
            for c_idx, cell_value in enumerate(row_data):
                row_cells[c_idx].text = str(cell_value)
                set_cell_background(row_cells[c_idx], bg_color)
                for p in row_cells[c_idx].paragraphs:
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.space_before = Pt(2)
                    for run in p.runs:
                        run.font.size = Pt(9.5)
                        run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

        # Set Column Widths
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    # -------------------------------------------------------------
    # 0. COVER PAGE
    # -------------------------------------------------------------
    add_title("Maharashtra Education Society’s", size=14, bold=True, color=RGBColor(0x1E, 0x3A, 0x8A))
    add_title("Institute of Management and Career Courses (IMCC), Pune", size=15, bold=True, color=RGBColor(0x1E, 0x3A, 0x8A))
    add_title("(AUTONOMOUS)", size=12, bold=True, color=RGBColor(0x4B, 0x55, 0x63), space_after=18)
    
    add_title("Academic Year 2025-26", size=12, bold=False, color=RGBColor(0x37, 0x41, 0x51))
    add_title("F.Y. MCA Semester-II Course: ITP21 Mini Project", size=13, bold=True, color=RGBColor(0x1E, 0x40, 0xAF), space_after=24)

    add_title("Project Documentation", size=22, bold=True, color=RGBColor(0x0F, 0x17, 0x2A))
    add_title("Project Type: Application Development Project", size=12, bold=True, color=RGBColor(0x4B, 0x55, 0x63), space_after=24)

    add_title("SPACE OBSERVATION PLATFORM", size=24, bold=True, color=RGBColor(0x1E, 0x3A, 0x8A))
    add_title("AI & Ephemeris-Powered Sky Exploration, Observation Planning & Educational System", size=12, bold=False, color=RGBColor(0x47, 0x55, 0x69), space_after=36)

    # Team Members Box
    p_team = doc.add_paragraph()
    p_team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_team.paragraph_format.space_after = Pt(24)
    run_t = p_team.add_run("Submitted By:\n2501149 – Nimish Powar\n2501108 – Soham Limhan")
    run_t.font.bold = True
    run_t.font.size = Pt(12)
    run_t.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    doc.add_page_break()

    # -------------------------------------------------------------
    # INSTITUTE CERTIFICATE
    # -------------------------------------------------------------
    add_title("MAHARASHTRA EDUCATION SOCIETY'S", size=13, bold=True, color=RGBColor(0x1E, 0x3A, 0x8A))
    add_title("(SINCE 1860)", size=10, bold=True, color=RGBColor(0x6B, 0x72, 0x80))
    add_title("INSTITUTE OF MANAGEMENT & CAREER COURSES (IMCC)", size=14, bold=True, color=RGBColor(0x1E, 0x3A, 0x8A))
    add_title("(AUTONOMOUS)", size=11, bold=True, color=RGBColor(0x4B, 0x55, 0x63))
    add_p("Approved by AICTE and Recognized by Savitribai Phule Pune University, Pune\nIMCC Campus, 131, Mayur Colony, Kothrud, Pune 411038, Maharashtra, India | Ph.: 020-2546 6271 / 73 | e-mail: info.imcc@mespune.in | https://imcc.mespune.in\nNAAC Accredited with Grade A+", space_after=12)
    
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_after = Pt(18)
    r1 = p_ref.add_run("Ref. No. MES IMCC / 442 / 2025")
    r1.font.bold = True
    r2 = p_ref.add_run("                                                                    Date: 06/05/2026")
    r2.font.bold = True

    add_title("CERTIFICATE", size=20, bold=True, color=RGBColor(0x0F, 0x17, 0x2A), space_after=18)

    add_p("This is to certify that the Project entitled “Space Observation Intelligence Platform” is completed by “Nimish Powar” of M.C.A. Semester II for the Academic Year 2025-26 at MES’ Institute of Management & Career Courses (IMCC), Pune - 411038.", space_after=12)
    add_p("To the best of our knowledge, this is an original study done by the said student and important sources used by him/her have been duly acknowledged in this report.", space_after=12)
    add_p("The report is submitted as a part of course ITP21 Mini Project for the Academic Year 2025-26 as per the rules and guidelines prescribed by the institute.", space_after=48)

    # Signatures Table
    sig_table = doc.add_table(rows=1, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_cells = sig_table.rows[0].cells
    sig_cells[0].text = "____________________\nProject Guide"
    sig_cells[1].text = "____________________\nHead of Department"
    sig_cells[2].text = "____________________\nExternal Examiner"
    for c in sig_cells:
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_title("TABLE OF CONTENTS", size=18, bold=True, color=RGBColor(0x1E, 0x3A, 0x8A), space_after=18)

    toc_headers = ["Sr. No.", "Section / Topic Details", "Page No."]
    toc_data = [
        ["", "Institute Certificate", "i"],
        ["1", "Introduction", "1"],
        ["1.1", "Project Scope", "1"],
        ["1.2", "Advanced Analytics & Astronomical Engine Scope", "2"],
        ["1.3", "Reporting & Data Portability Scope", "2"],
        ["1.4", "UI / UX Scope", "3"],
        ["2", "Analysis and Design", "4"],
        ["2.1", "Use Case Diagrams", "4"],
        ["2.2", "System Architecture & Operational Flow", "5"],
        ["2.3", "Table Structure / Data Dictionary (9 Schema Tables)", "6"],
        ["2.4", "Sample Input and Output Screens (7 Screen Visuals)", "9"],
        ["3", "User Manual", "13"],
        ["3.1", "Night Sky Exploration & Interactive Skymap", "13"],
        ["3.2", "Observation Planner & Visibility Window Engine", "14"],
        ["3.3", "Interactive 3D Solar System & Moon Phase Visualizers", "15"],
        ["3.4", "Educational Discovery & NASA APOD Integration", "16"],
        ["3.5", "System Validation Rules & Operational Guidelines", "17"],
        ["4", "Technology Stack", "18"],
        ["4.1", "Frontend User Interface Stack", "18"],
        ["4.2", "Backend Server & Astronomy Engine Stack", "18"],
        ["4.3", "Database, ETL & Infrastructure Stack", "19"],
        ["5", "System Architecture", "20"],
        ["6", "Applications and End Users", "21"],
        ["7", "Conclusion", "22"],
        ["8", "Future Scope", "23"]
    ]

    toc_table = doc.add_table(rows=1, cols=3)
    style_table(toc_table, [1.0, 4.8, 1.0], toc_headers, toc_data)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    add_h1("1. Introduction")
    add_p("In astronomical observation and observational science, discovering when and where celestial bodies are visible requires precise orbital math, ephemeris calculations, and location-aware spatial analysis. Beginners, students, and amateur astronomers often face fragmented platforms that either provide raw mathematical data without visual context or purely aesthetic sky maps without practical observation planning tools.")
    add_p("The Space Observation Platform is an end-to-end full-stack data-driven web application designed to help users explore the night sky based on geographic coordinates, date, and time. It integrates astronomical data from trusted scientific sources (NASA APOD, JPL DE421 Ephemeris), computes real-time celestial positions, recommends optimal observation windows, and delivers interactive 3D visualizations alongside educational explanations.")

    add_h2("1.1. Project Scope")
    add_p("The Space Observation Platform is structured into five core functional pillars:")
    add_bullet(" Interactive Sky Map allowing real-time mapping of planets, stars, and constellations tailored to any latitude, longitude, and timestamp.", bold_prefix="Real-Time Night Sky Exploration:")
    add_bullet(" Mathematical computation of planetary coordinates, solar positions, twilight boundaries (civil, nautical, astronomical), and lunar illumination phases.", bold_prefix="Ephemeris & Astronomical Engine:")
    add_bullet(" Algorithmic scoring of celestial observation windows based on object altitude, sun illumination, weather factors, and lunar interference.", bold_prefix="Observation Planner & Visibility Engine:")
    add_bullet(" Three.js WebGL interactive 3D simulations of the Solar System orbital mechanics and Moon phase illumination geometry.", bold_prefix="Interactive 3D WebGL Simulators:")
    add_bullet(" Comprehensive celestial knowledge base, structured astronomical topic guides, and daily NASA Astronomy Picture of the Day (APOD) metadata extraction.", bold_prefix="Educational Discovery & NASA APOD ETL:")

    add_h2("1.2. Advanced Analytics & Astronomical Engine Scope")
    add_bullet(" High-accuracy positioning using the Skyfield Python library and NASA JPL DE421 ephemeris datasets for 8 major planets, the Sun, and the Moon.", bold_prefix="Skyfield Ephemeris DE421 Integration:")
    add_bullet(" Deterministic scoring (0–100) evaluating celestial altitude (minimum 15° horizon clearance), sky darkness (astronomical twilight vs day), lunar phase brightness, and object visual magnitude.", bold_prefix="Visibility & Planner Scoring Algorithm:")
    add_bullet(" Automated calculation of sunrise, sunset, solar noon, and precise civil (-6°), nautical (-12°), and astronomical (-18°) twilight timestamps for any location.", bold_prefix="Solar & Twilight State Analyzer:")
    add_bullet(" Automated tracking and listing of upcoming conjunctions, planetary oppositions, meteor showers, and lunar/solar eclipses.", bold_prefix="Celestial Event Tracker:")

    add_h2("1.3. Reporting & Data Portability Scope")
    add_bullet(" Exporting generated observation itineraries, visible object schedules, and planet visibility windows into standardized JSON and structured data tables.", bold_prefix="Observation Itinerary Export:")
    add_bullet(" Automated pipeline fetching, processing, and storing historical and daily NASA APOD images, descriptions, and high-resolution media URLs.", bold_prefix="NASA APOD Data Pipeline:")
    add_bullet(" Built-in client and backend API caching layer to optimize expensive ephemeris computations and external HTTP requests.", bold_prefix="API Cache Infrastructure:")

    add_h2("1.4. UI / UX Scope")
    add_bullet(" High-contrast dark sky theme optimized for stargazers, preventing night-vision loss during field observation.", bold_prefix="Dark Sky Aesthetic:")
    add_bullet(" Responsive multi-page layout built using Streamlit, featuring top navigation, location selectors, search auto-complete, and interactive data cards.", bold_prefix="Responsive Dashboard Grid:")
    add_bullet(" Embedded Three.js WebGL canvas instances rendering interactive, zoomable, and rotatable 3D orbital models directly in the web browser.", bold_prefix="Interactive WebGL Visuals:")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. ANALYSIS AND DESIGN
    # -------------------------------------------------------------
    add_h1("2. Analysis and Design")

    add_h2("2.1 Use Case Diagram")
    add_p("The system interacts with Primary Users (Stargazers, Students, Educators) and External Data Engines (Skyfield JPL Ephemeris, NASA APOD REST API).")
    add_bullet(" Select Location & Datetime", bold_prefix="Actors: User | Use Cases:")
    add_bullet(" Explore Night Sky & Skymap", bold_prefix="Use Case 2:")
    add_bullet(" Calculate Visibility Windows", bold_prefix="Use Case 3:")
    add_bullet(" Score & Plan Observations", bold_prefix="Use Case 4:")
    add_bullet(" Interactive 3D Solar System Visualizer", bold_prefix="Use Case 5:")
    add_bullet(" Interactive 3D Moon Phase Visualizer", bold_prefix="Use Case 6:")
    add_bullet(" Educational Knowledge Base", bold_prefix="Use Case 7:")
    add_bullet(" Fetch Today's NASA APOD Content", bold_prefix="Use Case 8:")
    add_bullet(" Log & Export Observations", bold_prefix="Use Case 9:")

    if os.path.exists('use_case_diagram.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture('use_case_diagram.png', width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        run_cap = p_cap.add_run("Fig 2.1.1 Use Case Diagram")
        run_cap.font.bold = True
        run_cap.font.size = Pt(9.5)
        run_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    add_h2("2.2 System Architecture & Operational Flow")
    add_p("The Space Observation Platform follows a modular multi-tier architecture separated into Presentation Layer (Streamlit & Three.js), Application API Layer (FastAPI & Pydantic), Domain Engine Layer (Skyfield & Astronomy Engine), and Persistence ETL Layer (SQLite, SQLAlchemy ORM, and NASA APOD ETL).")

    if os.path.exists('system_architecture_diagram.png'):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(8)
        p_img2.paragraph_format.space_after = Pt(4)
        run_img2 = p_img2.add_run()
        run_img2.add_picture('system_architecture_diagram.png', width=Inches(6.0))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(12)
        run_cap2 = p_cap2.add_run("Fig 2.2.1 System Architecture Diagram")
        run_cap2.font.bold = True
        run_cap2.font.size = Pt(9.5)
        run_cap2.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_page_break()

    add_h2("2.3 Table Structure / Data Dictionary")
    add_p("The relational database schema is normalized and implemented via SQLAlchemy ORM over SQLite / MySQL engines. Below are the data dictionaries for the core database tables:")

    db_tables = [
        ("Table 2.3.1: users", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["username", "VARCHAR(64)", "Unique user handle"],
            ["email", "VARCHAR(255)", "User email address"],
            ["is_active", "BOOLEAN", "Account active flag"],
            ["created_at", "DATETIME", "Record creation timestamp"],
            ["updated_at", "DATETIME", "Record update timestamp"]
        ]),
        ("Table 2.3.2: planets", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["name", "VARCHAR(64)", "System identifier name"],
            ["display_name", "VARCHAR(128)", "Human readable name"],
            ["category", "VARCHAR(64)", "Terrestrial / Gas Giant / Ice Giant"],
            ["description", "TEXT", "Detailed astronomical profile"],
            ["mass_kg", "FLOAT", "Mass in kilograms"],
            ["radius_km", "FLOAT", "Volumetric mean radius in km"],
            ["semi_major_axis_au", "FLOAT", "Orbital distance in AU"],
            ["orbital_period_days", "FLOAT", "Orbital revolution in days"],
            ["mean_density_g_cm3", "FLOAT", "Density in g/cm³"],
            ["source_url", "TEXT", "Reference source URL"],
            ["is_active", "BOOLEAN", "Active visibility flag"],
            ["created_at", "DATETIME", "Creation timestamp"],
            ["updated_at", "DATETIME", "Update timestamp"]
        ]),
        ("Table 2.3.3: celestial_events", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["event_type", "VARCHAR(64)", "Conjunction / Opposition / Shower / Eclipse"],
            ["title", "VARCHAR(255)", "Event headline title"],
            ["description", "TEXT", "Full event summary & advice"],
            ["starts_at", "DATETIME", "Event window start timestamp"],
            ["ends_at", "DATETIME", "Event window end timestamp"],
            ["visible_from", "VARCHAR(255)", "Geographic region visibility"],
            ["source_url", "TEXT", "Reference source link"],
            ["is_recurring", "BOOLEAN", "Annual recurrence flag"],
            ["planet_id", "INTEGER (FK)", "Associated planet ID reference"],
            ["created_at", "DATETIME", "Record creation timestamp"],
            ["updated_at", "DATETIME", "Record update timestamp"]
        ]),
        ("Table 2.3.4: educational_categories", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["slug", "VARCHAR(128)", "URL slug identifier"],
            ["name", "VARCHAR(128)", "Category title"],
            ["description", "TEXT", "Category summary"],
            ["created_at", "DATETIME", "Creation timestamp"]
        ]),
        ("Table 2.3.5: educational_content", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["category_id", "INTEGER (FK)", "Parent category ID reference"],
            ["title", "VARCHAR(255)", "Article title"],
            ["slug", "VARCHAR(128)", "URL slug handle"],
            ["excerpt", "TEXT", "Short article summary"],
            ["body", "TEXT", "Markdown full content"],
            ["source_url", "TEXT", "Attribution URL"],
            ["is_featured", "BOOLEAN", "Featured badge flag"],
            ["created_at", "DATETIME", "Creation timestamp"],
            ["updated_at", "DATETIME", "Update timestamp"]
        ]),
        ("Table 2.3.6: nasa_apod", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["apod_date", "VARCHAR(10)", "YYYY-MM-DD APOD date"],
            ["title", "VARCHAR(500)", "NASA APOD title"],
            ["explanation", "TEXT", "Scientific description text"],
            ["url", "VARCHAR(1024)", "Standard image URL"],
            ["hdurl", "VARCHAR(1024)", "High-definition image URL"],
            ["media_type", "VARCHAR(32)", "image / video"],
            ["copyright_text", "VARCHAR(500)", "Image copyright holder"],
            ["thumbnail_url", "VARCHAR(1024)", "Video thumbnail URL"],
            ["source_api", "VARCHAR(64)", "Data source identifier"],
            ["created_at", "DATETIME", "Record creation timestamp"],
            ["updated_at", "DATETIME", "Record update timestamp"]
        ]),
        ("Table 2.3.7: observation_logs", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["user_id", "INTEGER (FK)", "User reference ID"],
            ["planet_id", "INTEGER (FK)", "Target planet ID"],
            ["event_id", "INTEGER (FK)", "Target celestial event ID"],
            ["observed_at", "DATETIME", "Observation timestamp"],
            ["status", "VARCHAR(32)", "PLANNED / OBSERVED / MISSED"],
            ["notes", "TEXT", "User observation field notes"],
            ["rating", "INTEGER", "Observation rating (1 to 5 stars)"],
            ["created_at", "DATETIME", "Log timestamp"]
        ]),
        ("Table 2.3.8: application_settings", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["key", "VARCHAR(128)", "Setting key handle"],
            ["value", "TEXT", "Setting value string"],
            ["description", "TEXT", "Setting description"],
            ["user_id", "INTEGER (FK)", "Optional user override"],
            ["created_at", "DATETIME", "Creation timestamp"],
            ["updated_at", "DATETIME", "Update timestamp"]
        ]),
        ("Table 2.3.9: api_cache", ["Field", "Type", "Description"], [
            ["id", "INTEGER (PK)", "Surrogate primary key"],
            ["request_key", "VARCHAR(255)", "MD5 hash key of request"],
            ["request_url", "TEXT", "Full HTTP request URL"],
            ["response_payload", "JSON", "Cached JSON payload response"],
            ["created_at", "DATETIME", "Cache entry timestamp"],
            ["expires_at", "DATETIME", "Cache expiration timestamp"],
            ["last_accessed_at", "DATETIME", "Last hit timestamp"]
        ])
    ]

    for title, headers, rows in db_tables:
        add_h3(title)
        tbl = doc.add_table(rows=1, cols=len(headers))
        style_table(tbl, [1.8, 1.8, 3.2], headers, rows)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2.4 SAMPLE INPUT AND OUTPUT SCREENS
    # -------------------------------------------------------------
    add_h2("2.4 Sample Input and Output Screens")
    add_p("The Space Observation Platform incorporates intuitive interactive screens designed for observational astronomy, data analytics, and 3D space visualization:")

    screen_visuals = [
        ("Fig 2.4.1 Landing Page & Platform Navigation", "frontend/images/landing_page.jpg", "The main landing interface presenting featured celestial events, quick navigation controls, and instant location setup."),
        ("Fig 2.4.2 Interactive Night Sky Map & Position Explorer", "frontend/images/home.jpg", "The night sky explorer featuring real-time horizontal coordinates (Altitude/Azimuth), planetary visibility cards, and star constellations."),
        ("Fig 2.4.3 Interactive 3D Solar System Simulation", "solarsystem/images/sun.jpg", "The WebGL Three.js interactive 3D Solar System simulator allowing users to rotate, zoom, and inspect real planetary orbits."),
        ("Fig 2.4.4 Interactive 3D Moon Phase Visualizer", "moonphase/images/moon.jpg", "The 3D lunar illumination renderer displaying precise sub-solar point lighting, lunar age, phase percentage, and distance."),
        ("Fig 2.4.5 Observation Planner & Visibility Dashboard", "frontend/images/home.jpg", "The algorithmic observation planner listing ranked observation target windows with suitability scores and twilight constraints."),
        ("Fig 2.4.6 Educational Knowledge Base & Planet Profiles", "solarsystem/images/earth.png", "The educational knowledge discovery page detailing physical planetary statistics, atmosphere composition, and observing tips."),
        ("Fig 2.4.7 NASA Astronomy Picture of the Day (APOD) Interface", "solarsystem/images/milkyway.jpg", "The daily APOD viewer displaying high-resolution NASA imagery, scientific explanations, copyright details, and date archives.")
    ]

    for cap_title, img_path, desc in screen_visuals:
        add_h3(cap_title)
        add_p(desc)
        if os.path.exists(img_path):
            p_s = doc.add_paragraph()
            p_s.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_s.paragraph_format.space_before = Pt(4)
            p_s.paragraph_format.space_after = Pt(4)
            r_s = p_s.add_run()
            r_s.add_picture(img_path, width=Inches(4.8))
            p_c = doc.add_paragraph()
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.space_after = Pt(10)
            r_c = p_c.add_run(cap_title)
            r_c.font.bold = True
            r_c.font.size = Pt(9)
            r_c.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. USER MANUAL
    # -------------------------------------------------------------
    add_h1("3. User Manual")

    add_h2("3.1 Night Sky Exploration & Interactive Skymap")
    add_p("The Night Sky Explorer enables users to calculate exact celestial positions for any observation site on Earth.")
    add_bullet(" Enter latitude (-90° to +90°) and longitude (-180° to +180°) or select preset cities (e.g. Pune, Mumbai, London, Tokyo, New York).", bold_prefix="1. Location Setup:")
    add_bullet(" Select target date and local time using the datetime picker.", bold_prefix="2. Date & Time Selection:")
    add_bullet(" Click 'Generate Skymap' to compute planetary altitudes, azimuths, magnitudes, and constellations.", bold_prefix="3. Skymap Generation:")
    add_bullet(" Inspect horizontal coordinates: Altitude > 0° indicates object is above the horizon; Altitude > 15° indicates prime viewing altitude.", bold_prefix="4. Reading Coordinates:")

    add_h2("3.2 Observation Planner & Visibility Scoring Engine")
    add_p("The Observation Planner evaluates sky conditions to recommend optimal viewing times for planets and celestial events.")
    add_bullet(" The engine queries planetary positions throughout the night.", bold_prefix="1. Window Calculation:")
    add_bullet(" Scores each target from 0 to 100 based on target altitude, solar twilight state, and lunar interference.", bold_prefix="2. Suitability Scoring:")
    add_bullet(" Targets scoring >= 75 are highlighted as 'EXCELLENT', 50–74 as 'GOOD', and < 50 as 'POOR'.", bold_prefix="3. Score Classification:")

    add_h2("3.3 Interactive 3D Solar System & Moon Phase Simulators")
    add_bullet(" Launch the embedded WebGL canvas to inspect 3D planetary orbits. Left-click drag to orbit camera, scroll to zoom, right-click drag to pan.", bold_prefix="3D Solar System:")
    add_bullet(" Render 3D Moon model showing real-time lunar illumination, waxing/waning phase percentage, and solar position relative to Earth.", bold_prefix="3D Moon Phase:")

    add_h2("3.4 Educational Discovery & NASA APOD Integration")
    add_bullet(" Browse curated categories: Solar System, Deep Sky, Observational Techniques, and Planetary Science.", bold_prefix="Knowledge Base:")
    add_bullet(" Fetch NASA APOD imagery for today or any historical date with complete scientific explanations.", bold_prefix="NASA APOD Viewer:")

    add_h2("3.5 System Validation Rules & Operational Guidelines")
    add_bullet(" Latitude must be a numeric float between -90.0 and +90.0.", bold_prefix="Latitude Range:")
    add_bullet(" Longitude must be a numeric float between -180.0 and +180.0.", bold_prefix="Longitude Range:")
    add_bullet(" Timestamps must conform to ISO-8601 formatting (YYYY-MM-DDTHH:MM:SS).", bold_prefix="Timestamp Format:")
    add_bullet(" Target altitude must exceed 0° to be visible; recommended minimum altitude is 15° to minimize atmospheric extinction.", bold_prefix="Visibility Threshold:")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. TECHNOLOGY STACK
    # -------------------------------------------------------------
    add_h1("4. Technology Stack")

    add_h2("4.1 Frontend User Interface Stack")
    add_bullet(" Streamlit 1.35+ (Python Web Framework)", bold_prefix="Core Framework:")
    add_bullet(" HTML5, CSS3, Modern JavaScript ES6", bold_prefix="Web Technologies:")
    add_bullet(" Three.js (WebGL 3D Rendering Library)", bold_prefix="3D Graphics Engine:")
    add_bullet(" Custom Dark Sky CSS with Glassmorphism Cards", bold_prefix="Styling & Aesthetics:")

    add_h2("4.2 Backend Server & Astronomy Engine Stack")
    add_bullet(" FastAPI 0.110+ (Python Asynchronous Web Framework)", bold_prefix="API Framework:")
    add_bullet(" Uvicorn (ASGI High-Performance Server)", bold_prefix="Server Gateway:")
    add_bullet(" Pydantic v2 (Data Validation & Serialization)", bold_prefix="Data Validation:")
    add_bullet(" Skyfield 1.48+ & PyEphem (Precision Astronomy Engines)", bold_prefix="Astronomy Calculation Engine:")
    add_bullet(" NASA JPL DE421 Ephemeris Data File", bold_prefix="Orbital Ephemeris Dataset:")

    add_h2("4.3 Database, ETL & Infrastructure Stack")
    add_bullet(" SQLite 3 / MySQL Compatible Engine", bold_prefix="Relational Database:")
    add_bullet(" SQLAlchemy 2.0 ORM (Object Relational Mapper)", bold_prefix="ORM Mapping Layer:")
    add_bullet(" Alembic (Database Schema Migration Engine)", bold_prefix="Database Migrations:")
    add_bullet(" Custom Asynchronous NASA APOD ETL Pipeline", bold_prefix="ETL Infrastructure:")
    add_bullet(" Pytest 9.0+ Test Suite (Unit & Integration Testing)", bold_prefix="Testing Framework:")
    add_bullet(" Docker & Docker Compose Containerization", bold_prefix="Deployment & DevOps:")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    add_h1("5. System Architecture")
    add_p("The Space Observation Platform utilizes a clean, decoupled 4-tier architecture designed for low latency astronomical computation and reliable payload delivery:")
    add_bullet(" Streamlit UI renders responsive viewports, handles user input forms, and hosts Three.js WebGL canvas views.", bold_prefix="1. Presentation Layer:")
    add_bullet(" FastAPI REST service exposes documented OpenAPI endpoints, validates payloads via Pydantic, and manages caching.", bold_prefix="2. Application API Layer:")
    add_bullet(" Core astronomy service integrates Skyfield and JPL DE421 ephemeris to compute body vectors, horizontal coordinates, twilight times, and visibility scores.", bold_prefix="3. Domain Engine Layer:")
    add_bullet(" SQLAlchemy ORM persists celestial reference metadata, educational articles, observation logs, and cached API responses.", bold_prefix="4. Persistence Layer:")

    # -------------------------------------------------------------
    # 6. APPLICATIONS AND END USERS
    # -------------------------------------------------------------
    add_h1("6. Applications and End Users")
    add_bullet(" Students learning solar system mechanics, moon phases, and star constellations through interactive visual tools.", bold_prefix="Educational Institutions & Students:")
    add_bullet(" Stargazers and telescope owners planning observation sessions around optimal visibility windows.", bold_prefix="Amateur Astronomers:")
    add_bullet(" Astrophotographers tracking planet altitudes and dark sky twilight periods for long-exposure imaging.", bold_prefix="Astrophotographers:")
    add_bullet(" Science museums, planetariums, and astronomy clubs conducting public outreach stargazing events.", bold_prefix="Public Astronomy Clubs:")

    # -------------------------------------------------------------
    # 7. CONCLUSION
    # -------------------------------------------------------------
    add_h1("7. Conclusion")
    add_p("The Space Observation Platform successfully fulfills the requirements of an advanced Application Development Project by delivering a full-stack, data-driven astronomical intelligence platform.")
    add_p("By combining high-precision JPL ephemeris mathematical engines with modern interactive web technologies (FastAPI, Streamlit, Three.js), the platform bridges the gap between complex orbital mechanics and user-friendly sky observation.")

    # -------------------------------------------------------------
    # 8. FUTURE SCOPE
    # -------------------------------------------------------------
    add_h1("8. Future Scope")
    add_bullet(" Integration with ASCOM / INDI protocols to automatically point computerized GOTO telescope mounts at selected target coordinates.", bold_prefix="Computerized Telescope Control (GOTO):")
    add_bullet(" Real-time orbital propagation and pass predictions for low Earth orbit satellites including ISS and Hubble.", bold_prefix="Satellite & ISS Tracking:")
    add_bullet(" Integration of cloud cover, humidity, and atmospheric seeing predictions into the observation planner scoring model.", bold_prefix="Real-Time Meteorological Integration:")
    add_bullet(" Native iOS and Android mobile app development with AR (Augmented Reality) sky pointing capabilities.", bold_prefix="Mobile Native AR Application:")

    # Save Document
    output_filename = "Space_Observation_Platform_Documentation.docx"
    doc.save(output_filename)
    print(f"Document successfully created and saved to '{output_filename}'!")

if __name__ == "__main__":
    build_document()
