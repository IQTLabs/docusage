import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from docusage.analyzer import Mission

app = FastAPI()


@app.post("/create_report")
async def create_report(files: List[UploadFile] = File(...)):
    with tempfile.TemporaryDirectory() as tempdir:
        temppaths = []
        for file in files:
            contents = await file.read()
            temppath = str(Path(tempdir) / file.filename)
            temppaths.append(temppath)
            with open(temppath, "wb") as f:
                f.write(contents)
            await file.close()
        report_content = Mission(temppaths).write_report()

    return JSONResponse(content={"content": report_content})


app.mount(
    "/",
    StaticFiles(directory=str(Path(__file__).parent / "static"), html=True),
    name="static",
)
