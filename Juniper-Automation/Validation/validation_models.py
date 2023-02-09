from pydantic import BaseModel, Field


class BGP(BaseModel):
    ASN: int = Field(gt=0, le=65535)
    group: str
    bgp_type: str = "internal"


class Model(BaseModel):
    BGP: BGP
