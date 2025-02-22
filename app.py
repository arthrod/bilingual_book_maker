from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import subprocess
import os, re
import uuid
import threading
from datetime import datetime

app = Flask(__name__)
# 配置 CORS
CORS(app, resources={
    r"/api/*": {  # 只对 /api 路由启用 CORS
        "origins": ["http://localhost:3000", "https://pptmagic.tech"],  # 允许的域名列表
        "methods": ["GET", "POST", "OPTIONS"],  # 允许的 HTTP 方法
        "allow_headers": ["Content-Type", "Authorization"]  # 允许的请求头
    }
})

# 存储翻译任务状态
translation_tasks = {}

def clean_old_files():
    """清理超过12小时的临时文件"""
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        return
    
    current_time = datetime.now()
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        if (current_time - file_modified).days >= 0.5:
            try:
                os.remove(file_path)
            except Exception:
                pass

def translate_book_task(task_id, file_path, model, language, single_translate, user_prompt, use_context):
    """异步执行翻译任务"""
    try:
        print(user_prompt)
        cmd = [
            'python3',
            'make_book.py',
            '--book_name', file_path,
            '--ollama_model', model,
            '--api_base', 'http://192.168.1.2:11434/v1',
            '--language', language,
            # '--model', 'gpt4omini',
            # '--openai_key', os.environ.get('OPENAI_API_KEY', 'sk-CdzI6CKPu6JFB5ul4dF42543Fe304a3bAa17B5E146D93eB9'),
            # '--api_base', os.environ.get('API_BASE', 'https://oneapi.haoran.li/v1')

            ]
        if user_prompt != '':
            cmd.append('--prompt')
            cmd.append(user_prompt + '''. Translate the given text to {language}. Be faithful or accurate in translation. Make the translation readable or intelligible. Be elegant or natural in translation. If the text cannot be translated, return the original text as is. Do not translate person's name. Do not add any additional text in the translation. The text to be translated is: 
{text} ''')
        if single_translate == 'true':
            cmd.append('--single_translate')
        if use_context == 'true':
            cmd.append('--use_context')
            # cmd.append('--context_paragraph_limit 3')


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
        
        is_epub = file_path.lower().endswith('.epub')
        last_update_time = datetime.now()
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            current_time = datetime.now()
            if is_epub:
                # 对 epub 文件使用 tqdm 进度
                if '%|' in line:
                    try:
                        parts = line.strip().split('|')
                        if len(parts) >= 2:
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
                    except Exception as e:
                        print(f"Progress parsing error: {e}")
                        pass

            else:
                # 对非 epub 文件使用虚拟进度
                if (current_time - last_update_time).seconds >= 2:  # 每2秒更新一次进度
                    current_progress = translation_tasks[task_id].get('progress', 0)
                    if current_progress < 95:  # 保留最后5%给完成时使用
                        new_progress = min(current_progress + 5, 95)
                        translation_tasks[task_id].update({
                            'progress': new_progress,
                            # 'remaining_time': '00:30'  # 固定显示剩余时间
                        })
                        last_update_time = current_time
        
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
        
        params = request.form

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
            **params,  # 使用字典解包添加所有参数
            'created_at': datetime.now().isoformat()
        }
        
        # 启动异步翻译任务，使用字典解包传递参数
        thread = threading.Thread(
            target=translate_book_task,
            args=(
                task_id,
                temp_path,
                params['model'],  # 传递模型
                params['language'],  # 传递语言
                params.get('single_translate', 'false'),  # 传递是否单独翻译
                params.get('user_prompt', ''),  # 传递用户提示
                params.get('use_context', 'false')  # 传递上下文
            )
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