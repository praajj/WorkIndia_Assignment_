from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView, AddTrainView,TrainAvailabilityView,BookSeatView
from .views import LoginView
urlpatterns = [
  path('register',RegisterUserAPIView.as_view()),
  path('login/', LoginView.as_view(), name='login'),
  path('add-train/', AddTrainView.as_view(), name='add-train'),
  path('trains/availability/', TrainAvailabilityView.as_view(), name='train-availability'),
  path('trains/book/', BookSeatView.as_view(), name='book-seat'),
]