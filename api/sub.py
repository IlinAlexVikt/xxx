from http.server import BaseHTTPRequestHandler
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Ссылка на ваш оригинальный Base64 файл на GitHub
        github_url = "https://githubusercontent.com"
        
        try:
            # Скачиваем файл с GitHub
            req = urllib.request.Request(github_url)
            with urllib.request.urlopen(req) as response:
                file_content = response.read()
                
            # 2. Формируем успешный HTTP-ответ (200 OK)
            self.send_response(200)
            
            # ПРИНУДИТЕЛЬНО ДОБАВЛЯЕМ HTTP-ЗАГОЛОВКИ БЕЗОПАСНОСТИ ДЛЯ HAPP
            self.send_header('hide-settings', '1')
            self.send_header('providerid', 'sosi1_private_vpn')
            
            # Разрешаем доступ и задаем тип контента
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            
            # Отдаем тело файла
            self.wfile.write(file_content)
            
        except Exception as e:
            # Если что-то пошло не так, отдаем ошибку 500
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error fetching subscription: {str(e)}".encode('utf-8'))
