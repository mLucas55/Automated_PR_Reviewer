from fastapi import FastAPI, HTTPException, Request
import httpx
from config import GITHUB_TOKEN

app = FastAPI()

github_headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    
    # Verifies PR action is for new/updated code
    if payload.get("action") in ["opened", "synchronize"]:

        try:
            repo_name = payload["repository"]["full_name"]
            pr_number = payload["pull_request"]["number"]
            
            async with httpx.AsyncClient() as client:
                pr_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
                pr_response = await client.get(pr_url, headers=github_headers)
                pr_response.raise_for_status()
                pr_details = pr_response.json()
                
                # Fetch files changed in the PR
                files_url = f"{pr_url}/files"
                files_response = await client.get(files_url, headers=github_headers)
                files_response.raise_for_status()
                changed_files = files_response.json()

                # Add a comment to the PR
                comments_url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
                comment_data = {
                    "body": "Test from bot"
                }
                comment_response = await client.post(comments_url, json=comment_data, headers=github_headers)
                comment_response.raise_for_status()
                
                print(f"PR #{pr_number} in {repo_name}:")
                print(f"Title: {pr_details['title']}")
                print(f"Changed files: {len(changed_files)}")
                print(f"Comment added: {comment_response.status_code}")
                
                return {"message": "Webhook processed successfully, comment added"}
                
                
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Invalid payload format: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, 
                               detail=f"GitHub API error: {e.response.text}")
    
    return {"message": "Webhook received"}, 200