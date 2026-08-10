import os
from flask import Flask, render_template, send_file
from report_generator import generate_report

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secure-coding-review-codealpha-task3")

VULNERABILITIES = [
    {
        "id": "V01",
        "name": "SQL Injection Risk",
        "severity": "CRITICAL",
        "description": "The login query concatenates raw user input directly into the SQL statement, allowing attackers to alter query logic and bypass authentication.",
        "impact": "Unauthenticated database access, unauthorized data retrieval, and potential full account takeover.",
        "component": "vulnerable_app.py -> login() / database query layer",
        "solution": "Use parameterized SQL queries with tuple bindings (e.g. cursor.execute(query, (username,))) and sanitize input.",
        "status": "Fixed"
    },
    {
        "id": "V02",
        "name": "Hardcoded Credentials",
        "severity": "HIGH",
        "description": "Administrative credentials and API tokens are embedded directly in source code files rather than loaded dynamically.",
        "impact": "Credential leakage through version control repos, unauthorized system access, and static key exposure.",
        "component": "vulnerable_app.py -> init_db() & auth configuration",
        "solution": "Retrieve secret keys and system passwords from environment variables using os.getenv().",
        "status": "Fixed"
    },
    {
        "id": "V03",
        "name": "Weak Password Handling",
        "severity": "HIGH",
        "description": "Passwords are compared or stored in plain text or with weak hash patterns, enabling easy decryption if compromised.",
        "impact": "User credentials exposed during database leaks, susceptible to rainbow table and brute-force attacks.",
        "component": "vulnerable_app.py -> user storage schema",
        "solution": "Hash passwords using Werkzeug's generate_password_hash() and verify using check_password_hash().",
        "status": "Fixed"
    },
    {
        "id": "V04",
        "name": "Missing Input Validation",
        "severity": "MEDIUM",
        "description": "User inputs are accepted without format checking, type validation, or length boundary constraints.",
        "impact": "Processing malformed inputs can trigger buffer issues, unexpected app logic behavior, or secondary injection risks.",
        "component": "vulnerable_app.py -> request form parser",
        "solution": "Validate input length (e.g. 3-30 chars for username), enforce required fields, and strip illegal characters.",
        "status": "Fixed"
    },
    {
        "id": "V05",
        "name": "Improper Error Handling",
        "severity": "MEDIUM",
        "description": "Internal database exception details and verbose system tracebacks are exposed directly to HTTP end users.",
        "impact": "Exposes underlying schema names, file paths, and environment internals to malicious actors.",
        "component": "vulnerable_app.py -> global error handlers",
        "solution": "Log detailed technical exceptions server-side while returning generic HTTP error responses (e.g. 400 / 401) to users.",
        "status": "Fixed"
    }
]

RECOMMENDATIONS = [
    {
        "title": "Validate and sanitize user input",
        "description": "Restrict input length and format to expected values before processing. This prevents injection and malformed payloads.",
        "icon": "fa-solid fa-filter"
    },
    {
        "title": "Use parameterized SQL queries",
        "description": "Separate SQL logic from user-supplied data to prevent injection risks and preserve query integrity.",
        "icon": "fa-solid fa-database"
    },
    {
        "title": "Never hardcode passwords or API keys",
        "description": "Store secrets in environment variables or a secure secret manager instead of source code.",
        "icon": "fa-solid fa-key"
    },
    {
        "title": "Use secure password hashing",
        "description": "Hash passwords with modern algorithms such as PBKDF2 or scrypt (via Werkzeug) rather than storing plain text.",
        "icon": "fa-solid fa-shield-halved"
    },
    {
        "title": "Implement authentication and authorization",
        "description": "Enforce session validation and role-based checks for protected routes and sensitive actions.",
        "icon": "fa-solid fa-user-lock"
    },
    {
        "title": "Use environment variables for secrets",
        "description": "Keep runtime configuration and credentials outside the codebase to reduce leakage during deployment.",
        "icon": "fa-solid fa-cloud"
    },
    {
        "title": "Implement proper error handling",
        "description": "Log technical details on the server side, while returning limited generic information to end users.",
        "icon": "fa-solid fa-bug-slash"
    },
    {
        "title": "Keep dependencies updated",
        "description": "Apply security patches and upgrade libraries regularly to reduce exposure to known vulnerabilities.",
        "icon": "fa-solid fa-arrows-rotate"
    },
    {
        "title": "Apply least privilege",
        "description": "Grant only the minimum database and file permissions required for the application to operate.",
        "icon": "fa-solid fa-user-check"
    },
    {
        "title": "Log security events safely",
        "description": "Capture important authentication and application events without exposing secret values in logs.",
        "icon": "fa-solid fa-file-lines"
    }
]

CODE_COMPARISONS = [
    {
        "title": "SQL Injection Prevention via Parameterized Query",
        "vulnerable": "# INSECURE: Raw string concatenation vulnerability\nusername = request.form.get('username')\npassword = request.form.get('password')\nquery = \"SELECT * FROM users WHERE username='\" + username + \"' AND password='\" + password + \"'\"\nresult = conn.execute(query).fetchone()",
        "secure": "# SECURE: Parameterized binding prevents SQL injection\nusername = request.form.get('username', '').strip()\npassword = request.form.get('password', '')\nquery = \"SELECT * FROM users WHERE username=?\"\nuser = conn.execute(query, (username,)).fetchone()",
        "explanation": "Parameterized queries help prevent SQL injection by strictly separating executable SQL code from user-provided input data. The database engine treats the input value as a literal string parameter rather than executable SQL command syntax."
    },
    {
        "title": "Credential & Secret Management",
        "vulnerable": "# INSECURE: Credentials hardcoded in codebase\nADMIN_USER = \"admin\"\nADMIN_PASSWORD = \"admin123\"\nSECRET_KEY = \"supersecret123\"",
        "secure": "# SECURE: Secrets loaded dynamically from Environment\nimport os\nADMIN_USER = os.getenv(\"ADMIN_USER\", \"admin\")\nADMIN_PASSWORD = os.getenv(\"ADMIN_PASSWORD\")\nSECRET_KEY = os.getenv(\"SECRET_KEY\", os.urandom(24))",
        "explanation": "Hardcoded credentials should be avoided because they can easily be exposed through source code leaks, version control commits, or build logs. Using environment variables keeps sensitive credentials separate from application code."
    },
    {
        "title": "Password Hashing & Verification",
        "vulnerable": "# INSECURE: Storing & comparing plain text passwords\nif user['password'] == input_password:\n    return 'Login successful'",
        "secure": "# SECURE: Hashing with Werkzeug PBKDF2/scrypt\nfrom werkzeug.security import generate_password_hash, check_password_hash\n\n# Registration / Seeding:\nhash_val = generate_password_hash(input_password)\n\n# Authentication:\nif user and check_password_hash(user['password_hash'], input_password):\n    return 'Login successful'",
        "explanation": "Plain text passwords expose all user accounts if a database breach occurs. One-way cryptographic hashing ensures that even database administrators cannot view raw passwords, protecting user credentials across systems."
    }
]


@app.route('/')
def dashboard():
    stats = {
        'total_vulnerabilities': 5,
        'critical': 1,
        'high': 2,
        'medium': 2,
        'low': 0,
        'score': 72,
        'improved_score': 92,
    }
    return render_template('dashboard.html', stats=stats, vulnerabilities=VULNERABILITIES)


@app.route('/security-review')
def security_review():
    return render_template(
        'security_review.html',
        app_name='Student Login Web Application',
        technology='Python + Flask + SQLite',
        score=72,
        vulnerabilities=VULNERABILITIES
    )


@app.route('/vulnerabilities')
def vulnerabilities():
    return render_template('vulnerabilities.html', vulnerabilities=VULNERABILITIES)


@app.route('/before-after')
def before_after():
    return render_template('before_after.html', comparisons=CODE_COMPARISONS)


@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html', recommendations=RECOMMENDATIONS)


@app.route('/secure-code')
def secure_code():
    return render_template('secure_code.html')


@app.route('/about')
def about_project():
    return render_template('about.html')


@app.route('/generate-report')
def generate_report_route():
    output_path = generate_report()
    return send_file(output_path, as_attachment=True, download_name='Secure_Coding_Review_Report.pdf')


if __name__ == '__main__':
    print("Starting Secure Coding Review Web Dashboard on http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
