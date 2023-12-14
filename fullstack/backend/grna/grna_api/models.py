from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    """
    This class represents the predictions model.

    Attributes:
        dna (str): The DNA sequence.
        grna (str): The gRNA sequence.
        score (float): The score of the prediction.
        created_at (DateTimeField): The date and time the prediction was created.
        user (ForeignKey): The user who created the prediction.

    DNA max length: 400
    - Long single-stranded DNA (ssDNA, lssDNA or megamers) can be synthesized and sequence verified with lengths now extending to 2000 nucleotides. 
    - Recommendations for homology arms range from 100 to 400 nucleotides.

    gRNA max length: 20
    - Because gRNAs are 20 nucleotides long, the potential off-targets are limited to closely related sequences, 
    - hence off-site cleavage is relatively predictable and potentially avoidable.
    """
    dna = models.CharField(max_length=400, blank=True, null=True)
    grna = models.CharField(max_length=20, blank=True, null=True)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "predictions"

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.dna} - {self.grna} - {self.score}"
        else:
            return f"{self.dna} - {self.grna} - {self.score}"
