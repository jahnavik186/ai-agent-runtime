from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "ai-github-contributor-automation-agent"


def test_analyze_endpoint():
    response = client.post(
        "/api/analyze",
        json={"repo": "open-source-labs/api-docs-toolkit", "branch": "main"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["repo"] == "open-source-labs/api-docs-toolkit"
    assert payload["branch"] == "main"
    assert len(payload["issues"]) >= 1
    assert {"id", "title", "severity", "file_path", "rationale"} <= set(payload["issues"][0].keys())


def test_demo_endpoint():
    response = client.post(
        "/api/demo",
        json={
            "repo": "open-source-labs/api-docs-toolkit",
            "branch": "main",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "analyze" in payload
    assert "fixes" in payload
    assert "pr_draft" in payload
    assert "docs_update" in payload
    assert payload["analyze"]["repo"] == "open-source-labs/api-docs-toolkit"
    assert payload["analyze"]["branch"] == "main"
    assert len(payload["fixes"]) >= 1
