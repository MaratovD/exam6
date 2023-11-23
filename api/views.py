from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from .serializer import CategorySerializer, PostSerializer, AuthenSerialize, LoginSerializer
from .models import Category, Post, Author
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated


class AuthListCreateView(ListCreateAPIView):
    serializer_class = AuthenSerialize
    queryset = Author.objects.all()
    # authentication_classes = (SessionAuthentication, )
    # pagination_class = PageNumberPagination
    # permission_classes = (IsAuthenticatedOrReadOnly, )


    def perform_create(self, serializer):
        auth = serializer.save(user= self.request.user)
        return auth

    # def get_queryset(self):
    #     user_id = self.request.query_params.get("user", [])
    #     # if user_id:
    #     queryset = TaskCategory.objects.filter(user = self.request.user)
    #     # else:
    #     #     queryset = Task.objects.all()
    #     return queryset

    # def filter_queryset(self, queryset):
    #     queryset = super().filter_queryset(queryset)
    #     queryset.filter(deadline__date = timezone.datetime.now())
    #     return queryset


class AuthRetriveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AuthenSerialize
    queryset = Author.objects.all()
    lookup_field = "pk"


@api_view(http_method_names=("GET", "POST"))
def category_list_create_view(request: Request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many = True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

@api_view(http_method_names=("GET", "PUT", "PATCH", "DELETE"))
def category_detail_view(request: Request, slug: str):
    category = get_object_or_404(category, slug=slug)
    if request.method == "GET":
        serializer = CategorySerializer(instance=category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=category, validated_data=serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        category.delete()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)



class CategoryDetailAPIView(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_object(self):
        return get_object_or_404(Category, slug = self.kwargs.get("slug"))
    
    def get(self, request, slug):
        serializer = self.serializer_class(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        serializer = self.serializer_class(instance=self.get_object(), data=request.data, partial= True)
        serializer.is_valid()
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self,  request, slug):
        product = self.get_object()
        product.delete()
        return Response(data={}, status=status.HTTP_200_OK)


class PostAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        post = serializer.save()
        return post


class PostDetailAPIView(GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self):
        return get_object_or_404(Post, slug = self.kwargs.get("slug"))
    
    def get(self, request, slug):
        serializer = self.serializer_class(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        serializer = self.serializer_class(instance=self.get_object(), data=request.data, partial= True)
        serializer.is_valid()
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self,  request, slug):
        product = self.get_object()
        product.delete()
        return Response(data={}, status=status.HTTP_200_OK)



class LoginAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.check_user(serializer.validated_data)
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={"token": token.key})
    

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(data={"success": "Tizimdan chiqdingiz!"}, status=status.HTTP_200_OK)