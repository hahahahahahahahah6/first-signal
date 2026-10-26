"""Optional extension point. Core never imports an SDK or calls a model."""
import os
class LLMAdapter:
    def __init__(self):
        self.provider = os.environ.get('FIRSTSIGNAL_LLM_PROVIDER', '')
    def suggest(self, evidence):
        raise NotImplementedError('Optional adapter stub; deterministic Coach is fully functional.')
