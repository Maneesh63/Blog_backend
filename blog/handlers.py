from blog.models import Blogs, Category

class BlogHandler:

    @classmethod
    def create_blog(cls, data):
        title = data.get('title')
        content = data.get('content')
        image_url = data.get('image_url')
        image = data.get('image')
        category_id = data.get('category_id')
        try:
           category = Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            return None
        blog = Blogs.objects.create(
            title=title,
            content=content,
            image_url=image_url,
            image=image,
            category=category
        )
        return blog.blog_id 
   
    @classmethod
    def edit_post(cls, post_id, data):
        try:
            blog = Blogs.objects.get(blog_id=post_id)
            blog.title = data.get('title', blog.title)
            blog.content = data.get('content', blog.content)
            blog.image_url = data.get('image_url', blog.image_url)
            blog.image = data.get('image', blog.image)
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
                    "category": blog.category.name if blog.category else None,
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
                    "category": blog.category.name if blog.category else None,
                }
                for blog in blogs
            ]
    
        except Blogs.DoesNotExist:
            return None

    # @classmethod
    # def delete_post(cls, post_id):
    #     try:
    #         blog = Blogs.objects.get(blog_id=post_id)
    #         #user id verification to be added here to check if the user is authorized to delete the post
    #         blog.delete()
    #         return True
    #     except Blogs.DoesNotExist:
    #         return False