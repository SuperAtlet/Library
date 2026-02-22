from pydantic import BaseModel,Field

class SBookAdd(BaseModel):
    title: str
    author: str
    year: int
    pages: int = Field(..., gt=10, description="Количество страниц (больше 10)")
    is_read: bool = False

class SBook(SBookAdd):
    id : int
    model_config = {
        "from_attributes": True
    }
