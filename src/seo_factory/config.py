"""Runtime configuration from environment variables only."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    no_llm_mode: bool = Field(default=True, alias="NO_LLM_MODE")
    offline_mode: bool = Field(default=True, alias="OFFLINE_MODE")
    output_dir: Path = Field(default=Path("outputs"), alias="OUTPUT_DIR")
    seed: int = Field(default=42, alias="SEED")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("seed")
    @classmethod
    def validate_seed(cls, value: int) -> int:
        if value < 0:
            msg = "SEED must be >= 0"
            raise ValueError(msg)
        return value

    @field_validator("output_dir")
    @classmethod
    def validate_output_dir(cls, value: Path) -> Path:
        if not str(value).strip():
            msg = "OUTPUT_DIR must not be empty"
            raise ValueError(msg)
        return value
