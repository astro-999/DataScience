from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
async def get_items():
    return [
        {"name": "Item 1"},
        {   
            "name": "Item 2",}  
    ]
