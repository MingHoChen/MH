from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/extract')
def extract():
    video_id = request.args.get('v')
    if not video_id:
        return jsonify({"error": "Missing video ID"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'extractor_args': {'youtube': {'player_client': ['tvhtml5', 'web']}}
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = info.get('formats', [])
            valid_formats = []
            for f in formats:
                valid_formats.append({
                    'itag': f.get('format_id'),
                    'url': f.get('url'),
                    'ext': f.get('ext'),
                    'width': f.get('width', 0),
                    'height': f.get('height', 0),
                    'vcodec': f.get('vcodec', 'none'),
                    'acodec': f.get('acodec', 'none'),
                    'headers': f.get('http_headers', {})
                })
            
            return jsonify({
                "url": info.get('url'),
                "is_live": info.get('is_live', False),
                "formats": valid_formats
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)