from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Directory where HLS files are stored
HLS_DIR = "static/hls"

# Ensure HLS directory exists
os.makedirs(HLS_DIR, exist_ok=True)

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


@app.get("/hls_test")
async def read_index():
    return FileResponse('static/hls_test.html')


@app.put("/upload/hls/{filename}")
async def upload_hls_file(filename: str, request: Request):
    try:
        file_location = os.path.join(HLS_DIR, filename)
        with open(file_location, "wb") as f:
            f.write(await request.body())
        return {"filename": filename, "location": f"/upload/hls/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hls/{filename}")
async def get_hls_file(filename: str):
    file_location = os.path.join(HLS_DIR, filename)
    if os.path.exists(file_location):
        return FileResponse(path=file_location, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.delete("/upload/hls/{filename}")
async def delete_hls_file(filename: str):
    file_location = os.path.join(HLS_DIR, filename)
    if os.path.exists(file_location):
        os.remove(file_location)
        return {"detail": f"Deleted {filename}"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
