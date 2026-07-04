import os
import time
from flask import Flask, Response, send_from_directory, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    categories = {}
    root_dir = 'ipas'
    all_files = []

    if os.path.exists(root_dir):
        for folder in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder)
            if os.path.isdir(folder_path):
                files = [f for f in os.listdir(folder_path) if f.endswith('.ipa')]
                if files:
                    categories[folder] = files
                    all_files.extend([os.path.join(folder, f) for f in files])
    
    if all_files:
        last_mod = max([os.path.getmtime(os.path.join(root_dir, f)) for f in all_files])
        last_updated = time.strftime('%Y-%m-%d %H:%M', time.localtime(last_mod))
    else:
        last_updated = "No apps found"
        
    return render_template('index.html', categories=categories, last_updated=last_updated)

@app.route('/manifest/<category>/<filename>.plist')
def get_manifest(category, filename):
    # Dynamically get the base URL from the request (works for both local and Render)
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
                    <string>{base_url}/ipas/{category}/{filename}.ipa</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>com.retro.testapp</string>
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

@app.route('/ipas/<category>/<path:filename>')
def serve_ipa(category, filename):
    return send_from_directory(os.path.join('ipas', category), filename)

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, defaulting to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)