from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 青空文庫の『こころ』の冒頭ページのURL
            url = "https://www.aozora.gr.jp/cards/000148/files/773_14560.html"
            response = requests.get(url)
            response.raise_for_status()

            # Shift_JISでデコード
            response.encoding = 'shift_jis'
            soup = BeautifulSoup(response.text, 'html.parser')

            # 本文のある要素を特定 (div.main_text)
            main_text_element = soup.find('div', class_='main_text')
            
            # 本文の最初の段落（例として最初の300文字）を抽出
            if main_text_element:
                text_content = main_text_element.get_text(strip=True)
                # 冒頭部分を抽出して不要な改行を整形
                excerpt = text_content[:300].replace('。', '。\n').strip()
            else:
                excerpt = "本文の取得に失敗しました。"

            result = {
                "text": excerpt
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

        except requests.exceptions.RequestException as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"HTTPリクエストエラー: {e}"}, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"予期せぬエラー: {e}"}, ensure_ascii=False).encode('utf-8'))