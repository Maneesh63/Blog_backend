from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from blog.models import Blogs, Category
from blog.serializers import CategorySerializer
from blog.handlers import BlogHandler

class CategorViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer   

class BlogCreateView(APIView):
    def post(self, request):
        data = request.data
        try:
            blog =  BlogHandler.create_blog(data)
        except Exception as e:
            return Response({'message': 'An error occurred while creating the post', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Post created successfully', 'blog_id': blog}, status=status.HTTP_201_CREATED)

    def patch(self, request, post_id):
        data = request.data
        try:
            blog = BlogHandler.edit_post(post_id, data)
            if not blog:
                return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': 'An error occurred while updating the post', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message': 'Post updated successfully', 'blog_id': blog.blog_id, 'title': blog.title}, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            post_id = request.query_params.get("post_id")
            blogs = BlogHandler.get_posts(post_id)
    
            if blogs is None:
                return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
            return Response({"message": "Posts fetched successfully", "blogs": blogs}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": "An error occurred while fetching posts","error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # def delete(self, request, post_id):
    #     try:
    #         blog = Blogs.objects.get(blog_id=post_id)
    #         blog = BlogHandler.delete_post(post_id)
             
    #         return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)
    #     except Blogs.DoesNotExist:
    #         return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"message": "An error occurred while deleting the post", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)