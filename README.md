# auto_pr_chat

## Run As API

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Set env vars

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY
```

3. Start FastAPI server

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

## API

- `GET /health`
- `POST /v1/agent/run`

Request example:

```json
{
  "task_informations": {
    "creator_name": "测试博主"
  },
  "task": [
    {
      "maximum_price": "1000",
      "collab_type": "单推",
      "delivery_type": "送拍",
      "video_type": "",
      "schedule": "",
      "product": ""
    },
    {
      "maximum_price": "",
      "collab_type": "",
      "delivery_type": "",
      "video_type": "",
      "schedule": "",
      "product": ""
    }
  ],
  "settings": {
    "openai_previous_id": null,
    "node_change": false,
    "node_current": "greet_run",
    "creator_latest_response": "你已经加上了博主"
  },
  "recursion_limit": 1000
}
```

## Run With Docker

1. Prepare env file

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY
```

2. Build image

```bash
docker build -t auto-pr-chat:latest .
```

3. Run container

```bash
docker run -d --name auto-pr-chat \
  --env-file .env \
  -p 8000:8000 \
  auto-pr-chat:latest
```

4. Verify

```bash
curl http://127.0.0.1:8000/health
```
