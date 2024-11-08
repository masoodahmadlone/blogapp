# blogapp/utils.py
def get_parent_comments(post):
    # Logic to retrieve parent comments for the post
    return post.comments.filter(parent=None)
