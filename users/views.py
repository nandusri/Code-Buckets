from .models import User
from .serializers import (
    UserSerializer, 
    UserDetailSerializer,
    UserResetPasswordSerializer
)
from rest_framework import status
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated, 
    AllowAny
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        queryset = User.objects.filter(pk = self.request.user.id)
        return queryset
    
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def sign_up(self, request):
        data = request.data
        data['username'] = data['email']
        user_serializer = UserSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        token = Token.objects.create(user=user)
        data['token'] = token.key
        print(user, data['token'])
        return Response({'data':data})
    
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token = Token.objects.filter(user=user).first()
                if not token:
                    token = Token.objects.create(user=user)
                return Response({
                    "is_authenticated": True,
                    "user": UserDetailSerializer(request.user).data,
                    "token": token.key,
                    "is_superuser": user.is_superuser
                })
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({"logged_out": True})
    
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        data = request.data
        password = data.get('password')
        old_password = data.get('old_password')
        if old_password is None or password is None:
            return Response({"message": "Old Password and New Password are Required."}, status=status.HTTP_403_FORBIDDEN)
        elif not request.user.check_password(old_password):
            return Response({"message": "Old password is Wrong."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            userQuerySet = User.objects.get(username=request.user.username)
            reset_password_serializer = UserResetPasswordSerializer(data=request.data)
            reset_password_serializer.is_valid(raise_exception=True)
            request.user.set_password(password)
            request.user.save()
            return Response({"message":"Password is updated"})