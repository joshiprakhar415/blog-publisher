from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret123'

users = {
    "admin": {"password": "12345", "role": "admin"}
}

# In-memory articles
articles = [
    {"id": 1, "title": "First Blog", "content": "This is first article", "date": "2026-03-23"}
]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User exists"
        users[username] = {"password": password, "role": "guest"}
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = users.get(username)
    if user and user['password'] == password:
        session['user'] = username
        session['role'] = user['role']
        return redirect(url_for('admin_dashboard') if user['role']=='admin' else url_for('guest_home'))
    return "Invalid credentials"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/guest_home')
def guest_home():
    return render_template('guest_home.html', articles=articles)

@app.route('/article/<int:id>')
def view_article(id):
    article = next((a for a in articles if a['id']==id), None)
    return render_template('article.html', article=article)



@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html', articles=articles)

@app.route('/add', methods=['GET','POST'])
def add_article():
    if request.method == 'POST':
        new = {
            "id": len(articles)+1,
            "title": request.form['title'],
            "content": request.form['content'],
            "date": request.form['date']
        }
        articles.append(new)
        return redirect(url_for('admin_dashboard'))
    return render_template('add_article.html')

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_article(id):
    article = next((a for a in articles if a['id']==id), None)

    if article is None:
        return "Article not found", 404

    if request.method == 'POST':
        article['title'] = request.form['title']
        article['content'] = request.form['content']
        article['date'] = request.form['date']
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_article.html', article=article)

@app.route('/delete/<int:id>')
def delete_article(id):
    global articles
    articles = [a for a in articles if a['id']!=id]
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)