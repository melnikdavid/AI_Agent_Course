from pydantic import BaseModel, Field, ConfigDict


class SearchArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(min_length=1, max_length=200)


class AnalyzeArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = Field(min_length=1, max_length=200)


class Plan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    steps: list[str] = Field(min_length=1, max_length=5)


class SaveArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report: str = Field(min_length=1, max_length=12000)


class RememberArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    note: str = Field(min_length=1, max_length=1000)
