from rest_framework import generics, filters
from .models import Category, Tag, Post, Comment, Rating, Like
from .serializers import CategorySerializer, TagSerializer, PostSerializer, CommentCreateSerializer, RatingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .permissions import IsOwnerPermission, IsAdminOrActivePermission
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filetrset_fields = ['category', 'author']
    search_fields = ['title','tags__title']
    ordering_fields = ['created_at', 'title']

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    

    @action(methods=['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk
        # print(data['post'])
        rating = Rating.objects.filter(post=pk, author=request.user).first()
        print(rating)
        serializer = RatingSerializer(data=data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('Вы уже оставляли PATCH запрос')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data, status=201)
            elif rating and request.method == 'PATCH':
                 serializer.update(rating, serializer.validated_data)
                 return Response('update', status=204)
            

    @action(['Post'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.delete()
            message = 'disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(post=post, author=user, is_liked=True)
            like.save()
            massage = 'liked'
            
        return Response(message, status=201)
        
                

        # if request.method == 'POST':
        #     serializer.create(serializer.validated_data)
        #     return Response(serializer.data)
        # elif request.method == 'PATCH':
        #     rating = Rating.objects.filter(pk=pk, author=request.user)
        #     serializer.update(rating, serializer.validated_data)






# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['category']
#     search_fields = ['title', 'body']


# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer




# class CommentListCreateView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     # serializer_class = CommentCreateSerializer
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return CommentCreateSerializer
#         elif self.request.method == 'GET':
#             return CommentSerializer


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer


    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()




# class RatingView(viewsets.ModelViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer

#     def get_permissions(self):
#         if self.action in ['update', 'destroy', 'partial_update']:
#             self.permission_classes = [IsOwnerPermission]
#         elif self.action == 'create':
#             self.permission_classes = [IsAdminOrActivePermission]
#         elif self.action in ['list', 'retrive']:
#             self.permission_classes = [AllowAny]
#         return super().get_permissions()



    
  

    