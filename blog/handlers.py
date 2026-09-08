from blog.models import Blogs, Category
from blog.media_handlers import S3Handler
from django.core.exceptions import ValidationError
import uuid
class BlogHandler:

    @classmethod
    def create_blog(cls, data):

        title = data.get("title")
        content = data.get("content")
        image = data.get("image")
        category_id = data.get("category_id")
        description = data.get("description")

        try:
            category = Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            return None

        public_url = None

        if image:
            try:
                image_bytes = image.read()

                filename = f"blog_images/{uuid.uuid4()}_{image.name}"

                public_url = S3Handler.upload_file_to_s3(
                    file_bytes=image_bytes,
                    file_path=filename
                )

            except Exception as e:
                print("Error uploading image:", str(e))
                return 

        blog = Blogs.objects.create(
            title=title,
            content=content,
            image_url=public_url,
            category=category,
            description=description
        )

        return blog.blog_id, public_url
   
    @classmethod
    def edit_post(cls, post_id, data):
        try:
            blog = Blogs.objects.get(blog_id=post_id)
            blog.title = data.get('title', blog.title)
            blog.content = data.get('content', blog.content)
            blog.image_url = data.get('image_url', blog.image_url)
            blog.image = data.get('image', blog.image)
            blog.description = data.get('description', blog.description)
            category_id = data.get('category_id')
            if category_id:
                category = Category.objects.get(category_id=category_id)
                blog.category = category
            blog.save()
            return blog
        except Blogs.DoesNotExist:
            return False

    @classmethod
    def get_posts(cls, post_id=None):
        try:
            if post_id:
                blog = Blogs.objects.get(blog_id=post_id)
    
                return {
                    "blog_id": blog.blog_id,
                    "title": blog.title,
                    "content": blog.content,
                    "image": blog.image.url if blog.image else None,
                    "image_url": blog.image_url,
                    "date_created": blog.created_at,
                    "category": blog.category.category_id if blog.category else None,
                    "category_name": blog.category.name if blog.category else None,
                    "description": blog.description,
                }
    
            blogs = Blogs.objects.all()
    
            return [
                {
                    "blog_id": blog.blog_id,
                    "title": blog.title,
                    "content": blog.content,
                    "image": blog.image.url if blog.image else None,
                    "image_url": blog.image_url,
                    "date_created": blog.created_at,
                    "category": blog.category.category_id if blog.category else None,
                    "category_name": blog.category.name if blog.category else None,
                    "description": blog.description,
                }
                for blog in blogs
            ]
    
        except Blogs.DoesNotExist:
            return None

    @classmethod
    def delete_post(cls, post_id):
        try:
            blog = Blogs.objects.get(blog_id=post_id)
            #user id verification to be added here to check if the user is authorized to delete the post
            blog.delete()
            return True
        except Blogs.DoesNotExist:
            return False