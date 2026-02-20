import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Словари для шифрования и расшифровки
encrypt_dict = {
    'й': '~', 'ц': '|', 'у': '•', 'к': '√', 'е': 'π', 'н': '÷', 'г': '×',
    'ш': '¶', 'щ': '¶', 'з': '∆', 'х': '£', 'ф': '€', 'ы': '$', 'в': '¢',
    'а': '^', 'п': '°', 'р': '=', 'о': '{', 'л': '}', 'д': '\\', 'ж': '%',
    'э': '©', 'я': '®', 'ч': '™', 'с': '℅', 'м': '[', 'и': ']', 'т': '@',
    'ь': '#', 'б': '₽', 'ю': '_'
}

decrypt_dict = {v: k for k, v in encrypt_dict.items()}

# HTML шаблон
HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Шифратор / Дешифратор</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
            font-size: 1.1em;
        }
        
        textarea {
            width: 100%;
            height: 150px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            resize: vertical;
            transition: border-color 0.3s;
            font-family: 'Courier New', monospace;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 25px 0;
            flex-wrap: wrap;
        }
        
        button {
            padding: 12px 30px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        #encryptBtn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        #decryptBtn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        #clearBtn {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .result {
            margin-top: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .result h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        #resultText {
            min-height: 80px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            font-family: 'Courier New', monospace;
            word-wrap: break-word;
        }
        
        .alphabet-section {
            margin-top: 30px;
            padding: 20px;
            background: #f1f3f5;
            border-radius: 10px;
        }
        
        .alphabet-section h3 {
            color: #333;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .alphabet-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 10px;
        }
        
        .alphabet-item {
            background: white;
            padding: 8px;
            border-radius: 6px;
            text-align: center;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #dee2e6;
        }
        
        .alphabet-item .letter {
            font-weight: bold;
            color: #667eea;
            margin-right: 5px;
        }
        
        .alphabet-item .symbol {
            font-family: 'Courier New', monospace;
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 4px;
        }
        
        .error {
            color: #dc3545;
            text-align: center;
            margin-top: 10px;
            font-weight: 500;
        }
        
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }
        
        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }
            
            h1 {
                font-size: 2em;
            }
            
            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Шифратор / Дешифратор</h1>
        
        <div class="input-group">
            <label for="inputText">Введите текст:</label>
            <textarea id="inputText" placeholder="Например: привет мир"></textarea>
        </div>
        
        <div class="buttons">
            <button id="encryptBtn">🔒 Зашифровать</button>
            <button id="decryptBtn">🔓 Расшифровать</button>
            <button id="clearBtn">🗑️ Очистить</button>
        </div>
        
        <div class="result">
            <h3>Результат:</h3>
            <div id="resultText"></div>
        </div>
        
        <div class="alphabet-section">
            <h3>📋 Алфавит шифрования</h3>
            <div class="alphabet-grid" id="alphabetGrid"></div>
        </div>
        
        <div class="footer">
            ⚡ Сервис шифрования на основе пользовательского алфавита
        </div>
    </div>

    <script>
        const encryptDict = {{ encrypt_dict | tojson }};
        const decryptDict = {{ decrypt_dict | tojson }};
        
        // Отображение алфавита
        function displayAlphabet() {
            const grid = document.getElementById('alphabetGrid');
            grid.innerHTML = '';
            
            // Сортируем буквы по алфавиту
            const sortedLetters = Object.keys(encryptDict).sort();
            
            for (const letter of sortedLetters) {
                const symbol = encryptDict[letter];
                const item = document.createElement('div');
                item.className = 'alphabet-item';
                item.innerHTML = `<span class="letter">${letter}</span> → <span class="symbol">${symbol}</span>`;
                grid.appendChild(item);
            }
        }
        
        // Шифрование
        document.getElementById('encryptBtn').addEventListener('click', async () => {
            const text = document.getElementById('inputText').value;
            if (!text) {
                alert('Введите текст для шифрования');
                return;
            }
            
            try {
                const response = await fetch('/encrypt', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                const data = await response.json();
                document.getElementById('resultText').textContent = data.result;
            } catch (error) {
                document.getElementById('resultText').textContent = 'Ошибка при шифровании';
            }
        });
        
        // Расшифрование
        document.getElementById('decryptBtn').addEventListener('click', async () => {
            const text = document.getElementById('inputText').value;
            if (!text) {
                alert('Введите текст для расшифровки');
                return;
            }
            
            try {
                const response = await fetch('/decrypt', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                const data = await response.json();
                document.getElementById('resultText').textContent = data.result;
            } catch (error) {
                document.getElementById('resultText').textContent = 'Ошибка при расшифровке';
            }
        });
        
        // Очистка
        document.getElementById('clearBtn').addEventListener('click', () => {
            document.getElementById('inputText').value = '';
            document.getElementById('resultText').textContent = '';
        });
        
        // Вставка примера при загрузке
        window.addEventListener('load', () => {
            displayAlphabet();
            document.getElementById('inputText').value = 'привет мир';
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML, encrypt_dict=encrypt_dict, decrypt_dict=decrypt_dict)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    text = request.json.get('text', '').lower()
    result = []
    for char in text:
        if char in encrypt_dict:
            result.append(encrypt_dict[char])
        else:
            result.append(char)
    return jsonify({'result': ''.join(result)})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    text = request.json.get('text', '')
    result = []
    for char in text:
        if char in decrypt_dict:
            result.append(decrypt_dict[char])
        else:
            result.append(char)
    return jsonify({'result': ''.join(result)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
