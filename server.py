from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.parse

class ContactsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        if path == '/' or path == '':
            page = 'contacts.html'
        elif path == '/catalog':
            page = 'catalog.html'
        elif path == '/category':
            page = 'category.html'
        elif path == '/home':
            page = 'home.html'
        elif path == '/contacts':
            page = 'contacts.html'
        else:
            page  = 'contacts.html'

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        try:
            page_path = Path("templates") / page
            with open(page_path, 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            contacts_path = Path('templates') / 'contacts.html'
            with open(contacts_path, 'rb') as file:
                self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        content_type = self.headers.get('Content-Type', '')

        print(f" Content-Type: {content_type}")
        print(f" Content-Length: {content_length} байт")
        print(f" Path: {self.path}")

        if content_length > 0:
            post_data = self.rfile.read(content_length)

            print(f"\nТело запроса:")
            print(f"  {post_data}")

            # Парсим данные в зависимости от типа
            print(f"\nРаспарсенные данные:")

            if 'application/x-www-form-urlencoded' in content_type:
                # Данные формы
                parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                for key, value in parsed_data.items():
                    print(f" {key}: {value[0] if len(value) == 1 else value}")

            elif 'application/json' in content_type:
                # JSON данные
                try:
                    import json
                    parsed_data = json.loads(post_data.decode('utf-8'))
                    for key, value in parsed_data.items():
                        print(f" {key}: {value}")
                except Exception as e:
                    print(f"Ошибка парсинга JSON: {e}")
                    print(f"Сырой JSON: {post_data.decode('utf-8')}")

            else:
                # Неизвестный формат - выводим как текст
                try:
                    print(f" {post_data.decode('utf-8')}")
                except:
                    print(f"Бинарные данные, размер: {len(post_data)} байт")
        else:
            print("(тело запроса пустое)")

        print("=" * 50)

        # Отправляем ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()





def run_server(port=8000):
    """Запускает сервер"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ContactsHandler)

    print(f"Сервер запущен на http://localhost:{port}")
    print("Доступные страницы:")
    print("/home - Главная")
    print("/catalog - Каталог")
    print("/category - Категории")
    print("/contacts   - Контакты")


    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")


if __name__ == '__main__':
    run_server()