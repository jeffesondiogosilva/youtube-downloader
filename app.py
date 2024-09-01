from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import tempfile
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Diretório para salvar os vídeos
DOWNLOAD_DIR = tempfile.mkdtemp()

# Certifique-se de que o caminho para o arquivo de cookies está correto
COOKIE_FILE = './cookies.txt'

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = ''
    formats = []

    if request.method == 'POST':
        video_url = request.form['url']
        try:
            logging.debug(f"Received video URL: {video_url}")
            ydl_opts = {
                'quiet': True,
                'cookiefile': COOKIE_FILE,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer': 'https://www.youtube.com/',
                },
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                formats = info_dict.get('formats', [])
                logging.debug(f"Available formats: {formats}")
        except Exception as e:
            logging.error(f"Error occurred while fetching video formats: {e}")
            return render_template('index.html', video_url=video_url, formats=formats, error_message=f"Error: {e}")

    return render_template('index.html', video_url=video_url, formats=formats)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    format_id = request.form['format_id']
    try:
        logging.debug(f"Downloading video URL: {video_url} with format ID: {format_id}")
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'cookiefile': COOKIE_FILE,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.youtube.com/',
            },
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        filepath = os.path.join(DOWNLOAD_DIR, os.path.basename(filename))
        if os.path.exists(filepath):
            logging.info(f"File successfully downloaded: {filepath}")
            return send_file(filepath, as_attachment=True)
        else:
            logging.error("File not found after download")
            return "Error: File not found", 404
    except Exception as e:
        logging.error(f"Error occurred during download: {e}")
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
