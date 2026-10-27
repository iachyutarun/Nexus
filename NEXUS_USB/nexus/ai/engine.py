import os
import glob
from nexus.config.settings import settings

class AIEngine:
    def __init__(self, output_callback=None, confirm_callback=None):
        self.engine_type = settings.get('ai_engine', 'rule')
        self.rule_engine = None
        self.local_model = None
        self.output_callback = output_callback or (lambda x: x)
        self.confirm_callback = confirm_callback or (lambda msg: True)
        self._init_engines()

    def _init_engines(self):
        from nexus.ai.rule_based import RuleBasedEngine
        self.rule_engine = RuleBasedEngine(self.output_callback, self.confirm_callback, self)
        self._auto_detect_model()

    def _auto_detect_model(self):
        if settings.get('local_model_enabled') and settings.get('local_model_path'):
            self._load_local_model()
            return
        try:
            usb_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            models_dir = os.path.join(usb_root, 'models')
            if not os.path.isdir(models_dir):
                return
            candidates = sorted(glob.glob(os.path.join(models_dir, '*.gguf')))
            if not candidates:
                return
            model_path = candidates[0]
            settings.set('local_model_path', model_path)
            settings.set('local_model_enabled', True)
            self._load_local_model()
            if self.local_model and self.local_model.available:
                if self.output_callback:
                    self.output_callback(f"[AUTO] Local model detected and enabled: {os.path.basename(model_path)}")
            else:
                if self.output_callback:
                    self.output_callback("[AUTO] GGUF model found, but inference backend unavailable. Install 'ctransformers' on the host to enable local AI.")
                self.engine_type = 'rule'
                self.local_model = None
        except Exception:
            pass

    def _load_local_model(self):
        try:
            from nexus.ai.local_model import LocalModelEngine
            self.local_model = LocalModelEngine(
                settings.get('local_model_path'),
                self.output_callback
            )
            if self.local_model.available:
                self.engine_type = 'local'
            else:
                self.engine_type = 'rule'
                self.local_model = None
        except Exception:
            self.local_model = None
            self.engine_type = 'rule'

    def process(self, text, username=None):
        if self.engine_type == 'local' and self.local_model:
            return self.local_model.generate(text)
        return self.rule_engine.process(text, username=username)

    def get_engine_name(self):
        if self.engine_type == 'local' and self.local_model:
            return 'LOCAL AI MODEL'
        return 'LOCAL COMMAND ENGINE'

    def enable_local_model(self, path=None):
        if path:
            settings.set('local_model_path', path)
        settings.set('local_model_enabled', True)
        self._load_local_model()
        return self.get_engine_name()

    def disable_local_model(self):
        settings.set('local_model_enabled', False)
        self.engine_type = 'rule'
        self.local_model = None
        return self.get_engine_name()

    def get_model_status(self):
        if self.engine_type == 'local' and self.local_model:
            backend = getattr(self.local_model, 'backend', None) or 'unknown'
            return f"Local model active: {backend} ({self.local_model.model_path})"
        if settings.get('local_model_path'):
            return f"Local model configured but inactive: {settings.get('local_model_path')}"
        return "No local model configured. Use 'model on <path>' after placing a GGUF model in models/"
