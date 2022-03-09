from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from code_test.models import Problem, Solution
from .serializers import SolutionSerializer, ProblemSerializer
import json

import sys;
import os 
# Create your views here.
@api_view(['GET', 'POST'])
def check(request, problem_pk):
    
    problem = get_object_or_404(Problem, pk=problem_pk)
    inputdata = problem.answer
    temp = list(map(str, inputdata.split('\r\n')))
    
    
    
    if request.method == "GET":
        serializers = ProblemSerializer(problem)
        return Response(serializers.data)
    elif request.method == "POST":
        
        with open('code_test/algo/algo.py', 'w', encoding='UTF-8')as file:
            file.write(json.dumps(request.data['answer'], ensure_ascii=False))
        f = open('code_test/algo/algo.py', 'r')

        line = f.readline()
        
        line = line[1:len(line)-1]
        
        def exec_code(line):
            new_dict = {}
            
            code_list = list(map(str, line.split('\\n')))
            exec('\n'.join(code_list), None, new_dict)
            return new_dict
            
            
        
        sys.stdin=open('code_test/algo/input.txt', "r")
        
        correct = 0
        message = ''            
        exec_code(line)
        tc = 0
        if correct == tc:
            message = "pass입니다."
        else:
            message = f'틀렸습니다.테스트케이스 중 {correct}개 맞음'
        # code = compile(line, 'algo.py', 'eval')
        alert = {
            'message':message,
        }
        
        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(problem=problem)
            return Response(alert, status=status.HTTP_201_CREATED)