```
cd qr_server
python3 -m venv env
source env/bin/activate
pip install python-multipart
pip install -r requirements.txt
pip install "uvicorn[standard]"
uvicorn app.main:app  --host 0.0.0.0 --ssl-keyfile=./key.key --ssl-certfile=./cert.key --port 8005

```
