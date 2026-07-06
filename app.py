import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#SQL Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Fetch the secret key from environment variables
API_KEY = os.getenv("NEWS_API_KEY")
TEMPLATE_PATH = os.path.join(os.getcwd(), 'templates', 'index.html')

def require_api_key(f):
    """Decorator to protect endpoints with an API key."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        # Read the 'X-API-Key' header from the request
        provided_key = request.headers.get("X-API-Key")
        if not API_KEY or provided_key != API_KEY:
            return jsonify({"error": "Unauthorized. Invalid or missing API key."}), 401
        return f(*args, **kwargs)
    return decorated

class GuestbookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        
        if name and message:
            new_entry = GuestbookEntry(name=name, message=message)
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('index'))
            
    # .limit(3) ensures we only grab the last 3 entries for the homepage
    recent_entries = GuestbookEntry.query.order_by(GuestbookEntry.date_posted.desc()).limit(3).all()
    return render_template('index.html', entries=recent_entries)

@app.route('/template')
def template():
    return render_template('template.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/entries')
def all_entries():
    all_entries = GuestbookEntry.query.order_by(GuestbookEntry.date_posted.desc()).all()
    return render_template('all_entries.html', entries=all_entries)

#API Endpoints 

@app.route('/api/news', methods=['POST'])
@require_api_key
def add_news_via_api():
    data = request.get_json() or {}
    
    title = data.get("title")
    content = data.get("content")
    image = data.get("image", "").strip()
    author = data.get("author", "Aqua")
    email = data.get("email", "cat@grisu.app")

    if not title or not content:
        return jsonify({"error": "Title and content are required fields."}), 400

    # Format line breaks to HTML
    content_html = content.replace("\n", "<br>")

    # 1. Read and Parse HTML Template
    if not os.path.exists(TEMPLATE_PATH):
        return jsonify({"error": "Template file not found on server"}), 500

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 2. Find target marker
    target = soup.find('a', attrs={'name': 'NewsItemID'})
    if not target:
        return jsonify({"error": "Template marker <a name='NewsItemID'> missing."}), 500

    # 3. Build image HTML fragment if image given
    image_html = ""
    if image:
        image_html = f'''
        <a href="/static/img/News/{image}" target="_blank">
            <img class="NewsImg" src="{{{{ url_for('static', filename='img/News/{image}') }}}}">
        </a><br>
        '''

    # 4. Construct structural news element
    new_article_raw = f'''
    <table class="news-container">
        <tr>
            <td>
                <div class="newshead">{title}</div>
                <div class="news">
                    {content_html}<br><br>
                    {image_html}
                    <br>[<a href="mailto:{email}">{author}</a>]
                </div>
            </td>
        </tr>
    </table>
    <p></p>
    '''
    
    # 5. Inject element and save file
    new_article_soup = BeautifulSoup(new_article_raw, 'html.parser')
    target.insert_after(new_article_soup)

    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return jsonify({"message": "Successfully published article remotely!"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5678)