from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # これを追加して、CORSを有効化

@app.route('/api/get-url', methods=['POST'])
def get_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    url = data['url']

    ydl_opts = {'quiet': True, 'dump_single_json': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            if formats:
                first_url = formats[0].get('url', 'No URL found')
                return jsonify({'url': first_url})
            else:
                return jsonify({'error': 'No formats found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
