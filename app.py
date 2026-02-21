from fastapi import FastAPI
from task_zero import task_zero_router
from task_one import task_one_router


app = FastAPI(debug=True)


app.include_router(task_zero_router)
app.include_router(task_one_router)


@app.get("/health", tags=["Health"], description="Health Check")
def health():
    return {"status": "ok"}