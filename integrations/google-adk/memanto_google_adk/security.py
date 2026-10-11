"""Security hardening for explicit Google ADK agent IDs.

An explicit ``agent_id`` used to be shared verbatim by every ADK app. If one
service instance served multiple apps, a user's memories could therefore
cross the app boundary because the memory tags only scoped by user. This
module keeps the public configuration model while deriving an app-scoped
backend agent for every app.
"""

from __future__ import annotations

import hashlib

from memanto.cli.client.sdk_client import SdkClient
from memanto_google_adk.memory import MemantoMemoryService as _BaseMemoryService
from memanto_google_adk.memory import _Agent


class MemantoMemoryService(_BaseMemoryService):
    """App-isolated Google ADK memory service.

    Explicit backend agent IDs are namespaced by ``app_name``. This prevents
    two ADK applications sharing the same configured agent ID from sharing
    user memories accidentally.
    """

    def _agent(self, app_name: str) -> _Agent:
        if not self._agent_id:
            return super()._agent(app_name)

        suffix = hashlib.sha256(app_name.encode("utf-8")).hexdigest()[:16]
        scoped_agent_id = f"{self._agent_id}-{suffix}"
        with self._agents_lock:
            if scoped_agent_id not in self._agents:
                self._agents[scoped_agent_id] = _Agent(
                    SdkClient(self._api_key), scoped_agent_id
                )
            return self._agents[scoped_agent_id]
