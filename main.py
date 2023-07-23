from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import get_hashed_password
import uvicorn

# signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}

@app.post("/registration", response_class=JSONResponse)
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    try:
        user_obj = await User.create(**user_info)
        new_user = await user_pydantic.from_tortoise_orm(user_obj)
        return {
            "status": "ok",
            "data": f"Hello, {new_user.username}, thanks for choosing our services. Please check your email inbox and click on the link to confirm your registration."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    user_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:
    
    if created:
        business_obj = await Business.create(
            business_name = instance.username, owner = instance
        )
        
        await business_pydantic.from_tortoise_orm(business_obj)
        # send a email

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models" : ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")