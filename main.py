from fastapi import FastAPI, HTTPException, Request
import httpx
from config import GITHUB_TOKEN
import ollama

app = FastAPI()

github_headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_model_feedback(diff_content, commit_messages):
    
    combined_string = "\n".join(commit_messages)
    
    prompt = "This is data from a Github pull request. It contains a diff file and a list of commit messages. Please review the code quality and generate a concise but effective comment. Keep in mind this comment will be posted to the pull request on Github: \n"
    payload = prompt + "\n" + combined_string + "\n" + diff_content

    response = ollama.chat(
        model="qwen2.5-coder:1.5b",
        messages=[{"role": "user", 
                   "content": payload}],
        stream=False
    )

    return response

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    
    # Verifies PR action is for new/updated code
    if payload.get("action") in ["opened", "synchronize"]:

        try:
            repo_name = payload["repository"]["full_name"]
            pr_number = payload["pull_request"]["number"]
            
            commits_url = payload["pull_request"]["commits_url"]

            async with httpx.AsyncClient() as client:
                commits_response = await client.get(commits_url, headers=github_headers)
                commits_response.raise_for_status() # Raises an error *if* the request fails
                commits_data = commits_response.json()

                # Builds list of all commit messages
                commit_messages = [commit["commit"]["message"] for commit in commits_data]

                diff_url = payload["pull_request"]["diff_url"] # Standard unified diff format
                #patch_url = payload["pull_request"]["patch_url"] # Email-style patch format

                # Fetch the acual code
                diff_response = await client.get(diff_url, headers=github_headers, follow_redirects=True)
                diff_response.raise_for_status()
                diff_content = diff_response.text #TODO should be a raw multi line diff file

                automated_comment = get_model_feedback(diff_content, commit_messages)






                ############# CHANGES STOP HERE ##############







                # Add a comment to the PR
                comments_url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
                comment_data = {
                    "body": automated_comment
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