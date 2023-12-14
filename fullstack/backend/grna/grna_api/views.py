from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import PredictionSerializer
from .models import Prediction

# Create your views here.
class PredictionListApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all predictions.
        """
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def get_one(self, request, *args, **kwargs):
    #     """
    #     Returns a single prediction.
    #     """
    #     prediction = Prediction.objects.get(pk=kwargs["pk"])
    #     serializer = PredictionSerializer(prediction)

    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Creates a new prediction.
        """
        data = {
            "dna": request.data.get("dna"),
            "grna": request.data.get("grna"),
            "score": request.data.get("score"),
            "user": request.user.id
        }

        serializer = PredictionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # def put(self, request, *args, **kwargs):
    #     """
    #     Updates a prediction.
    #     """
    #     prediction = Prediction.objects.get(pk=kwargs["pk"])

    #     if request.user.id != prediction.user.id or request.user.is_superuser == False:
    #         return Response(
    #             {"error": "You do not have permission to edit this prediction."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )

    #     serializer = PredictionSerializer(prediction, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
        
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
    
    # def delete(self, request, *args, **kwargs):
    #     """
    #     Deletes a prediction.
    #     """
    #     prediction = Prediction.objects.get(pk=kwargs["pk"])

    #     if request.user.id != prediction.user.id or request.user.is_superuser == False:
    #         return Response(
    #             {"error": "You do not have permission to delete this prediction."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )

    #     prediction.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)

class PredictionDetailApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns a single prediction.
        """
        prediction = Prediction.objects.get(pk=kwargs["pk"])

        if not prediction:
            return Response(
                {"error": "Prediction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PredictionSerializer(prediction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        """
        Updates a prediction.
        """
        prediction = Prediction.objects.get(pk=kwargs["pk"])

        if not prediction:
            return Response(
                {"error": "Prediction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.id != prediction.user.id or request.user.is_superuser == False:
            return Response(
                {"error": "You do not have permission to edit this prediction."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = {
            "dna": request.data.get("dna"),
            "grna": request.data.get("grna"),
            "score": request.data.get("score")
        }

        serializer = PredictionSerializer(prediction, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, *args, **kwargs):
        """
        Deletes a prediction.
        """
        prediction = Prediction.objects.get(pk=kwargs["pk"])

        if not prediction:
            return Response(
                {"error": "Prediction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.id != prediction.user.id or request.user.is_superuser == False:
            return Response(
                {"error": "You do not have permission to delete this prediction."},
                status=status.HTTP_403_FORBIDDEN
            )

        prediction.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)