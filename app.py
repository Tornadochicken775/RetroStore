import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, Response, request

app = Flask(__name__)
BASE_URL = "https://archive.org/download/ios_40_42_ipa/"

@app.route('/')
def index():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Fetch files and categorize them as "Collection"
    files = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.ipa')]
    return render_template('index.html', categories={"Collection": files})

@app.route('/manifest/<path:filename>.plist')
def get_manifest(filename):
    # This points the install to the actual file on Archive.org
    ipa_url = f"{BASE_URL}{filename}.ipa"
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
