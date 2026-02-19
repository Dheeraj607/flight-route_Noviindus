from django.db import models

# Model to represent a node in a binary tree flight network
class AirportNode(models.Model):
    POSITION_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
    ]
    
    airport_code = models.CharField(max_length=10, unique=True)
    # Binary tree structure: each node can have one parent
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # Child position relative to parent
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, null=True, blank=True)
    # Weight of the edge leading to this node
    duration = models.PositiveIntegerField(help_text="Duration to reach this node from parent")
    
    class Meta:
        # Business Logic: A parent can only have one left and one right connection
        unique_together = ('parent', 'position')

    def __str__(self):
        if self.parent:
            return f"{self.airport_code} ({self.position} of {self.parent.airport_code})"
        return f"{self.airport_code} (Root)"
