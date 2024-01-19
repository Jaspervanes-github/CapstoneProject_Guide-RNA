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

import pandas as pd
import datasets

import os

# Create your views here.
class PredictionListApiView(APIView):
    permission_classes = [permissions.AllowAny]
    tokenizer_path = "./best_model/checkpoint-4455"
    model_path = "./best_model/checkpoint-4455"

    tokenizer_var = transformers.AutoTokenizer.from_pretrained(
        tokenizer_path,
        model_max_length=100,
        padding_side="right",
        use_fast=True,
        trust_remote_code=True,
        local_files_only=True,
    )
    
    model = transformers.AutoModelForSequenceClassification.from_pretrained(
        model_path,
        cache_dir=None,
        num_labels=1,
        trust_remote_code=True,
    )

    def tokenize_function(self, example):
        return self.tokenizer_var(example["seq"], truncation=True)

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

        df_twenty_mers = pd.DataFrame({'seq' : twenty_mers})
        raw_dataset = datasets.Dataset.from_pandas(df_twenty_mers)

        tokenized_dataset = raw_dataset.map(self.tokenize_function, batched=True)
        tokenized_dataset.set_format("torch")

        y_preds = []

        for row in tokenized_dataset:
            # Include the start index with each prediction
            y_preds.append({
                "index": y_preds.__len__(),
                "sequence": row['seq'],
                "score": self.model(row["input_ids"].unsqueeze(0), row["attention_mask"].unsqueeze(0))[0].item()
            })

        # Create a DataFrame from the predictions
        df_y_preds = pd.DataFrame(y_preds)

        # Sort by prediction score and reset index
        df_y_preds.sort_values(by=['score'], inplace=True, ascending=False)
        df_y_preds.reset_index(drop=True, inplace=True)

        # Get the top 10 predictions
        top_10 = df_y_preds.head(10)

        request_body = {
            "dna": dna,
            "top_10": top_10.to_dict(orient="records"),
            "all_predictions": df_y_preds.to_dict(orient="records")
        }

        return Response(request_body, status=status.HTTP_201_CREATED)

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