from django.shortcuts import render
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import UserSerializer, LoginSerializer, AllPostSerializer, SinglePostSerializer, CommentSerializer
from django.contrib.auth.models import User
from django.core.cache import cache
import random
from django.conf import settings
from django.core.mail import send_mail
from uuid import uuid4
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# Method for sending mail


def sending_mail(gmail, token):
    subject = "Scrolliffy Wants Your Profile Needs to be verified"
    message = f"Paste This OTP in Authentication Field {token}"
    sender = settings.EMAIL_HOST_USER
    reciptent = [gmail]
    send_mail(subject, message, sender, reciptent)


# Simple Method for Otp generation
def generate_otp():
    otps = ""
    for i in range(6):
        otps += str(random.randint(0, 9))
    return otps


@api_view(['POST'])
def signup(request):
    try:
        req_data = request.data
        serial = UserSerializer(data=req_data)
        print(req_data)
        if serial.is_valid():

            # Generating and, backing up otp for server
            my_otp = generate_otp()
            cache.set(req_data['email'], "session", 600)
            cache.set(f"{req_data['email']}_otp", my_otp, 120)

            # Sending Otp
            sending_mail(req_data['email'], my_otp)
            return Response({
                "status": True,
                "data": serial.data
            })
        return Response({
            "status": False,
            "error": serial.errors
        })
    except Exception as e:
        return Response({
            'try_error': "Something Went Totally (please sign up again)"
        })


@api_view(['POST'])
def verify_user(request):
    data = dict(request.data)

    # Session Cheching
    if not cache.get(data['email']):
        return Response({
            'error': "Session expired please enter your details again in signup page"
        })

    # Otp Validation
    if not str(data['otp']).isdigit() and len(str(data['otp'])) != 6:
        return Response({
            'error': "otp should be of 6 characters and only digits"
        })

    # Otp session validation
    if not cache.get(f"{data['email']}_otp"):
        return Response({
            'error': "2 minutes over please generate new otp by clicking on resend otp"
        })

    # Otp succession handler
    if str(data['otp']) == cache.get(f"{data['email']}_otp"):

        # Using username as uuid field for unique username's and the jwt authentication process
        user = User.objects.create(email=str(data['email']), username=uuid4())
        user.set_password(data['v_password'])
        user.save()
        cache.delete(f"{data['email']}")
        cache.delete(f"{data['email']}_otp")
        return Response({
            'success': "User Created Successfully"
        })
    return Response({
        'error': "something went wrong (please re-signup using signup page)"
    })

# Resend Otp


@api_view(['POST'])
def resend_otp(request):
    try:
        data = request.data
        if not cache.get(f"{data['email']}_otp"):
            my_otp = generate_otp()
            sending_mail(data['email'], my_otp)
            return Response({
                'success': "Otp Resended Successfully"
            })
        else:
            return Response({
                'error': "you can resend otp after 2 minutes only"
            })
    except Exception as e:
        return Response({
            'error': "Something Went Totally Wrong"
        })


@api_view(['POST'])
def login(request):
    data = request.data
    serail = LoginSerializer(data=data)
    if serail.is_valid():
        if len(User.objects.filter(email=data['email'])) == 0:
            return Response({
                'req_jwt': False,
                'glob_error': "User with this credential's does'nt exist"
            })
        user = User.objects.filter(email=data['email'])[0]
        correct = user.check_password(data['password'])
        if correct:
            return Response({
                'req_jwt': True,
                'user': user.username
            })
        return Response({
            'req_jwt': False,
            'glob_error': "User with this credential's does'nt exist"
        })
    return Response({
        'req_jwt': False,
        'errors': serail.errors
    })


class AllPosts(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = JSONRenderer().render(
            AllPostSerializer(Post.objects.all(), many=True).data)
        return Response({
            'datas': data
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def SinglePost(request, pk):
    try:
        single_data = Post.objects.get(pk=pk)

        # Detecting My Like is Exist's or not ?
        myer = False
        my_self = request.user.pk
        if str(my_self) in json.loads(single_data.likes):
            myer = True

        # preparing data for sendings
        single_serial = SinglePostSerializer(single_data)
        return Response({
            'data': single_serial.data,
            'my_one': myer
        })
    except Exception as e:
        return Response({
            'error': "Data Not Found"
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def handle_liking(request):
    mare = request.user
    the_post = Post.objects.get(pk=request.data['posting'])

    data = list(json.loads(the_post.likes))
    print(data)
    if str(mare.pk) in json.loads(the_post.likes):
        data.remove(str(mare.pk))
    else:
        data.append(str(mare.pk))
    print(data)
    the_post.likes = json.dumps(data)
    the_post.save()

    return Response({
        'like_handled': True
    })


class CommentApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            ider = request.GET.get('post_id')
            all_coms = Comments.objects.filter(post=Post.objects.get(pk=ider))
            coms = CommentSerializer(all_coms, many=True).data
            return Response({
                'data': coms
            })
        except Exception as e:
            return Response({
                'error': "Something Went Totally Wrong"
            })

    def post(self, request):
        req_data = request.data
        if req_data['comment'] == "":
            return Response({
                'error': "comment cannot be blank"
            })

        poster = Post.objects.get(pk=req_data['post_id'])
        new_com = Comments.objects.create(
            comment=req_data['comment'],  post=poster, user=request.user.email)
        new_com.save()
        return Response({
            'data': "saved"
        })
