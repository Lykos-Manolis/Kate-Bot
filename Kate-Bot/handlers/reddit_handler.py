from replit import db

def RedditOptimizer():
    while len(db["viewedPostIDs"]) > 1000:
        db["viewedPostIDs"].pop(0)