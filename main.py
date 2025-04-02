from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    # verifies PR action is for new/updated code
    if payload.get("action") in ["opened", "synchronize"]:
        # Extract PR details and modified files here
        print(payload)  
    return {"message": "Webhook received"}, 200