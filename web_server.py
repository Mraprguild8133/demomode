from flask import Flask, render_template, request, redirect
import os
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player')
def player():
    encoded_url = request.args.get('url', '')
    encoded_name = request.args.get('name', 'Media File')
    file_type = request.args.get('type', 'video')
    
    if not encoded_url:
        return redirect('/')
    
    url = urllib.parse.unquote(encoded_url)
    file_name = urllib.parse.unquote(encoded_name)
    
    return render_template('player.html', url=url, file_name=file_name, file_type=file_type)

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
