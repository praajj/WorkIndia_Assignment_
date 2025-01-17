from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer,TrainSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics,status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer,TrainAvailabilitySerializer  
from rest_framework.permissions import IsAdminUser
from .models import Train

class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_200_OK)

class AddTrainView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = TrainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TrainAvailabilityView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, *args, **kwargs):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')

        if not source or not destination:
            return Response({"error": "Source and destination are required."}, status=status.HTTP_400_BAD_REQUEST)

        trains = Train.objects.filter(source__iexact=source, destination__iexact=destination)

        if not trains.exists():
            return Response({"message": "No trains found for the given route."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TrainAvailabilitySerializer(trains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
