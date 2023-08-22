import tempfile
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import nest_asyncio

from docusage.analyzer import Mission

app = FastAPI()


@app.post("/create_report")
async def create_report(
    files: List[UploadFile] = File(...),
    mission: Optional[str] = Form(None),
    reportSize: str = Form(...),
    dynamicHeaders: Optional[bool] = Form(False),
):
    with tempfile.TemporaryDirectory() as tempdir:
        temppaths = []
        for file in files:
            contents = await file.read()
            temppath = str(Path(tempdir) / file.filename)
            temppaths.append(temppath)
            with open(temppath, "wb") as f:
                f.write(contents)
            await file.close()
        mission_reporter = Mission(
            temppaths, mission, use_dynamic_section_headers=dynamicHeaders
        )
        report_content = mission_reporter.write_report(length=reportSize)

    return JSONResponse(content={"content": report_content})


@app.on_event("startup")
async def startup():
    # Paper-QA eats up the event loop, so we need to use nest_asyncio to get around this.
    nest_asyncio.apply()


app.mount(
    "/",
    StaticFiles(directory=str(Path(__file__).parent / "static"), html=True),
    name="static",
)
