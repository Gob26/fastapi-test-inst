import instaloader
from model.inst import Inst

def download_profile(inst: Inst):
    L = instaloader.Instaloader()
    L.login(inst.login, inst.password)
    L.download_profile(inst.profile, profile_pic_only=False, fast_update=True)
    return {"status": "success", "message": f"Profile {inst.profile} downloaded successfully"}

def download_posts(inst: Inst):
    L = instaloader.Instaloader()
    L.login(inst.login, inst.password)
    posts = L.get_profile_posts(inst.profile)
    for post in posts:
        L.download_post(post, target=inst.profile)
    return {"status": "success", "message": f"Posts for profile {inst.profile} downloaded successfully"}

def download_hashtag(inst: Inst):
    L = instaloader.Instaloader()
    L.login(inst.login, inst.password)
    posts = L.get_hashtag_posts(inst.profile)
    for post in posts:
        L.download_post(post, target=f"hashtag_{inst.profile}")
    return {"status": "success", "message": f"Hashtag {inst.profile} posts downloaded successfully"}

def download_stories(inst: Inst):
    L = instaloader.Instaloader()
    L.login(inst.login, inst.password)
    profile = instaloader.Profile.from_username(L.context, inst.profile)
    stories = profile.get_stories()
    for story in stories:
        for item in story.get_items():
            L.download_storyitem(item, target=inst.profile)
    return {"status": "success", "message": f"Stories for profile {inst.profile} downloaded successfully"}

def download_followers(inst: Inst):
    L = instaloader.Instaloader()
    L.login(inst.login, inst.password)
    profile = instaloader.Profile.from_username(L.context, inst.profile)
    followers = profile.get_followers()
    follower_list = [follower.username for follower in followers]
    return {"status": "success", "followers": follower_list}
