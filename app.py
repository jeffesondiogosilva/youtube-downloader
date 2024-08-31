from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

# Diretório para salvar os vídeos (será criado no diretório temporário)
DOWNLOAD_DIR = tempfile.mkdtemp()

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = ''
    formats = []

    if request.method == 'POST':
        video_url = request.form['url']
        try:
            # Obter informações do vídeo usando yt-dlp
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                formats = info_dict.get('formats', [])
        except Exception as e:
            return f"Error: {e}"

    return render_template('index.html', video_url=video_url, formats=formats)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    format_id = request.form['format_id']
    try:
        # Opções de download
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),  # Salvar apenas no diretório temporário
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # Verifica se o arquivo existe no diretório de downloads e envia o arquivo
        filepath = os.path.join(DOWNLOAD_DIR, os.path.basename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return "Error: File not found", 404
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
