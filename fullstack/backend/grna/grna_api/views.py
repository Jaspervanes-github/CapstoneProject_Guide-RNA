from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from torch.utils.data import DataLoader
from transformers import DataCollatorWithPadding
import transformers
import re 

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
    
    def post(self, request, *args, **kwargs):
        """
        Creates a new prediction.
        """
        request_body = {
            "dna": request.data.get("dna")
        }

        # Cut the DNA sequence into 20-mers
        dna = request_body["dna"]

        if not dna:
            return Response(
                {"error": "DNA sequence not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(dna) < 20:
            return Response(
                {"error": "DNA sequence must be at least 20 characters long."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if re.search('[^ACTGactg]', dna):
            return Response(
                {"error": "DNA sequence must only contain A, C, G, T, or N."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dna_length = len(dna)
        twenty_mers = []

        for i in range(dna_length - 19):
            twenty_mers.append(dna[i:i+20])

        request_body["grna"] = twenty_mers

        # Preprocess the 20-mers for the AI model
        # Encode the 20-mers
        dataloader = preprocess(twenty_mers)

        # Load the AI model
        model = transformers.AutoModelForSequenceClassification.from_pretrained("fullstack/backend/grna/grna_api/ai_model")

        # Make predictions
        predictions = []
        for batch in dataloader:
            outputs = model(**batch)
            predictions.append(outputs.logits)

        request_body["predictions"] = [prediction.item() for prediction in predictions]

        # Calculate the average score
        score = sum(predictions) / len(predictions)
        request_body["score"] = score.item()
        
        return Response(request_body, status=status.HTTP_201_CREATED)

def preprocess(twenty_mers):
    tokenizer = transformers.AutoTokenizer.from_pretrained("fullstack/backend/grna/grna_api/ai_model")
    tokens = tokenizer(twenty_mers, padding=True, truncation=True, return_tensors="pt")
    dataloader = DataLoader(tokens, batch_size=1, collate_fn=DataCollatorWithPadding(tokenizer))

    return dataloader


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