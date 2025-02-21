from flask import Flask, request, jsonify, render_template, send_file
import subprocess
import os, re
import uuid
import threading
from datetime import datetime

app = Flask(__name__)

# 存储翻译任务状态
translation_tasks = {}

# 支持的翻译模型
SUPPORTED_MODELS = {
    'qwen2.5': 'Qwen 2.5',
    'gpt4omini': 'GPT 4o mini',
    'deepseek-r1:14b': 'DeepSeek R1 14B',
    'gemini-2.0-flash': 'Gemini 2.0 Flash'
}

# 支持的目标语言
SUPPORTED_LANGUAGES = {
    'zh-hans': '简体中文',
    'zh-hant': '繁体中文',
    'en': 'English',
    'ja': '日本語',
    'ko': '한국어',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch'
}

def clean_old_files():
    """清理超过24小时的临时文件"""
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        return
    
    current_time = datetime.now()
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        if (current_time - file_modified).days >= 1:
            try:
                os.remove(file_path)
            except Exception:
                pass

def translate_book_task(task_id, file_path, model, language, api_key=None):
    """异步执行翻译任务"""
    try:
        cmd = [
            'python3',
            'make_book.py',
            '--book_name', file_path,
            '--ollama_model', 'qwen2.5',
            '--api_base', 'http://192.168.1.2:11434/v1',
            '--language', language,
            # '--model', model,
            # '--openai_key', os.environ.get('OPENAI_API_KEY', 'sk-CdzI6CKPu6JFB5ul4dF42543Fe304a3bAa17B5E146D93eB9'),
            # '--api_base', os.environ.get('API_BASE', 'https://oneapi.haoran.li/v1')
        ]

        print(cmd)
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env={**os.environ, 'PYTHONUNBUFFERED': '1'}
        )
        
        total_pages = 0
        current_page = 0
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
                
            # print(line.strip())
            
            # 尝试从进度条输出中提取进度信息
            if '%|' in line:
                try:
                    # 从tqdm输出中提取进度信息
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        # 提取百分比
                        percent = int(float(parts[0].strip('%'))) 
                        s = parts[2]
                        match = re.search(r'<(\d{2}:\d{2})', s)
                        remaining_time = None
                        if match:
                            remaining_time = match.group(1)
                        translation_tasks[task_id].update({
                            'progress': percent,
                            'remaining_time': remaining_time,
                        })
                        print("CURRENT STATE:",percent, parts)
                except Exception as e:
                    print(f"Progress parsing error: {e}")
                    pass
        
        process.wait()
        
        if process.returncode == 0:
            output_file = f"{os.path.splitext(file_path)[0]}_bilingual{os.path.splitext(file_path)[1]}"
            translation_tasks[task_id].update({
                'status': 'completed',
                'output_file': output_file,
                'progress': 100
            })
        else:
            error = process.stderr.read()
            translation_tasks[task_id].update({
                'status': 'failed',
                'error': error,
                'progress': 0
            })
    except Exception as e:
        translation_tasks[task_id].update({
            'status': 'failed',
            'error': str(e),
            'progress': 0
        })
        translation_tasks[task_id].update({
            'status': 'failed',
            'error': str(e),
            'progress': 0
        })

@app.route('/')
def index():
    return render_template('index.html',
                          models=SUPPORTED_MODELS,
                          languages=SUPPORTED_LANGUAGES)

@app.route('/api/translate', methods=['POST'])
def translate_book():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有找到文件'}), 400
            
        file = request.files['file']
        if not file.filename:
            return jsonify({'error': '没有选择文件'}), 400
            
        model = request.form.get('model', 'google')
        if model not in SUPPORTED_MODELS:
            return jsonify({'error': '不支持的翻译模型'}), 400
            
        language = request.form.get('language', 'zh-hans')
        if language not in SUPPORTED_LANGUAGES:
            return jsonify({'error': '不支持的目标语言'}), 400
            
        api_key = request.form.get('api_key')
        
        # 生成任务ID和临时文件路径
        task_id = str(uuid.uuid4())
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        file_ext = os.path.splitext(file.filename)[1]
        temp_path = os.path.join(temp_dir, f"{task_id}{file_ext}")
        file.save(temp_path)
        
        # 创建翻译任务
        translation_tasks[task_id] = {
            'status': 'processing',
            'filename': file.filename,
            'model': model,
            'language': language,
            'created_at': datetime.now().isoformat()
        }
        
        # 启动异步翻译任务
        thread = threading.Thread(
            target=translate_book_task,
            args=(task_id, temp_path, model, language, api_key)
        )
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'status': 'processing'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<task_id>')
def get_status(task_id):
    task = translation_tasks.get(task_id)

    if not task:
        return jsonify({'error': '任务不存在'}), 404
    return jsonify(task)

@app.route('/api/download/<task_id>')
def download_file(task_id):
    task = translation_tasks.get(task_id)
    if not task or task['status'] != 'completed':
        return jsonify({'error': '文件不可用'}), 404
        
    return send_file(
        task['output_file'],
        as_attachment=True,
        download_name=f"bilingual_{task['filename']}"
    )

@app.before_request
def before_request():
    clean_old_files()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)