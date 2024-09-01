from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import tempfile
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Diretório temporário para salvar os vídeos
DOWNLOAD_DIR = tempfile.mkdtemp()

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = ''
    formats = []
    error_message = ''

    if request.method == 'POST':
        video_url = request.form['url']
        try:
            logging.debug(f"Received video URL: {video_url}")
            
            # Verifique se a URL é válida
            if not video_url.startswith(('http://', 'https://')):
                error_message = "Invalid URL. Please enter a valid video URL."
                logging.error(error_message)
                return render_template('index.html', video_url=video_url, formats=formats, error_message=error_message)

            # Obter informações do vídeo usando yt-dlp
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                formats = info_dict.get('formats', [])
                logging.debug(f"Available formats: {formats}")
        except Exception as e:
            error_message = f"Error occurred while fetching video formats: {e}"
            logging.error(error_message)
            return render_template('index.html', video_url=video_url, formats=formats, error_message=error_message)

    return render_template('index.html', video_url=video_url, formats=formats, error_message=error_message)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    format_id = request.form['format_id']
    try:
        logging.debug(f"Downloading video URL: {video_url} with format ID: {format_id}")

        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        filepath = os.path.join(DOWNLOAD_DIR, os.path.basename(filename))
        if os.path.exists(filepath):
            logging.info(f"File successfully downloaded: {filepath}")
            return send_file(filepath, as_attachment=True)
        else:
            error_message = "Error: File not found"
            logging.error(error_message)
            return error_message, 404
    except Exception as e:
        error_message = f"Error occurred during download: {e}"
        logging.error(error_message)
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
