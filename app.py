import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, Response, request

app = Flask(__name__)
BASE_URL = "https://archive.org/download/ios_40_42_ipa/"

@app.route('/')
def index():
    try:
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        files = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.ipa')]
        categories = {"Collection": files}
        return render_template('index.html', categories=categories, last_updated="Live from Archive.org")
    except Exception as e:
        return f"Error loading collection: {e}"

@app.route('/manifest/<filename>.plist')
def get_manifest(filename):
    ipa_url = f"{BASE_URL}{filename}.ipa"
    # This automatically detects your Render domain
    base_url = request.host_url.rstrip('/') 
    
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>{ipa_url}</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>com.retro.store</string>
                <key>bundle-version</key>
                <string>1.0</string>
                <key>kind</key>
                <string>software</string>
                <key>title</key>
                <string>{filename}</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>"""
    return Response(plist_content, mimetype='text/xml')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
