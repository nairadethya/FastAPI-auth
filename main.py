import fastapi 

app = fastapi.FastAPI()

@app.post('/login')
def login():
    """
        
    """
    return "ThisTokenFake"