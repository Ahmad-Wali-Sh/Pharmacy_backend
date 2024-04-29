from waitress import serve
from app.wsgi import application as wsgiapp

serve(wsgiapp, host='0.0.0.0', port=8000)