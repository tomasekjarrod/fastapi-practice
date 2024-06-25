from pydantic import BaseModel, Field

class MovieBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    rating: float = Field(..., ge=0, le=10)
    # director_id: int

    # Optionally, you can add validation rules here
    # For example, to ensure that the name is not empty
    # and the description is at least 10 characters long
    # name: str = Field(..., min_length=1)
    # description: str = Field(..., min_length=10)

# Use this model for creating new movies
class CreateMovie(MovieBase):
    pass

# Use this model for updating existing movies
class UpdateMovie(BaseModel):
    name: str = Field(default=None, max_length=100)
    description: str = Field(default=None, max_length=500)
    rating: float = Field(default=None, ge=0, le=10)

# Use this model to return a movie in responses
class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True
        
class DirectorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

    # Optionally, you can add validation rules here
    # For example, to ensure that the name is not empty
    # and the description is at least 10 characters long
    # name: str = Field(..., min_length=1)
    # description: str = Field(..., min_length=10)

# Use this model for creating new movies
class CreateDirector(DirectorBase):
    pass

# Use this model for updating existing movies
class UpdateDirector(DirectorBase):
    pass

# Use this model to return a movie in responses
class Director(DirectorBase):
    id: int

    class Config:
        orm_mode = True