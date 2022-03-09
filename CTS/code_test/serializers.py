from rest_framework import serializers
from .models import Solution
from .models import Problem


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('title','content',)



class SolutionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer("problem", read_only=True)    
    class Meta:
        model = Solution
        fields = ('id','user', 'answer', 'problem',) 
        
        