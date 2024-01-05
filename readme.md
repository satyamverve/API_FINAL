# Commands:
1. Make sure to create virtual environment and install requirements.txt file provided

2. Run the Application
uvicorn main:app --reload

# To run with IP in Local
> add this lines to "main.py"

app = FastAPI()
if _name_ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

know_your_IP:
windows: ipconfig
ubuntu: ifconfig

<run(IP): uvicorn main:app --host 0.0.0.0 --port 8000 --reload>

## access the fastapi app from others system:
<search: http://<your-local-ip>:8000>
origins=["*"] 


# Endpoints requests
All endpoints can be used by visiting the swagger documentation at localhost:9999/v1/documentation

# Command to clear all __pycache__ files
find . -type d -name "__pycache__" -exec rm -r {} \;

