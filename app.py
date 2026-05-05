from flask import Flask, render_template, request, redirect

# Initialise the Flask application
app = Flask(__name__)

# ── Static project data (used by the /projects route) ──────────────────────
# Each dict represents one portfolio project with a title, description,
# and category used for the filter buttons on the projects page.
projects = [
    {"title": "portfolio website", "description": "my personal portfolio", "category": "Web"},
    {"title": "calculator app",    "description": "python calculator",     "category": "App"},
    {"title": "todo app",          "description": "task manager",          "category": "Web"},
]


# ── Home page ───────────────────────────────────────────────────────────────
@app.route("/")
def home1():
    """Render the landing / welcome page."""
    return render_template("home1.html")


# ── About page ──────────────────────────────────────────────────────────────
@app.route("/about")
def about():
    """Render the About Me page with skills and education info."""
    return render_template("about.html")


# ── Projects page ───────────────────────────────────────────────────────────
@app.route('/projects')
def projects():
    """
    Render the Projects page.
    Supports optional ?cat= query parameter to filter by category.
    """
    all_projects = [
        {'title': 'Portfolio WEBSITE', 'category': 'Web', 'description': 'MY PERSONAL PORTFOLIo'},
        {'title': 'CALCULATOR app',    'category': 'App', 'description': 'python calculator'},
        {"title": "todo app",          "description": "task manager", "category": "Web"},
    ]

    # Build a unique list of categories for the filter buttons
    all_categories = list(set(p['category'] for p in all_projects))

    # Read the optional category filter from the URL query string
    cat_filter = request.args.get('cat')

    if cat_filter:
        # Show only projects that match the selected category
        display_projects = [p for p in all_projects if p['category'] == cat_filter]
    else:
        # No filter applied — show all projects
        display_projects = all_projects

    return render_template('project.html',
                           projects=display_projects,
                           categories=all_categories)


# ── Contact page ─────────────────────────────────────────────────────────────
@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    GET:  Render the contact form.
    POST: Save the submitted name and message to data.txt, then confirm.
    """
    if request.method == "POST":
        name    = request.form["name"]
        message = request.form["message"]

        # Append the new message to the persistent data file
        with open("data.txt", "a") as file:
            file.write(f"{name}: {message}\n")

        return "message sent!"

    return render_template("contact.html")


# ── Admin data view ──────────────────────────────────────────────────────────
@app.route("/data")
def data_view():
    """Read all lines from data.txt and display them on the admin page."""
    with open("data.txt", "r") as file:
        data = file.readlines()

    return render_template("data.html", data=data)


# ── Collaborate page ─────────────────────────────────────────────────────────
@app.route("/collaborate")
def collaborate():
    """
    Read messages from data.txt, parse them into name/message dicts,
    and render the collaborate page.
    """
    messages = []
    try:
        with open("data.txt", "r") as file:
            for line in file.readlines():
                if ":" in line:
                    # Each line is formatted as "Name: message text"
                    name, message = line.split(":", 1)
                    messages.append({
                        "name":    name.strip(),
                        "message": message.strip(),
                    })
    except FileNotFoundError:
        # data.txt does not exist yet — start with an empty list
        messages = []

    return render_template("collaborate.html", messages=messages)


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Run on all interfaces so the app is accessible outside the container
    app.run(host="0.0.0.0", port=5000, debug=True)
