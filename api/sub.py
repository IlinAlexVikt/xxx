from http.server import BaseHTTPRequestHandler
import urllib.request
import base64

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Прямая ссылка на ваш Base64 файл на GitHub
        github_url = "https://raw.githubusercontent.com/IlinAlexVikt/xxx/refs/heads/main/1.txt"
        
        try:
            # 1. Скачиваем оригинальный файл с GitHub
            req = urllib.request.Request(github_url)
            with urllib.request.urlopen(req) as response:
                encoded_content = response.read().decode('utf-8').strip()
                
            # 2. Декодируем оригинальный Base64-текст подписки обратно в строки
            try:
                decoded_bytes = base64.b64decode(encoded_content)
                decoded_text = decoded_bytes.decode('utf-8')
            except Exception:
                # Если файл на GitHub вдруг лежал в открытом виде (не Base64)
                decoded_text = encoded_content

            # 3. Формируем новые ЖЕСТКИЕ текстовые заголовки подписки для Happ
            # Убираем дефисы из служебных параметров, так как некоторые версии Happ их не любят
            forced_text_headers = (
                "#profile-title: SoSi 1 VPN ⚡\n"
                "#profile-update-interval: 1\n"
                "#hide-settings: 1\n"
                "#providerid: sosi1_private_vpn\n"
                "#subscription-userinfo: upload=1073741824000; download=1073741824000; total=10737418240000; expire=1782864000\n"
                "#support-url: https://\n"
                "#profile-web-page-url: https://\n"
                '#announce: "Привет халявщики и тунеядцы"\n'
            )

            # 4. Очищаем старые текстовые комментарии из оригинального файла (если они там были)
            clean_lines = []
            for line in decoded_text.splitlines():
                if line.strip() and not line.startswith('#'):
                    clean_lines.append(line)
            
            # Соединяем новые заголовки и оригинальные VLESS-ссылки
            full_plain_text = forced_text_headers + "\n".join(clean_lines) + "\n"
            
            # 5. Заново кодируем весь текст в единый Base64, чтобы Happ принял его как один файл
            final_base64_content = base64.b64encode(full_plain_text.encode('utf-8'))
                
            # 6. Отправляем HTTP-ответ (дублируем защиту и в сетевые заголовки сервера)
            self.send_response(200)
            self.send_header('hide-settings', '1')
            self.send_header('providerid', 'sosi1_private_vpn')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            
            # Отдаем приложению итоговый защищенный Base64-код
            self.wfile.write(final_base64_content)
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
