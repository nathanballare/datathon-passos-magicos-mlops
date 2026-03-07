import os
import base64
import pandas as pd
import requests
from datetime import datetime
from loguru import logger
from io import StringIO

GITHUB_TOKEN  = os.getenv("GITHUB_TOKEN")
GITHUB_REPO   = os.getenv("GITHUB_REPO", "Allhons/datathon-fiap")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
CSV_PATH      = "logs/predictions.csv"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def _get_file_sha() -> str | None:
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_PATH}"
    resp = requests.get(url, headers=HEADERS, params={"ref": GITHUB_BRANCH})
    if resp.status_code == 200:
        return resp.json()["sha"]
    return None


def _get_current_csv() -> pd.DataFrame:
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_PATH}"
    resp = requests.get(url, headers=HEADERS, params={"ref": GITHUB_BRANCH})
    if resp.status_code == 200:
        content = base64.b64decode(resp.json()["content"]).decode("utf-8")
        return pd.read_csv(StringIO(content))
    return pd.DataFrame()


def push_prediction_to_github(record: dict) -> bool:
    try:
        df_existing = _get_current_csv()
        df_new = pd.DataFrame([record])
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)

        csv_content = df_updated.to_csv(index=False)
        encoded = base64.b64encode(csv_content.encode("utf-8")).decode("utf-8")

        sha = _get_file_sha()
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_PATH}"

        payload = {
            "message": f"log: nova predição em {datetime.utcnow().isoformat()}",
            "content": encoded,
            "branch": GITHUB_BRANCH,
        }
        if sha:
            payload["sha"] = sha

        resp = requests.put(url, headers=HEADERS, json=payload)
        if resp.status_code in (200, 201):
            logger.info("Push no GitHub realizado com sucesso!")
            return True
        else:
            logger.error(f"Erro no push: {resp.status_code} - {resp.text}")
            return False

    except Exception as e:
        logger.error(f"Erro ao fazer push no GitHub: {e}")
        return False