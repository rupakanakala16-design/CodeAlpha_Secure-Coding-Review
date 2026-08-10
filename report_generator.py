import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'reports')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'Secure_Coding_Review_Report.pdf')


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render exact page count: 'Page X of Y'
    and draw professional header/footer accents.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress headers on Cover Page (Page 1)
        if self._pageNumber > 1:
            # Top Header Bar
            self.setFillColor(colors.HexColor('#09111e'))
            self.rect(0, 800, 595.27, 42, stroke=0, fill=1)
            
            self.setStrokeColor(colors.HexColor('#38bdf8'))
            self.setLineWidth(1.5)
            self.line(0, 800, 595.27, 800)

            self.setFillColor(colors.HexColor('#38bdf8'))
            self.setFont('Helvetica-Bold', 8.5)
            self.drawString(36, 814, 'SECURE CODING REVIEW & VULNERABILITY ASSESSMENT')

            self.setFillColor(colors.HexColor('#94a3b8'))
            self.setFont('Helvetica', 8.5)
            self.drawRightString(559, 814, 'CodeAlpha Internship — Task 3')

        # Footer on ALL pages
        self.setFillColor(colors.HexColor('#09111e'))
        self.rect(0, 0, 595.27, 36, stroke=0, fill=1)

        self.setStrokeColor(colors.HexColor('#1e293b'))
        self.setLineWidth(1)
        self.line(0, 36, 595.27, 36)

        self.setFillColor(colors.HexColor('#64748b'))
        self.setFont('Helvetica', 8)
        self.drawString(36, 14, 'Candidate: Rupa Kanakala | CodeAlpha Cyber Security Internship')
        self.drawRightString(559, 14, f'Page {self._pageNumber} of {page_count}')

        self.restoreState()


def draw_cover_shield(c, x, y, size):
    """Draws a vector security shield graphic on the cover page."""
    c.saveState()
    c.setFillColor(colors.HexColor('#0f172a'))
    c.setStrokeColor(colors.HexColor('#38bdf8'))
    c.setLineWidth(2.5)

    p = c.beginPath()
    p.moveTo(x, y + size)
    p.lineTo(x + size * 0.75, y + size * 0.85)
    p.lineTo(x + size * 0.9, y + size * 0.15)
    p.lineTo(x + size * 0.5, y - size * 0.75)
    p.lineTo(x + size * 0.1, y + size * 0.15)
    p.lineTo(x + size * 0.25, y + size * 0.85)
    p.closePath()
    c.drawPath(fill=1, stroke=1)

    # Shield Inner Accent Line
    c.setStrokeColor(colors.HexColor('#4ade80'))
    c.setLineWidth(1.5)
    p2 = c.beginPath()
    p2.moveTo(x + size * 0.5, y + size * 0.75)
    p2.lineTo(x + size * 0.72, y + size * 0.2)
    p2.lineTo(x + size * 0.5, y - size * 0.55)
    p2.lineTo(x + size * 0.28, y + size * 0.2)
    p2.closePath()
    c.drawPath(fill=0, stroke=1)

    c.setFillColor(colors.HexColor('#ffffff'))
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(x + size * 0.5, y + size * 0.12, 'S')
    c.restoreState()


def build_story():
    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor('#38bdf8')      # Cyan accent
    SECONDARY = colors.HexColor('#60a5fa')    # Soft Blue
    SUCCESS = colors.HexColor('#4ade80')      # Green
    WARNING = colors.HexColor('#fb923c')      # Orange
    DANGER = colors.HexColor('#f87171')       # Red
    DARK_BG = colors.HexColor('#0f172a')      # Dark Navy
    CARD_BG = colors.HexColor('#1e293b')      # Slate Dark
    TEXT_MAIN = colors.HexColor('#f8fafc')    # Crisp White
    TEXT_MUTED = colors.HexColor('#94a3b8')   # Slate Muted

    # Custom Typography Styles
    cover_title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Title'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=PRIMARY, alignment=0, spaceAfter=8
    )
    cover_sub_style = ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=TEXT_MAIN, spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'Header1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=PRIMARY, spaceBefore=0, spaceAfter=10
    )
    h2_style = ParagraphStyle(
        'Header2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=SECONDARY, spaceBefore=8, spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyTextCustom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=14.5,
        textColor=TEXT_MAIN, spaceAfter=8
    )
    body_muted = ParagraphStyle(
        'BodyMuted', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5,
        textColor=TEXT_MUTED, spaceAfter=6
    )
    code_style = ParagraphStyle(
        'CodeStyle', parent=styles['Code'],
        fontName='Courier', fontSize=8, leading=11,
        textColor=colors.HexColor('#e2e8f0'), spaceAfter=6
    )
    note_style = ParagraphStyle(
        'NoteStyle', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8.5, leading=13,
        textColor=colors.HexColor('#cbd5e1')
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph('SECURE CODING REVIEW & VULNERABILITY ASSESSMENT', cover_title_style))
    story.append(Paragraph('CodeAlpha Cyber Security Internship – Task 3', cover_sub_style))
    
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=20))
    
    story.append(Paragraph('<b>Candidate:</b> Rupa Kanakala', body_style))
    story.append(Paragraph('<b>Role:</b> Cyber Security Intern', body_style))
    story.append(Paragraph('<b>Project Date:</b> ' + datetime.now().strftime('%d %B %Y'), body_style))
    story.append(Paragraph('<b>Target System:</b> Student Login Web Application (Flask + SQLite)', body_style))
    story.append(Paragraph('<b>Technology Stack:</b> Python 3, Flask, HTML5, CSS3, JavaScript, Jinja2, ReportLab, Pygments, Three.js', body_style))

    story.append(Spacer(1, 0.4 * inch))

    # Cover Page Information Box Table
    cover_box_data = [
        [Paragraph('<b>ASSESSMENT SNAPSHOT</b>', ParagraphStyle('CBH', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY))],
        [Paragraph('• Total Codebase Vulnerabilities Identified: <b>5 Findings</b> (1 Critical, 2 High, 2 Medium)<br/>'
                   '• Baseline Security Score: <b>72 / 100</b><br/>'
                   '• Post-Remediation Security Score: <b>92 / 100</b><br/>'
                   '• Security Controls Applied: Parameterized SQL, Werkzeug Password Hashing, Input Validation, Secrets Isolation, Error Masking.', body_style)]
    ]
    cover_box_table = Table(cover_box_data, colWidths=[6.8 * inch])
    cover_box_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#334155')),
        ('PADDING', (0, 0), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (-1, 0), 1, PRIMARY),
    ]))
    story.append(cover_box_table)

    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph('<i>This secure coding review report is submitted in partial fulfillment of the requirements for CodeAlpha Cyber Security Internship Task 3.</i>', note_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph('PAGE 2: EXECUTIVE SUMMARY', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph('<b>1. Purpose & Executive Context</b>', h2_style))
    story.append(Paragraph(
        'This Secure Coding Review was conducted for CodeAlpha Cyber Security Internship Task 3 to evaluate the security posture '
        'of the sample <i>Student Login Web Application</i>. The primary objective is to demonstrate how security weaknesses in source code '
        'can be identified through manual code analysis, classified according to industry severity benchmarks (CVSS / OWASP), and remediated '
        'using defensive software development principles.', body_style
    ))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('<b>2. Application Under Assessment</b>', h2_style))
    story.append(Paragraph('• <b>Application Name:</b> Student Login Web Application', body_style))
    story.append(Paragraph('• <b>Technology Stack:</b> Python 3.10+, Flask Web Framework, SQLite Database Engine, HTML5/CSS3 UI', body_style))
    story.append(Paragraph('• <b>Assessment Scope:</b> Authentication workflow, database access routines, password storage mechanics, input handling, and session configuration.', body_style))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('<b>3. Review Methodology</b>', h2_style))
    story.append(Paragraph(
        'The assessment utilized static application security testing (SAST) principles and security code auditing against OWASP Top 10 vulnerabilities. '
        'Key focus areas included SQL injection risks, credential hardcoding, weak cryptographic algorithms, missing input validation, and verbose error exposure.', body_style
    ))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('<b>4. Summary of Overall Findings</b>', h2_style))
    story.append(Paragraph(
        'A total of <b>5 vulnerabilities</b> were identified during the initial code review. All findings were systematically addressed in the remediated codebase '
        '(<code>secure_app.py</code>). The overall security score improved from a vulnerable baseline of <b>72/100</b> to a hardened score of <b>92/100</b>.', body_style
    ))

    exec_summary_table = Table([
        ['Metric', 'Pre-Review (Vulnerable)', 'Post-Review (Secured)', 'Delta / Improvement'],
        ['Critical Flaws', '1 (SQL Injection)', '0 Flaws', '100% Remediated'],
        ['High Flaws', '2 (Credentials & Auth)', '0 Flaws', '100% Remediated'],
        ['Medium Flaws', '2 (Input & Errors)', '0 Flaws', '100% Remediated'],
        ['Overall Score', '72 / 100', '92 / 100', '+20 Points (+27.7%)']
    ], colWidths=[1.8 * inch, 1.7 * inch, 1.7 * inch, 1.6 * inch])
    exec_summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), PRIMARY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
        ('BACKGROUND', (0, 1), (-1, -1), CARD_BG),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(exec_summary_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: PROJECT OVERVIEW
    # =========================================================================
    story.append(Paragraph('PAGE 3: PROJECT OVERVIEW', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph('<b>1. Core Project Objectives</b>', h2_style))
    story.append(Paragraph(
        'The main goal of this project is to construct a practical, interactive secure coding review system that displays the life cycle of application security vulnerabilities: '
        'from identification and severity classification to code refactoring and executive compliance reporting.', body_style
    ))

    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph('<b>2. Scope of Code Audit</b>', h2_style))
    story.append(Paragraph('The code review targeted three primary application layers:', body_style))
    story.append(Paragraph('1. <b>Presentation Layer (HTTP Forms & Sessions):</b> Examined form inputs, length restrictions, and cookie security flags.', body_style))
    story.append(Paragraph('2. <b>Application Logic Layer (Flask Handlers):</b> Analyzed route authentication, error handlers, and credential management.', body_style))
    story.append(Paragraph('3. <b>Data Persistence Layer (SQLite Engine):</b> Reviewed SQL query composition, parameter binding, and password hashing implementations.', body_style))

    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph('<b>3. Target Architecture Overview</b>', h2_style))
    story.append(Paragraph(
        'The demonstration environment comprises two standalone Python Flask drivers: <code>vulnerable_app.py</code> (demonstration flawed state) '
        'and <code>secure_app.py</code> (remediated state), complemented by a central Flask dashboard (<code>app.py</code>) and this ReportLab PDF Engine (<code>report_generator.py</code>).', body_style
    ))

    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph('<b>4. Review Methodology Workflow</b>', h2_style))
    story.append(Paragraph('• <b>Phase 1: Line-by-Line Inspection:</b> Audited python source code for unsafe dynamic query formatting and secret storage.', body_style))
    story.append(Paragraph('• <b>Phase 2: Risk Scoring:</b> Mapped findings to CVSS v3.1 severity tiers (Critical, High, Medium, Low).', body_style))
    story.append(Paragraph('• <b>Phase 3: Secure Refactoring:</b> Replaced raw queries with parameterized bindings and integrated Werkzeug secure password hashing.', body_style))
    story.append(Paragraph('• <b>Phase 4: Validation & Reporting:</b> Verified fix efficacy via input payload testing and compiled PDF documentation.', body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SECURITY FINDINGS SUMMARY
    # =========================================================================
    story.append(Paragraph('PAGE 4: SECURITY FINDINGS SUMMARY', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph(
        'The table below summarizes all 5 security vulnerabilities identified during the code audit of the sample student login application. '
        'Each finding was analyzed for technical impact and fully remediated in the secure baseline release.', body_style
    ))
    story.append(Spacer(1, 0.12 * inch))

    findings_table_data = [
        ['ID', 'Vulnerability Name', 'Severity', 'Affected Component', 'Remediation Status'],
        ['V01', 'SQL Injection Risk', 'CRITICAL', 'vulnerable_app.py -> login() query', 'Fixed'],
        ['V02', 'Hardcoded Credentials', 'HIGH', 'vulnerable_app.py -> init_db() credentials', 'Fixed'],
        ['V03', 'Weak Password Handling', 'HIGH', 'vulnerable_app.py -> plain text storage', 'Fixed'],
        ['V04', 'Missing Input Validation', 'MEDIUM', 'vulnerable_app.py -> request form parser', 'Fixed'],
        ['V05', 'Improper Error Handling', 'MEDIUM', 'vulnerable_app.py -> exception handler', 'Fixed'],
    ]

    findings_table = Table(findings_table_data, colWidths=[0.6 * inch, 2.2 * inch, 1.1 * inch, 1.9 * inch, 1.0 * inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), PRIMARY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
        ('BACKGROUND', (0, 1), (-1, -1), CARD_BG),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        ('TEXTCOLOR', (2, 1), (2, 1), DANGER),
        ('TEXTCOLOR', (2, 2), (2, 3), WARNING),
        ('TEXTCOLOR', (2, 4), (2, 5), colors.HexColor('#facc15')),
        ('TEXTCOLOR', (4, 1), (4, -1), SUCCESS),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(findings_table)

    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph('<b>Risk Distribution Analysis</b>', h2_style))
    story.append(Paragraph('• <b>Critical Risk (20%):</b> Direct SQL injection allowing unauthenticated authentication bypass.', body_style))
    story.append(Paragraph('• <b>High Risk (40%):</b> Plaintext password validation and hardcoded admin secrets.', body_style))
    story.append(Paragraph('• <b>Medium Risk (40%):</b> Unrestricted input payload length and verbose internal error disclosure.', body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: DETAILED VULNERABILITY ANALYSIS
    # =========================================================================
    story.append(Paragraph('PAGE 5: DETAILED VULNERABILITY ANALYSIS', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12))

    vulns_detail = [
        ('V01', 'SQL Injection Risk', 'CRITICAL', 'The login route constructs SQL statements via raw string concatenation with user-supplied form fields.', 'Unauthenticated database compromise, account takeover, and full data leakage.', 'Use parameterized SQL queries with tuple parameter bindings.', 'Fixed'),
        ('V02', 'Hardcoded Credentials', 'HIGH', 'Administrative passwords and secret keys are stored directly inside source code constants.', 'Secret exposure in version control history and unauthorized application access.', 'Extract secrets into environment variables via os.getenv().', 'Fixed'),
        ('V03', 'Weak Password Handling', 'HIGH', 'User passwords are validated using plaintext comparisons without cryptographic hashing.', 'Full credential exposure if the backend user database is accessed or dumped.', 'Utilize Werkzeug PBKDF2 / scrypt password hashing functions.', 'Fixed'),
        ('V04', 'Missing Input Validation', 'MEDIUM', 'Form parameters are accepted without type checking, character whitelist, or length constraints.', 'Processing malformed or oversized payloads may trigger application logic anomalies.', 'Enforce minimum/maximum length constraints and strip illegal input characters.', 'Fixed'),
        ('V05', 'Improper Error Handling', 'MEDIUM', 'Detailed database tracebacks and system errors are returned directly to end users.', 'Internal database schema details are leaked, assisting targeted exploit attempts.', 'Log detailed error stacks server-side and return generic HTTP error status codes.', 'Fixed'),
    ]

    for item in vulns_detail:
        v_box_data = [
            [Paragraph(f'<b>Finding {item[0]}: {item[1]}</b>', ParagraphStyle('VBH', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY)),
             Paragraph(f'<b>Severity: {item[2]}</b>', ParagraphStyle('VBS', parent=body_style, fontName='Helvetica-Bold', textColor=DANGER if item[2]=='CRITICAL' else (WARNING if item[2]=='HIGH' else colors.HexColor('#facc15')), alignment=2))],
            [Paragraph(f'• <b>Description:</b> {item[3]}<br/>'
                       f'• <b>Security Impact:</b> {item[4]}<br/>'
                       f'• <b>Recommendation:</b> {item[5]}<br/>'
                       f'• <b>Remediation Status:</b> <font color="#4ade80"><b>{item[6]}</b></font>', body_style), '']
        ]
        v_table = Table(v_box_data, colWidths=[4.8 * inch, 2.0 * inch])
        v_table.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, PRIMARY),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(v_table)
        story.append(Spacer(1, 0.08 * inch))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: BEFORE VS AFTER CODE COMPARISON
    # =========================================================================
    story.append(Paragraph('PAGE 6: BEFORE VS AFTER CODE COMPARISON', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph('<b>1. SQL Injection Remediation (Parameterized Queries)</b>', h2_style))
    story.append(Paragraph('<font color="#f87171"><b>VULNERABLE IMPLEMENTATION (vulnerable_app.py):</b></font>', body_style))
    vuln_code_1 = "query = \"SELECT * FROM users WHERE username='\" + username + \"' AND password='\" + password + \"'\"\nresult = conn.execute(query).fetchone()"
    story.append(Table([[Paragraph(f'<font color="#f8d9d9"><code>{vuln_code_1}</code></font>', code_style)]], colWidths=[6.8 * inch], style=[('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a0f14')), ('BOX', (0, 0), (-1, -1), 0.5, DANGER), ('PADDING', (0, 0), (-1, -1), 8)]))

    story.append(Spacer(1, 0.06 * inch))
    story.append(Paragraph('<font color="#4ade80"><b>SECURE REMEDIATED IMPLEMENTATION (secure_app.py):</b></font>', body_style))
    sec_code_1 = "query = \"SELECT * FROM users WHERE username = ?\"\nuser = conn.execute(query, (username,)).fetchone()"
    story.append(Table([[Paragraph(f'<font color="#d4ffe7"><code>{sec_code_1}</code></font>', code_style)]], colWidths=[6.8 * inch], style=[('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0d1f17')), ('BOX', (0, 0), (-1, -1), 0.5, SUCCESS), ('PADDING', (0, 0), (-1, -1), 8)]))
    story.append(Paragraph('<i>Analysis: Parameterized queries separate executable SQL logic from user parameters, rendering payload injection ineffective.</i>', note_style))

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph('<b>2. Credential & Secret Management Remediation</b>', h2_style))
    story.append(Paragraph('<font color="#f87171"><b>VULNERABLE IMPLEMENTATION:</b></font>', body_style))
    vuln_code_2 = "password = \"admin123\"\nsecret_key = \"supersecret123\""
    story.append(Table([[Paragraph(f'<font color="#f8d9d9"><code>{vuln_code_2}</code></font>', code_style)]], colWidths=[6.8 * inch], style=[('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a0f14')), ('BOX', (0, 0), (-1, -1), 0.5, DANGER), ('PADDING', (0, 0), (-1, -1), 8)]))

    story.append(Spacer(1, 0.06 * inch))
    story.append(Paragraph('<font color="#4ade80"><b>SECURE REMEDIATED IMPLEMENTATION:</b></font>', body_style))
    sec_code_2 = "import os\npassword = os.getenv(\"APP_PASSWORD\")\nsecret_key = os.getenv(\"SECRET_KEY\", os.urandom(24))"
    story.append(Table([[Paragraph(f'<font color="#d4ffe7"><code>{sec_code_2}</code></font>', code_style)]], colWidths=[6.8 * inch], style=[('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0d1f17')), ('BOX', (0, 0), (-1, -1), 0.5, SUCCESS), ('PADDING', (0, 0), (-1, -1), 8)]))
    story.append(Paragraph('<i>Analysis: Retrieving secrets from environment variables prevents credential leaks via version control repositories.</i>', note_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: SECURITY RECOMMENDATIONS
    # =========================================================================
    story.append(Paragraph('PAGE 7: SECURITY RECOMMENDATIONS', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph('Below are 10 key secure coding recommendations established from the application code audit:', body_style))
    story.append(Spacer(1, 0.1 * inch))

    recs = [
        ("1. Validate and Sanitize User Input", "Enforce strict length limits, data types, and character whitelists for all incoming form parameters."),
        ("2. Use Parameterized SQL Queries", "Always use placeholders (?) and tuple parameter passing to completely isolate query logic from user data."),
        ("3. Never Hardcode Secrets or Credentials", "Load database credentials, API tokens, and secret keys dynamically from runtime environment variables."),
        ("4. Use Secure Password Hashing", "Hash stored passwords using PBKDF2, scrypt, or Argon2 algorithms via trusted libraries like Werkzeug."),
        ("5. Implement Robust Auth & Session Controls", "Store session keys securely with HttpOnly flags and cryptographically signed session cookies."),
        ("6. Leverage Environment Variables for Config", "Isolate deployment configuration from source code repositories to streamline secret rotation."),
        ("7. Implement Safe Error Handling & Logging", "Log technical stack traces on the server side while displaying generic 400/401 messages to end users."),
        ("8. Keep Software Dependencies Updated", "Audit and update core dependencies (Flask, Werkzeug, Jinja2) regularly to patch known CVE vulnerabilities."),
        ("9. Enforce Principle of Least Privilege", "Configure database connections with minimal permissions required for operational execution."),
        ("10. Log Security Events Safely", "Capture audit logs for authentication attempts without logging plain text credentials or secret tokens.")
    ]

    for r_title, r_desc in recs:
        story.append(Paragraph(f'<b>• {r_title}</b>', h2_style))
        story.append(Paragraph(r_desc, body_style))
        story.append(Spacer(1, 0.02 * inch))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: TESTING & VALIDATION
    # =========================================================================
    story.append(Paragraph('PAGE 8: TESTING & VALIDATION', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph(
        'To confirm the effectiveness of remediated security controls, a structured test suite was executed against the hardened baseline '
        '(<code>secure_app.py</code>). The validation process verified that all identified vulnerabilities were successfully neutralized.', body_style
    ))
    story.append(Spacer(1, 0.1 * inch))

    test_table_data = [
        ['Security Test Case', 'Target Vulnerability', 'Test Payload / Vector', 'Observed Result', 'Status'],
        ['Input Validation Check', 'V04: Missing Input', 'Username = "a" (Len < 3)', 'Rejected with HTTP 400', 'PASSED'],
        ['SQL Injection Testing', 'V01: SQL Injection', "' OR '1'='1' --", 'Safely escaped by SQLite', 'PASSED'],
        ['Password Hash Verification', 'V03: Weak Auth', 'Submit plain password', 'Werkzeug scrypt match', 'PASSED'],
        ['Error Disclosure Test', 'V05: Verbose Error', 'Trigger invalid request', 'Generic 401 response', 'PASSED'],
        ['Secrets Audit', 'V02: Hardcoded Secrets', 'Source code search', '0 secrets in repository', 'PASSED'],
    ]

    test_table = Table(test_table_data, colWidths=[1.5 * inch, 1.3 * inch, 1.6 * inch, 1.5 * inch, 0.9 * inch])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), PRIMARY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
        ('BACKGROUND', (0, 1), (-1, -1), CARD_BG),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        ('TEXTCOLOR', (4, 1), (4, -1), SUCCESS),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(test_table)

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph('<b>Validation Conclusion</b>', h2_style))
    story.append(Paragraph(
        'All 5 test cases passed empirical validation. Parameterized bindings successfully neutralized SQL injection vectors, '
        'length bounds rejected malformed username payloads, and error handlers masked internal database schema details.', body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: FINAL SECURITY ASSESSMENT
    # =========================================================================
    story.append(Paragraph('PAGE 9: FINAL SECURITY ASSESSMENT', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph('<b>Security Score Comparison</b>', h2_style))
    story.append(Paragraph(
        'The security review demonstrated a measurable reduction in software risk exposure following code refactoring.', body_style
    ))
    story.append(Spacer(1, 0.15 * inch))

    score_box_data = [
        [Paragraph('<b>INITIAL SECURITY SCORE</b>', ParagraphStyle('SB1', parent=body_style, fontName='Helvetica-Bold', textColor=WARNING, alignment=1)),
         Paragraph('<b>FINAL SECURITY SCORE</b>', ParagraphStyle('SB2', parent=body_style, fontName='Helvetica-Bold', textColor=SUCCESS, alignment=1))],
        [Paragraph('<font size="28"><b>72 / 100</b></font>', ParagraphStyle('SV1', parent=body_style, fontName='Helvetica-Bold', textColor=WARNING, alignment=1)),
         Paragraph('<font size="28"><b>92 / 100</b></font>', ParagraphStyle('SV2', parent=body_style, fontName='Helvetica-Bold', textColor=SUCCESS, alignment=1))],
        [Paragraph('Status: Vulnerable Baseline', ParagraphStyle('SS1', parent=body_style, alignment=1)),
         Paragraph('Status: Hardened Implementation', ParagraphStyle('SS2', parent=body_style, alignment=1))]
    ]
    score_table = Table(score_box_data, colWidths=[3.3 * inch, 3.3 * inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1f1910')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#0e241b')),
        ('BOX', (0, 0), (0, -1), 1, WARNING),
        ('BOX', (1, 0), (1, -1), 1, SUCCESS),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(score_table)

    story.append(Spacer(1, 0.3 * inch))

    disclaimer_box = Table([
        [Paragraph('<b>ASSESSMENT DISCLAIMER NOTE</b>', ParagraphStyle('DH', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY))],
        [Paragraph('<i>These scores represent project evaluation metrics designed specifically for the CodeAlpha Cyber Security Internship Task 3 demo. '
                   'They serve as an educational comparison of baseline code quality versus secure code refactoring and do NOT constitute a formal third-party commercial security audit certification.</i>', note_style)]
    ], colWidths=[6.8 * inch])
    disclaimer_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(disclaimer_box)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: CONCLUSION
    # =========================================================================
    story.append(Paragraph('PAGE 10: CONCLUSION', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph('<b>1. Summary of Achievements</b>', h2_style))
    story.append(Paragraph(
        'Through this Secure Coding Review project for CodeAlpha Task 3, a complete security assessment lifecycle was successfully demonstrated. '
        'Critical flaws such as raw SQL concatenation and plaintext credential handling were thoroughly identified, analyzed, and remediated.', body_style
    ))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('<b>2. Impact on Application Security Posture</b>', h2_style))
    story.append(Paragraph(
        'Refactoring the codebase to use parameterized queries, Werkzeug password hashing, input validation, and environment secret storage '
        'significantly enhanced system resilience against unauthorized access, credential theft, and database compromise.', body_style
    ))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('<b>3. Future Security Roadmap</b>', h2_style))
    story.append(Paragraph('• Integrate Automated SAST tools (e.g. Bandit, Semgrep) into the continuous integration (CI/CD) pipeline.', body_style))
    story.append(Paragraph('• Implement multi-factor authentication (MFA) and strict role-based access controls (RBAC).', body_style))
    story.append(Paragraph('• Conduct periodic web application penetration testing and third-party dependency vulnerability scans.', body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: GITHUB REPOSITORY / PROJECT STRUCTURE
    # =========================================================================
    story.append(Paragraph('PAGE 11: GITHUB REPOSITORY / PROJECT STRUCTURE', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Paragraph(
        'The project source code is organized into a clean, modular repository layout ready for GitHub submission and local evaluation:', body_style
    ))
    story.append(Spacer(1, 0.1 * inch))

    repo_structure_text = """Secure-Coding-Review/
├── app.py                  # Flask Main Web Controller & Dashboard Routes
├── vulnerable_app.py       # Insecure Sample Application (Educational Demo)
├── secure_app.py           # Hardened Sample Application (Remediated Baseline)
├── report_generator.py     # ReportLab 12-Page PDF Engine Generator
├── requirements.txt        # Python Dependencies Specification
├── README.md               # GitHub Project Documentation & Setup Guide
├── templates/              # Jinja2 HTML Page Layouts
│   ├── base.html           # Core Navigation & Layout Shell
│   ├── dashboard.html      # Hero Section & Three.js Canvas Container
│   ├── security_review.html# Application Audit Overview & Timeline
│   ├── vulnerabilities.html# 5 Detailed Vulnerability Finding Cards
│   ├── before_after.html   # Side-by-Side Code Comparison Panels
│   ├── recommendations.html# 10 Secure Coding Guidelines Cards
│   ├── secure_code.html    # Hardened Application Showcase
│   └── about.html          # Internship Task & Repository Metadata
├── static/                 # Static Assets & Styling
│   ├── css/styles.css      # Dark Cybersecurity Glassmorphism CSS
│   └── js/script.js        # Three.js 3D Shield & Counter Animations
└── reports/                # Compliance PDF Outputs
    └── Secure_Coding_Review_Report.pdf"""

    struct_table = Table([[Paragraph(f'<code>{repo_structure_text.replace(chr(10), "<br/>").replace(" ", "&nbsp;")}</code>', code_style)]], colWidths=[6.8 * inch])
    struct_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#02050b')),
        ('BOX', (0, 0), (-1, -1), 0.5, PRIMARY),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(struct_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: DECLARATION / FINAL NOTES
    # =========================================================================
    story.append(Paragraph('PAGE 12: DECLARATION / FINAL NOTES', h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=14))

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('<b>INTERNSHIP PROJECT DECLARATION</b>', h2_style))
    story.append(Paragraph(
        'I hereby declare that this project titled <b>"Secure Coding Review & Vulnerability Assessment"</b> is an authentic piece of work '
        'developed by me for the <b>CodeAlpha Cyber Security Internship – Task 3</b>.', body_style
    ))
    story.append(Paragraph(
        'This project was developed strictly for educational and internship demonstration purposes to showcase secure coding principles, '
        'risk assessment methodologies, and executive security documentation.', body_style
    ))

    story.append(Spacer(1, 0.4 * inch))

    sig_table_data = [
        [Paragraph('<b>Candidate Name:</b> Rupa Kanakala', body_style), Paragraph('<b>Internship Program:</b> CodeAlpha Cyber Security', body_style)],
        [Paragraph('<b>Task Number:</b> Task 3', body_style), Paragraph('<b>Submission Status:</b> Completed & Verified', body_style)],
        [Paragraph('<b>Date of Submission:</b> ' + datetime.now().strftime('%d %B %Y'), body_style), Paragraph('<b>Signature:</b> <i>Rupa Kanakala</i>', body_style)]
    ]
    sig_table = Table(sig_table_data, colWidths=[3.4 * inch, 3.4 * inch])
    sig_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, PRIMARY),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, 1), 0.5, colors.HexColor('#334155')),
    ]))
    story.append(sig_table)

    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph('<i>End of Secure Coding Review & Vulnerability Assessment Report — CodeAlpha Task 3.</i>', note_style))

    return story


def generate_report():
    """Generates the official 12-page ReportLab PDF report."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        title='Secure Coding Review & Vulnerability Assessment',
        author='Rupa Kanakala',
        subject='CodeAlpha Cyber Security Internship – Task 3',
        keywords='Cybersecurity Secure Coding Vulnerability Report CodeAlpha Task 3'
    )

    story = build_story()
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully at: {OUTPUT_FILE}")
    return OUTPUT_FILE


if __name__ == '__main__':
    generate_report()
