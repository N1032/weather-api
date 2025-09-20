from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url = "https://weathernews.jp/onebox/tenki/osaka/27216/"
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # 「公式見解」のセクションを特定
            # 最新のセレクタを使って、公式見解の文章を抽出
            comment_element = soup.select_one(".oneday-comment-box__text")
            
            comment = comment_element.get_text(strip=True) if comment_element else "公式見解の取得に失敗しました。"
            
            # 不要な空白や改行を削除
            comment = re.sub(r'[\r\n\t]', '', comment)

            result = {
                "official_comment": comment
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