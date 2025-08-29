import urllib.request
import os
import requests
import base64

print("Obtaining presigned URL")

iam_token = os.environ['IAM_TOKEN']

print(f"[debug] Token length: {len(iam_token)}")
# print(f"token: {base64.b64encode(iam_token[:5].encode())}")

headers = {'Authorization': f"Bearer {iam_token}"}

# url = f"{os.environ['FUNC_URL'}?run_id=${os.environ['RUN_ID']}&repo_id=${os.environ['REPO_ID']}"
presigned = requests.post(
    os.environ['UPLOAD_FUNC_URL'],
    headers=headers,
    params={'run_id': os.environ['RUN_ID'], 'repo_id': os.environ['REPO_ID']},
)
presigned.raise_for_status()
presigned = presigned.json()


print("Uploading archive")
upload_resp = requests.post(
    presigned['url'],
    data=presigned['fields'],
    files={'file': ('file', open(os.environ['ARCHIVE_PATH'], 'rb'))},
    timeout=300,
)
if upload_resp.status_code != 204:
    print(upload_resp.text)
    upload_resp.raise_for_status()

print("Starting build")
response = requests.post(
    os.environ['START_FUNC_URL'],
    headers=headers,
    params={'run_id': os.environ['RUN_ID'], 'repo_id': os.environ['REPO_ID']},
)
response.raise_for_status()
response = response.json()

print(f"Build successfully started, id={response['build_id']}, execution_id={response['execution_id']}")

with open("./build-id", 'w') as f:
    f.write(response['build_id'])
