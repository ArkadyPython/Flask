import pydantic


class CreateAdvertisement(pydantic.BaseModel):
    title: str
    description: str
    owner: str

    @pydantic.field_validator("title")
    def normal_length_title(cls, v: str) -> str:
        if len(v) > 20:
            raise ValueError(f"Maximal length of title is 20")
        return v