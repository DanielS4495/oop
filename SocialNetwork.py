# Singleton Design Pattern
from datetime import datetime
import matplotlib.pyplot as plt
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Factory Design Pattern
class PostFactory:
    def create_post(self, post_type, **kwargs):
        try:
            if post_type == 'Text':
                print(f"{kwargs['created_by']} published a post:\n\"{kwargs['content']}\"\n")
                return TextPost(kwargs['post_id'], kwargs['content'], kwargs['created_at'], kwargs['created_by'])
            elif post_type == 'Image':
                print(f"{kwargs['created_by']} posted a picture\n")
                return ImagePost(kwargs['post_id'], kwargs['content'], kwargs['created_at'], kwargs['created_by'], kwargs['image_path'])
            elif post_type == 'Sale':
                print(f"{kwargs['created_by']} posted a product for sale:\nFor sale! {kwargs['description']}, price: {kwargs['price']}, pickup from: {kwargs['location']}\n")
                return SalePost(kwargs['post_id'], kwargs['content'], kwargs['created_at'], kwargs['created_by'], kwargs['description'], kwargs['price'], kwargs['location'])
            else:
                raise ValueError("Invalid post type")
        except Exception as e:
            print("An error occurred:", e)

class Observer:
    def update(self, message):
        pass

from datetime import datetime
class User(Observer):
    def __init__(self, user_id, username, password, social_network):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.password = password
        self.date_joined = datetime.now()
        self.logged_in = False
        self.followers = []
        self.following = []
        self.posts = []
        self.notifications = []
        self.social_network = social_network

    def create_post(self, content):
        post = Post(len(self.posts) + 1, content, datetime.now(), self)
        self.posts.append(post)
        for follower in self.followers:
            follower.add_notification(f"{follower.username} has a new post")
        return post

    def like_post(self, post):
        if post.created_by != self:
            print(f"notification to {post.created_by.username}: {self.username} liked your post")
            post.created_by.add_notification(f"{self.username} liked your post")

    def comment_on_post(self, post, comment):
        if post.created_by.username != self:
            print(f"notification to {post.created_by.username}: {self.username} commented on your post: {comment}")
            post.created_by.add_notification(f"{self.username} commented on your post")

    def follow(self, other_user):
        try:
            if other_user != self or self.username not in other_user.followres:
                other_user.followers.append(self)
                print(f"{self.username} started following {other_user.username}")
            else:
                raise (Exception("You can't follow yourself or your already following the other user."))
        except Exception as e:
            print("An error occurred:", e)

    def unfollow(self, other_user):
        flag = False
        try:
            if (self.username == other_user.username):
                raise (Exception("You can't follow yourself."))
            for follower in other_user.followers:
                if follower.username == self.username:
                    other_user.followers.remove(self)
                    print(f"{self.username} unfollowed {other_user.username}")
                    flag = True
            if not flag:
                raise (Exception("You dont follow other user."))
        except Exception as e:
            print("An error occurred:", e)

    def notify(self, message):
        self.notifications.append(message)
        print(message)

    def add_notification(self,message):
        self.notifications.append(message)
   
    def print_notifications(self):
        print(f"{self.username}'s notifications:")
        for notification in self.notifications:
            print(notification)

    def publish_post(self, post_type, ConOrPath, price=None, location=None):
        try:
            if not self.logged_in:
                raise PermissionError("User not logged in")
            else:
                post_id = len(self.posts) + 1
                created_at = datetime.now()
                post_factory = PostFactory()
                new_post = post_factory.create_post(post_type,post_id=post_id,content=ConOrPath,image_path=ConOrPath,created_at=created_at,created_by=self,description=ConOrPath,price=price,location=location)
                self.posts.append(new_post)
                for user in self.followers:
                    if self.username != user:
                        user.add_notification(f"{self.username} has a new post")
                return new_post
        except Exception as e:
            print("An error occurred:", e)
            return None

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"


class Post:
    def __init__(self, post_id, content, created_at, created_by):
        self.post_id = post_id
        self.content = content
        self.created_at = created_at
        self.created_by = created_by
        self.likes = []
        self.comments = []

    def like(self, user):
        self.likes.append(user)
        user.like_post(self)

    def comment(self, user, comment):
        self.comments.append((user, comment))
        user.comment_on_post(self,comment)

    def display(self):
        pass

    def __str__(self):
        if isinstance(self, TextPost):
            return f"{self.created_by.username} published a post:\n\"{self.content}\"\n"
        elif isinstance(self, ImagePost):
            return f"{self.created_by.username} posted a picture\n"
        elif isinstance(self, SalePost):
            return f"{self.created_by.username} published a sale post:\n{self.description}, price: {self.price}, pickup from: {self.location}"

class TextPost(Post):
    pass

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ImagePost(Post):
    def __init__(self, post_id, content, created_at, created_by, image_path):
        super().__init__(post_id, content, created_at, created_by)
        self.image_path = image_path

    def display(self):
        try:
            print(f"Shows picture")
            img = mpimg.imread(self.image_path)
            plt.imshow(img)
            plt.axis('off')
            plt.show()
        except Exception as e:
            print("An error occurred:", e)
            return None

class SalePost(Post):
    def __init__(self, post_id, content, created_at, created_by, description, price, location, available=True):
        super().__init__(post_id, content, created_at, created_by)
        self.description = description
        self.price = price
        self.location = location
        self.available = available

    def discount(self, percent, password):
        try:
            if self.created_by.password == password:
                if  isinstance(percent, int):
                    self.price -= (self.price * percent) / 100
                    print(f"Discount on {self.created_by.username} product! the new price is: {self.price}")
            else:
                raise PermissionError("Incorrect password for discount")
        except Exception as e:
            print("An error occurred:", e)
            return None

    def sold(self, password):
        try:
            if self.created_by.password == password:
                self.available = False
                print(f"{self.created_by.username}'s product is sold")
            else:
                raise PermissionError("Incorrect password for marking as sold")
        except Exception as e:
            print("An error occurred:", e)
            return None

    def __str__(self):
        status = "Available" if self.available else "Sold"
        return f"{self.created_by.username} posted a product for sale:\n{status}! {self.description}, price: {self.price}, pickup from: {self.location}\n"

class SocialNetwork(metaclass=Singleton):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.users = []
        print(f"The social network {name} was created!")

    def sign_up(self, username, password):
        try: 
            # Check if the username is already taken
            if any(user.username == username for user in self.users):
                raise (Exception(f"The username '{username}' is already taken."))
            # Check password length
            if not (4 <= len(password) <= 8):
                raise (Exception("Password length should be between 4 and 8 characters.")) 
        except Exception as e:
            print("An error occurred:", e)
            return None
        user_id = len(self.users) + 1
        new_user = User(user_id, username, password, self)
        self.users.append(new_user)
        new_user.logged_in = True
        return new_user

    def log_in(self, username, password):
        try:
            for user in self.users:
                if user.username == username:
                    if user.password == password:
                        if user.logged_in==True:
                            raise (Exception(f"already connected"))
                            return False
                        else:
                            user.logged_in = True
                            print(f"{username} connected")
                            return True
                    else:
                        raise (Exception("Incorrect password"))
                        return False
            raise (Exception("User not found"))
        except Exception as e:
            print("An error occurred:", e)
            return None

    def log_out(self, username):
        try:
            for user in self.users:
                if user.username == username:
                    if user.logged_in == True:
                        user.logged_in = False
                        print(f"{user.username} disconnected")
                        return None
                    else:
                        raise (Exception("User already disconnected"))
                        return None
            raise (Exception("User not found"))
        except Exception as e:
            print("An error occurred:", e)
            return None

    def get_user(self, username):
        try:
            for user in self.users:
                if user.username == username:
                    return user
            raise (Exception("User not found"))
        except Exception as e:
            print("An error occurred:", e)
            return None

    def __str__(self):
        result = "Twitter social network:\n"
        for user in self.users:
            result += user.__str__() + "\n"
        return result
