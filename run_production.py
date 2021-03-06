import os
from app import create_app

app = create_app(config = 'PRODUCTION')

if __name__ == '__main__':
	PORT = int(os.environ.get("PORT",5000))
	app.run(host = '0.0.0.0', port = PORT)