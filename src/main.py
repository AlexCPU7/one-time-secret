import uvicorn

from config import PORT_EXTERNAL

if __name__ == "__main__":
    uvicorn.run("application:app", host="0.0.0.0", port=PORT_EXTERNAL, reload=True)
