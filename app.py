import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

# The collection URL
BASE_URL = "https://archive.org/download/ios_40_42_ipa/"

@app.route('/')
def index():
    try:
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all .ipa files in the directory listing
        files = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.ipa')]
        return render_template('index.html', files=files, base_url=BASE_URL)
    except Exception as e:
        return f"Error loading collection: {e}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
