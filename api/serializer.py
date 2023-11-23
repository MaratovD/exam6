
from rest_framework import serializers
from django.template.defaultfilters import slugify
from .models import Category, Post, Author
from django.contrib.auth import authenticate


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2 ,max_length=250)
    slug = serializers.SlugField(read_only=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.slug = slugify(validated_data.get("title", instance.slug))
        instance.save()
        return instance

    def validate(self, attrs):
        title = attrs.get("title")
        return super().validate(attrs)

    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content" ,"slug", "image", "publish_date", "category", "author"]

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", isinstance.content)
        instance.slug = slugify(validated_data.get("title", instance.slug))
        instance.save()
        return instance

    def validate(self, attrs):
        title = attrs.get("title")
        return super().validate(attrs)

class AuthenSerialize(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["full_name", "bio"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)

    def check_user(self, validate_data):
        email= validate_data.get("email")
        password = validate_data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            return user
        else:
            raise serializers.ValidationError(detail={"error": "Login yoki parolingiz xato!"})
