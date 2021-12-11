from fastapi.routing import APIRouter 
from serviceHandling.endpoints.billingapi import router as billing
from serviceHandling.endpoints.maths import router as Maths_utils
from serviceHandling.endpoints.login_and_signup import router as Login_and_signup

router = APIRouter()

router.include_router(billing)
router.include_router(Maths_utils)
router.include_router(Login_and_signup)