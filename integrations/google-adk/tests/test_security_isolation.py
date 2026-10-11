from memanto_google_adk.security import MemantoMemoryService


def test_explicit_agent_id_is_scoped_per_app(monkeypatch):
    service = MemantoMemoryService(api_key="test-key", agent_id="shared")

    app_a = service._agent("app-a")
    app_a_again = service._agent("app-a")
    app_b = service._agent("app-b")

    assert app_a.agent_id != app_b.agent_id
    assert app_a.agent_id == app_a_again.agent_id
    assert app_a.agent_id.startswith("shared-")
    assert app_b.agent_id.startswith("shared-")
