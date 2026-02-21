from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from loguru import logger

def find_env_file():
    """
    Locate a .env file by searching relative to this file's directory
    and parent directories.
    """
    current = Path(__file__).resolve().parent
    for _ in range(4):
        env_path = current / ".env"
        if env_path.exists():
            return str(env_path)
        current = current.parent
    return ".env"

ENV_FILE = find_env_file()

class LLMConfig(BaseSettings):
    provider: str
    model: str
    api_key: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="LLM_",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

class VLMConfig(BaseSettings):
    provider: str
    model: str
    api_key: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="VLM_",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

class GlobalConfig(BaseSettings):
    """
    Global configuration entry point with lazily
    initialized component configurations.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._llm_config = None
        self._vlm_config = None

    @property
    def llm_config(self) -> LLMConfig:
        if self._llm_config is None:
            self._llm_config = LLMConfig()
        return self._llm_config

    @property
    def vlm_config(self) -> VLMConfig:
        if self._vlm_config is None:
            self._vlm_config = VLMConfig()
        return self._vlm_config

# Check if .env file exists and warn if not
if not Path(ENV_FILE).exists():
    logger.warning(f"\n.env file not found at: {ENV_FILE}")
    logger.warning("Please create a .env file with required configuration.")
    logger.warning("See .env.example for reference.\n")


settings = GlobalConfig()
