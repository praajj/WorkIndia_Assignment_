from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer,TrainSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer,TrainAvailabilitySerializer,BookSeatSerializer 
from rest_framework.permissions import IsAdminUser
from .models import Train
from django.db import transaction
from rest_framework import status
from .models import Train, Booking

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
      
class BookSeatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BookSeatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        train = serializer.validated_data['train']

        try:
            with transaction.atomic():
                
                train = Train.objects.select_for_update().get(id=train.id)
                
                if train.booked_seats >= train.total_seats:
                    return Response({
                        "status": "error",
                        "message": "No seats available."
                    }, status=status.HTTP_400_BAD_REQUEST)

                
                train.booked_seats += 1
                train.save()

                booking = Booking.objects.create(
                    user=request.user,
                    train=train
                )

                return Response({
                    "status": "success",
                    "message": "Seat booked successfully.",
                    "booking_id": booking.id,
                    "train_name": train.train_name,
                    "train_number": train.train_number,
                    "booked_seats": train.booked_seats,
                    "available_seats": train.total_seats - train.booked_seats
                }, status=status.HTTP_201_CREATED)
        except Train.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Train not found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
