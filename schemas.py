from pydantic import BaseModel


class Country(BaseModel):
    name: str
    capital: str
    flags: str
