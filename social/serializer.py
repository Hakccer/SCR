from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    v_password = serializers.CharField()
    # Validating data for creating user

    def validate(self, data):
        my_errors = ["", "", "", ""]

        # Getting Email Error if exists
        if "@" not in str(data['email']):
            my_errors[0] = "Invalid email try again '@' must be there"
        elif len(str(data['email'])) < 5:
            my_errors[0] = "email must be greater than 5 characters"
        elif len(User.objects.filter(email=data['email'])) > 0:
            my_errors[0] = "user with this email already exist"

        # Getting Password Error if exists
        if len(data['password']) < 9:
            my_errors[1] = "password field must be greater than 8 characters"

        if len(data['password']) < 9:
            my_errors[2] = "password field must be greater than 8 characters"

        # getting password validation error is exists
        if data['password'] != "" or data['v_password'] != "":
            if data['password'] != data['v_password']:
                my_errors[3] = "both the password fields must be same"

        for i in my_errors:
            if i != "":
                raise serializers.ValidationError(my_errors)

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        err_list = ["", "", ""]

        # Checking email
        if "@" not in str(data['email']):
            err_list[0] = "please enter a valid email"
        elif User.objects.filter(email=str(data['email'])) == 0:
            err_list[0] = "user with this email does'nt exist"

        # Checking Password
        if len(data['password']) < 9:
            err_list[1] = "password should be greater than 8 characters"

        for i in err_list:
            if i != "":
                raise serializers.ValidationError(err_list)

        return data


class AllPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'image', 'description']


class SinglePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'image', 'description', 'likes']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
