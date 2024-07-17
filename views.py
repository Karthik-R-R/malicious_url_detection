from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate
from .models import URLAnalysis
from .models import MLModel
from .ml_model import analyze_url
from .serializers import ModelDetailsSerializer
from .serializers import FeedbackSerializer, UserRegistrationSerializer
from .serializers import URLAnalysisSerializer

class AnalyzeURL(APIView):
    def get(self, request):
        url = request.query_params.get('url', None)
        if url is None:
            return Response({"error": "URL parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        result = analyze_url(url)
        return Response({"url": url, "type": result}, status=status.HTTP_200_OK)
   
class SubmitFeedback(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FeedbackListCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save valid data to database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def analyze_url_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return render(request, 'analyze_form.html', {'error': 'URL parameter is missing'})
        
        try:
            result = analyze_url(url)
            context = {'url': url, 'result': result}
            return render(request, 'analyze_form.html', context)
        except Exception as e:
            return render(request, 'analyze_form.html', {'error': str(e)})
    
    elif request.method == 'GET' and 'url' in request.GET:
        url = request.GET.get('url')
        if not url:
            return HttpResponseBadRequest("URL parameter is missing")
        
        try:
            result = analyze_url(url)
            context = {'url': url, 'result': result}
            return render(request, 'analyze_result.html', context)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return render(request, 'analyze_form.html')

def analyze_url_form_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            return render(request, 'analyze_form.html', {'error': 'URL parameter is missing'})

        try:
            result = analyze_url(url)
            context = {'url': url, 'result': result}
            return render(request, 'analyze_form.html', context)
        except Exception as e:
            return render(request, 'analyze_form.html', {'error': str(e)})
    else:
        return render(request, 'analyze_form.html')

def analyze_url_api_view(request):
    url = request.GET.get('url')
    if not url:
        return HttpResponseBadRequest("URL parameter is missing")
    
    try:
        result = analyze_url(url)
        context = {'url': url, 'result': result}
        return render(request, 'analyze_result.html', context)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"status": "success", "userId": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class UserLogoutView(APIView):
    permission_classes = [] 

    def post(self, request, *args, **kwargs):
        try:
            token = request.auth
            if token:
                # Blacklist the token
                try:
                    BlacklistedToken.objects.create(token=OutstandingToken.objects.get(token=token))
                except OutstandingToken.DoesNotExist:
                    return Response({"status": "error", "message": "Invalid token"}, status=400)
                
                return Response({"status": "success", "message": "Token blacklisted successfully"}, status=200)
            else:
                return Response({"status": "error", "message": "No token provided"}, status=400)
        except (TokenError, InvalidToken) as e:
            return Response({"status": "error", "message": str(e)}, status=400)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=200)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=400)

@api_view(['PUT'])
def update_url_analysis(request, analysis_id):
    try:
        analysis = URLAnalysis.objects.get(pk=analysis_id)
    except URLAnalysis.DoesNotExist:
        return Response({"status": "error", "message": "Analysis does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Update the URL if provided in the request body
    if 'url' in request.data:
        new_url = request.data['url']
        analysis.url = new_url
        analysis.save()
        return Response({"status": "success", "message": "Analysis updated"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "message": "Missing 'url' in request body"}, status=status.HTTP_400_BAD_REQUEST)

class GetModelDetailsAPIView(APIView):
    def get(self, request, model_id):
        try:
            model = MLModel.objects.get(id=model_id)
            serializer = ModelDetailsSerializer(model)
            return Response({
                "status": "success",
                "modelDetails": serializer.data
            })
        except MLModel.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Model with ID {model_id} does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        
class ListUsersView(APIView):
    permission_classes = []

    def get(self, request):
        users = User.objects.all()
        user_list = [
            {
                "userId": user.id,
                "username": user.username,
                "email": user.email,
            }
            for user in users
        ]
        return Response({"users": user_list})

class UpdateURLAnalysisView(APIView):
    def put(self, request, analysis_id):
        try:
            # Retrieve existing URLAnalysis instance by analysis_id
            analysis = URLAnalysis.objects.get(id=analysis_id)

            # Update the URL with the new_url_string from request body
            new_url = request.data.get('url')

            if new_url:
                analysis.url = new_url
                analysis.save()

                return Response({"status": "success", "message": "Analysis updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message": "No URL provided in request body"}, status=status.HTTP_400_BAD_REQUEST)
        except URLAnalysis.DoesNotExist:
            return Response({"status": "error", "message": "Analysis not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Logic to delete the user
        user.delete()

        # Example response for demonstration
        return Response({"status": "success", "message": "User deleted"}, status=status.HTTP_200_OK)

class CreateURLAnalysisView(APIView):
    def post(self, request):
        serializer = URLAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

