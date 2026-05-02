from flask import Flask, render_template,request,redirect

app = Flask(__name__)
projects = [
    {"title":"portfolio website","description":"my personal portfolio","category":"Web"},
    {"title":"calculator app","description":"python calculator","category":"App"},
    {"title":"todo app","description":"task manager","category":"Web"}

]

@app.route("/")
def home1():
    return render_template("home1.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/projects')
def projects():
    all_projects = [
        {'title': 'Portfolio WEBSITE', 'category': 'Web', 'description': 'MY PERSONAL PORTFOLIo'},
        {'title': 'CALCULATOR app', 'category': 'App', 'description': 'python calculator'},
        {"title": "todo app", "description": "task manager", "category": "Web"}
    ]
    all_categories = list(set(p['category'] for p in all_projects))
    cat_filter = request.args.get('cat')
    if cat_filter:
        display_projects = [p for p in all_projects if p['category'] == cat_filter]
    else:
        display_projects = all_projects
    return render_template('project.html',
                           projects=display_projects,
                           categories=all_categories)

@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        with open("data.txt","a") as file:
           file.write(f"{name}: {message}\n")
        return "message sent!"
    return render_template("contact.html")
@app.route("/data")
def data_view():
        with open("data.txt","r") as file:
            data = file.readlines()

        return render_template("data.html",data=data)

@app.route("/collaborate")
def collaborate():
    messages = []
    try:
        with open("data.txt","r") as file:
            for line in file.readlines():
                if ":" in line:
                    name, message = line.split(":", 1)
                    messages.append({
                        "name": name.strip(),
                        "message": message.strip()
                    })
    except FileNotFoundError:
        messages = []
    
    return render_template("collaborate.html", messages=messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=5000, debug=True)