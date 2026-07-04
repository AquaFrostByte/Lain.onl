import os
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

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
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/template')
def template():
    return render_template('template.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

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