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
    def create_post(self, post_type, post_id, content, created_at, created_by, **kwargs):
        if post_type == 'Text':
            print(f"{created_by.username} published a post:\n\"{content}\"\n")
            return TextPost(post_id, content, created_at, created_by)
        elif post_type == 'Image':
            print(f"{created_by.username} posted a picture\n")
            return ImagePost(post_id, content, created_at, created_by, kwargs['image_path'])
        elif post_type == 'Sale':
            print(f"{created_by.username} posted a product for sale:\nFor sale! {kwargs['description']}, price: {kwargs['price']}, pickup from: {kwargs['location']}\n")
            return SalePost(post_id, content, created_at, created_by, kwargs['description'], kwargs['price'], kwargs['location'])
        else:
            raise ValueError("Invalid post type")


class Observer:
    def update(self, message):
        pass


# class Subject:
#     def __init__(self):
#         self._observers = set()
#
#     def add_observer(self, observer):
#         self._observers.add(observer)
#
#     def remove_observer(self, observer):
#         self._observers.remove(observer)
#
#     def notify_observers(self, message):
#         for observer in self._observers:
#             observer.update(message)

from datetime import datetime
class User(Observer):
    def __init__(self, user_id, username, password, social_network):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.password = password
        self.date_joined = datetime.now()
        self.logged_in = False
        self.followers = set()
        self.following = set()
        self.posts = []
        self.notifications = []
        self.social_network = social_network
       # social_network.add_observer(self)

    def create_post(self, content):
        post = Post(len(self.posts) + 1, content, datetime.now(), self)
        self.posts.append(post)
        for follower in self.followers:
            follower.add_notification(f"{follower.username} has a new post")
        return post

    def like_post(self, post):
        if post.created_by != self:
            # post.add_like(self)
            print(f"notification to {post.created_by.username}: {self.username} liked your post")
            post.created_by.add_notification(f"{self.username} liked your post")

    def comment_on_post(self, post, comment):
        # post.add_comment(self, comment)
        if post.created_by.username != self:
            print(f"notification to {post.created_by.username}: {self.username} commented on your post: {comment}")
            post.created_by.add_notification(f"{self.username} commented on your post")

    def follow(self, other_user):
        if other_user != self:
            other_user.followers.add(self)
            # self.following.add(other_user)
            print(f"{self.username} started following {other_user.username}")
        else:
            print("You can't follow yourself.")
        # for post in other_user.posts:
        #     self.notify(other_user, f"{self.username} started following you and you have a new post", "follow_post")

    def unfollow(self, other_user):
        other_user.followers.remove(self)
        # self.following.remove(other_user)
        print(f"{self.username} unfollowed {other_user.username}")

    def notify(self, message):
        self.notifications.append(message)
        print(message)

    def add_notification(self,message):
        self.notifications.append(message)

    # need to change!!!!!!!!!!!!!!!!!
    # def print_notifications(self):
    #     print(f"{self.username}'s notifications:")
    #     for notification in self.notifications:
    #         print(notification)
    #     for post in self.posts:
    #         for like in post.likes:
    #             if like != self:
    #                 print(f"{like.username} liked your post")
    #         for comment in post.comments:
    #             if comment[0] != self:
    #                 print(f"{comment[0].username} commented on your post")
    #     for follower in self.followers:
    #         for follower_post in follower.posts:
    #             if follower_post not in self.posts:
    #                 print(f"{follower.username} has a new post")
    #             for follower_like in follower_post.likes:
    #                 if follower_like == self:
    #                     print(f"{follower.username} liked {follower_post.created_by.username}'s post.")
    #             for follower_comment in follower_post.comments:
    #                 if follower_comment[0] == self:
    #                     print(f"{follower.username} commented on {follower_post.created_by.username}'s post: {follower_comment[1]}")

# /////////////
    # def print_notifications(self):
    #     print(f"{self.username}'s notifications:")
        
    #     # Collect notifications
    #     notifications = []

    #     for post in self.posts:
    #         for like in post.likes:
    #             if like != self:
    #                 notifications.append((like.username, f"{like.username} liked your post"))
    #         for comment in post.comments:
    #             if comment[0] != self:
    #                 notifications.append((comment[0].username, f"{comment[0].username} commented on your post"))

    #     for follower in self.followers:
    #         for follower.posts in follower.posts:
    #             if follower.posts not in self.posts:
    #                 notifications.append((follower.username, f"{follower.username} has a new post"))
    #             for follower_like in follower.posts.likes:
    #                 if follower_like == self:
    #                     notifications.append((follower.username, f"{follower.username} liked {follower.posts.created_by.username}'s post."))
    #             for follower_comment in follower.posts.comments:
    #                 if follower_comment[0] == self:
    #                     notifications.append((follower.username, f"{follower.username} commented on {follower.posts.created_by.username}'s post: {follower_comment[1]}"))

    #     # Print notifications in the order they were added
    #     for _, notification in notifications:
    #         print(notification)
        
    def print_notifications(self):
        print(f"{self.username}'s notifications:")
        for notification in self.notifications:
            print(notification)



    def publish_post(self, post_type, ConOrPath, price=None, location=None):
        if not self.logged_in:
            raise PermissionError("User not logged in")
        post_id = len(self.posts) + 1
        created_at = datetime.now()
        post_factory = PostFactory()
        if post_type == 'Text':
            new_post = post_factory.create_post(post_type, post_id, ConOrPath, created_at, self)
        elif post_type == 'Image':
            new_post = post_factory.create_post(post_type, post_id,content=None,created_at=created_at, created_by=self,image_path=ConOrPath)
        elif post_type == 'Sale':
          new_post = post_factory.create_post(post_type, post_id, content=None, created_at=created_at, created_by=self,image_path=None,description=ConOrPath,price=price,location=location)
        else:
            raise ValueError("Invalid post type")
        self.posts.append(new_post)
        for user in self.followers:
            if self.username != user:
                user.add_notification(f"{self.username} has a new post")
        return new_post

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers)}"


class Post:
    def __init__(self, post_id, content, created_at, created_by):
        self.post_id = post_id
        self.content = content
        self.created_at = created_at
        self.created_by = created_by
        self.likes = set()
        self.comments = []

    def like(self, user):
        self.likes.add(user)
        user.like_post(self)

    def comment(self, user, comment):
        self.comments.append((user, comment))
        user.comment_on_post(self,comment)

    # need to do a picture
    def display(self):
        pass

    def __str__(self):
        if isinstance(self, TextPost):
            return f"{self.created_by.username} published a post:\n\"{self.content}\"\n"
        elif isinstance(self, ImagePost):
            return f"{self.created_by.username} posted a picture\n"
        elif isinstance(self, SalePost):
            return f"{self.created_by.username} published a sale post:\n{self.description}, price: {self.price}, pickup from: {self.location}"
        else:
            return "Unknown post type"

class TextPost(Post):
    pass

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ImagePost(Post):
    def __init__(self, post_id, content, created_at, created_by, image_path):
        super().__init__(post_id, content, created_at, created_by)
        self.image_path = image_path

    def display(self):
        print(f"Shows picture")
        img = mpimg.imread(self.image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()

   


class SalePost(Post):
    def __init__(self, post_id, content, created_at, created_by, description, price, location, available=True):
        super().__init__(post_id, content, created_at, created_by)
        self.description = description
        self.price = price
        self.location = location
        self.available = available

    def discount(self, percent, password):
        if self.created_by.password == password:
            if  isinstance(percent, int):
                self.price -= (self.price * percent) / 100
                print(f"Discount on {self.created_by.username} product! the new price is: {self.price}")
        else:
            raise PermissionError("Incorrect password for discount")

    def sold(self, password):
        if self.created_by.password == password:
            self.available = False
            print(f"{self.created_by.username}'s product is sold")
        else:
            raise PermissionError("Incorrect password for marking as sold")

    def __str__(self):
        status = "Available" if self.available else "Sold"
        return f"{self.created_by.username} posted a product for sale:\n{status}! {self.description}, price: {self.price}, pickup from: {self.location}\n"

class SocialNetwork(metaclass=Singleton):
    # צריך לאכוף את זה שלא נוצר עוד אחד
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.users = []
        print(f"The social network {name} was created!")

    def sign_up(self, username, password):
        # Check if the username is already taken
        if any(user.username == username for user in self.users):
            print(f"The username '{username}' is already taken.")
            return None

        # Check password length
        if not (4 <= len(password) <= 8):
            print("Password length should be between 4 and 8 characters.")
            return None

        # Create a new user and add to the network
        user_id = len(self.users) + 1
        new_user = User(user_id, username, password, self)
        self.users.append(new_user)
        new_user.logged_in = True
        return new_user

    def log_in(self, username, password):
        for user in self.users:
            if user.username == username:
                if user.password == password:
                    if user.logged_in==True:
                        print(f"already connected")
                    else:
                        user.logged_in = True
                        print(f"{username} connected")
                        return True
                else:
                    print("Incorrect password")
                    return False
        print("User not found")
        return None

    def log_out(self, username):
        for user in self.users:
            if user.username==username:
                user.logged_in = False
                print(f"{user.username} disconnected")
                return None
        print("User not found")

    def get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def __str__(self):
        result = "Twitter social network:\n"
        for user in self.users:
            result += user.__str__() + "\n"
        return result
