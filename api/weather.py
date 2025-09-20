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

            # 最新のセレクタを使って天気と気温を抽出
            # 天気情報の要素を検索
            weather_element = soup.select_one(".oneday-weather-telop")
            # 気温情報の要素を検索
            temperature_element = soup.select_one(".oneday-weather-temp")
            
            weather = weather_element.get_text(strip=True) if weather_element else "情報なし"
            temperature = temperature_element.get_text(strip=True) if temperature_element else "情報なし"
            
            # 不要な文字を削除
            weather = re.sub(r'[\r\n\t]', '', weather)
            temperature = re.sub(r'[\r\n\t]', '', temperature)

            result = {
                "weather": weather,
                "temperature": temperature
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

        except requests.exceptions.RequestException as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"HTTPリクエストエラー: {e}"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"予期せぬエラー: {e}"}).encode('utf-8'))