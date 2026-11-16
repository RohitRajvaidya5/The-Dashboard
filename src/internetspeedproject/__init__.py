import uvicorn
from internetspeedproject.app import app


def main() -> None:
    uvicorn.run("internetspeedproject.app:app", host="127.0.0.1", port=8000, reload=True)


__all__ = ["app", "main"]
