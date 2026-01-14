from fastapi import FastAPI
from .api.ingest import router as ingest_router

app = FastAPI()

app.include_router(ingest_router)




# if __name__ == "__main__":
#     main()
