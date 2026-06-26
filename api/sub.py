
from http.server import BaseHTTPRequestHandler
import urllib.request
import ssl
import base64

# ⚠️ ВСТАВЬТЕ СЮДА ВАШ НАСТОЯЩИЙ PROVIDER ID С САЙТА HAPP-PROXY.COM, ЕСЛИ ОН ЕСТЬ
REAL_PROVIDER_ID = "sGiUuYKS"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        github_url = "https://raw.githubusercontent.com/IlinAlexVikt/xxx/refs/heads/main/1.txt"
        
        try:
            # ИСПРАВЛЕНИЕ: Имитируем реальный браузер (User-Agent) и отключаем строгую проверку SSL на Vercel
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            ssl_context = ssl._create_unverified_context()
            
            req = urllib.request.Request(github_url, headers=headers)
            with urllib.request.urlopen(req, context=ssl_context) as response:
                encoded_content = response.read().decode('utf-8').strip()
                
            # Декодируем Base64-текст подписки
            try:
                decoded_bytes = base64.b64decode(encoded_content)
                decoded_text = decoded_bytes.decode('utf-8')
            except Exception:
                decoded_text = encoded_content

            # Формируем новые ЖЕСТКИЕ текстовые заголовки подписки по спецификации Happ
            forced_text_headers = (
                "#profile-title: SoSi 1 VPN ⚡\n"
                "#profile-update-interval: 1\n"
                "#hide-settings: 1\n"                       # Зажигает тумблер "Скрыть настройки"
                f"#provider-id: {REAL_PROVIDER_ID}\n"       # Зажигает тумблер "Зашифрованная подписка"
                "#subscription-userinfo: upload=1073741824000; download=1073741824000; total=10737418240000; expire=1782864000\n"
                "#support-url: https://\n"
                "#profile-web-page-url: https://\n"
                '#announce: "Привет халявщики и тунеядцы"\n'
            )

            # Очищаем старые текстовые комментарии из оригинального файла
            clean_lines = []
            for line in decoded_text.splitlines():
                if line.strip() and not line.startswith('#'):
                    clean_lines.append(line)
            
            full_plain_text = forced_text_headers + "\n".join(clean_lines) + "\n"
            
            # Заново кодируем весь текст в единый Base64 для Happ
            final_base64_content = base64.b64encode(full_plain_text.encode('utf-8'))
                
            # Отправляем HTTP-ответ и дублируем параметры в сетевые заголовки сервера Vercel
            self.send_response(200)
            self.send_header('hide-settings', '1')
            self.send_header('provider-id', REAL_PROVIDER_ID)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            
            # Отдаем приложению итоговый защищенный Base64-код
            self.wfile.write(final_base64_content)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Error fetching data: {str(e)}".encode('utf-8'))
