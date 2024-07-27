from fastapi import APIRouter
from model.inst import Inst
import service.inst as service

router = APIRouter(prefix="/inst", tags=["inst"])

@router.post("/profile")
def download_profile(inst: Inst):
    return service.download_profile(inst)

@router.post("/posts")
def download_posts(inst: Inst):
    return service.download_posts(inst)

@router.post("/stories")
def download_stories(inst: Inst):
    return service.download_stories(inst)

@router.post("/hashtag")
def download_hashtag(inst: Inst):
    return service.download_hashtag(inst)

@router.post("/followers")
def download_followers(inst: Inst):
    return service.download_followers(inst)
