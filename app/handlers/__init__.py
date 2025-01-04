from app.handlers.classify import router as classify_router
from app.handlers.human_classifier import router as human_router
from app.handlers.animal_classifier import router as animal_router
from app.handlers.alien_classifier import router as alien_router

routers = [classify_router, human_router, animal_router, alien_router]