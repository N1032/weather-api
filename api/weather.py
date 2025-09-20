from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url = "https://weather.yahoo.co.jp/weather/27/6210/27382.html"
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # 「今日の天気」の概要を特定
            # 最新のセレクタを使ってテキストを抽出
            comment_element = soup.select_one(".yjw_table_area .yjw_td_comment")
            
            comment = comment_element.get_text(strip=True) if comment_element else "天気概要の取得に失敗しました。"
            
            # 不要な空白や改行を削除
            comment = re.sub(r'[\r\n\t]', '', comment)

            result = {
                "weather_summary": comment
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