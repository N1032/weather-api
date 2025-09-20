from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. Yahoo!天気から天気概要をスクレイピング
            yahoo_url = "https://weather.yahoo.co.jp/weather/27/6210/27382.html"
            yahoo_response = requests.get(yahoo_url)
            yahoo_response.raise_for_status()
            yahoo_soup = BeautifulSoup(yahoo_response.content, 'html.parser')
            
            summary_element = yahoo_soup.select_one(".yjw_table_area .yjw_td_comment")
            summary = summary_element.get_text(strip=True) if summary_element else "概要の取得に失敗しました。"
            summary = re.sub(r'[\r\n\t]', '', summary)

            # 2. OpenWeatherMapから気温情報をAPIで取得
            # あなたのOpenWeatherMap APIキーをここに貼り付けてください
            owm_api_key = "e7be61aefcb6fae216e924aa79a0cec3"
            lat = 34.4554
            lon = 135.6322
            owm_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={owm_api_key}&units=metric&lang=ja"
            owm_response = requests.get(owm_url)
            owm_response.raise_for_status()
            owm_data = owm_response.json()
            
            temp_max = owm_data['main']['temp_max']
            temp_min = owm_data['main']['temp_min']

            result = {
                "weather_summary": summary,
                "temp_max": temp_max,
                "temp_min": temp_min
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