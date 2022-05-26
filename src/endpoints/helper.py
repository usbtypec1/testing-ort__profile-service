from fastapi import APIRouter

import models

router = APIRouter()


@router.get('/genders', response_model=list[models.GenderOut])
async def get_genders():
    return [models.GenderOut(name=gender.name, value=gender.value) for gender in models.Gender]
