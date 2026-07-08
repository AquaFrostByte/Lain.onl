import click
import requests

# Set your server configuration here
API_URL = "http://192.168.2.22:5678/api/news"  # Update this to your live domain when deployed
API_KEY = "API"  # Match this with the server environment variable

@click.command()
@click.option('--title', prompt='Article Title')
@click.option('--author', prompt='Author Name', default='Aqua')
@click.option('--email', prompt='Author Email', default='cat@grisu.app')
@click.option('--image', prompt='Image filename (Leave blank to skip)', default='')
def publish(title, author, email, image):
    """Submit news items securely to your remote Flask site."""
    
    click.echo("\nEnter the article content. Press Ctrl+D (Unix) or Ctrl+Z (Windows) then Enter when finished:")
    content_lines = []
    while True:
        try:
            line = input()
            content_lines.append(line)
        except EOFError:
            break
            
    content = "\n".join(content_lines)

    # Prepare payload data
    payload = {
        "title": title,
        "content": content,
        "author": author,
        "email": email,
        "image": image
    }

    # Attach secret token to custom header
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    click.echo("\n📡 Sending to remote server...")
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            click.echo("🚀 Success: " + response.json().get("message", "Article published!"))
        else:
            click.echo(f"❌ Server Error ({response.status_code}): {response.json().get('error')}")
            
    except requests.exceptions.RequestException as e:
        click.echo(f"❌ Failed to connect to server: {e}")

if __name__ == '__main__':
    publish()