from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from code_test.models import Problem, Solution
from .serializers import SolutionSerializer, ProblemSerializer
import json

import sys;
import os 

import ast
import copy



# Create your views here.
@api_view(['GET', 'POST'])
def check(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    inputdata = problem.answer
    def convertExpr2Expression(Expr):
        Expr.lineno = 0
        Expr.col_offset = 0
        result = ast.Expression(Expr.value, lineno=0, col_offset = 0)

        return result
    def exec_with_return(code):
        code_ast = ast.parse(code)

        init_ast = copy.deepcopy(code_ast)
        init_ast.body = code_ast.body[:-1]

        last_ast = copy.deepcopy(code_ast)
        last_ast.body = code_ast.body[-1:]

        exec(compile(init_ast, "<ast>", "exec"), globals())
        if type(last_ast.body[0]) == ast.Expr:
            return eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"),globals())
        else:
            exec(compile(last_ast, "<ast>", "exec"),globals())
    
    if request.method == "GET":
        serializers = ProblemSerializer(problem)
        return Response("serializers.data")
    elif request.method == "POST":
        with open('code_test/algo/algo.py', 'w', encoding='UTF-8')as file:
            file.write(json.dumps(request.data['answer'], ensure_ascii=False))
        f = open('code_test/algo/algo.py', 'r')

        lines = f.readlines()

        for line in lines:
            c = exec_with_return(eval(line))


        response = {
            "points": json.dumps(c)
        }

        #exec(lines)      
        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(problem=problem)
            return Response(response, status=status.HTTP_201_CREATED)





        # flag = False;
        # for line in lines:

            # if ":\\r\\n" in line:
            #     flag = True;
            # line = line.strip()
            # line = line.replace("\\n","\n")
            # line = line.replace("\\", "")
            # if flag:
            #     line = "    " + line.strip()
            #     flag = False;
            # line = line.replace(":\\r\\n", ":\n")
            # line = line.replace("\\r\\n", "\n")
            # line = line.replace("\\n","\n")
            # l

            # code = compile(line[1: len(line) - 1], "<string>", "exec")

        
        # line = line[1:len(line)-1]
        
        # def exec_code(line):
        #     new_dict = {}
            
        #     code_list = list(map(str, line.split('\\n')))
        #     exec('\n'.join(code_list), None, new_dict)
        #     return new_dict
            
            
        
        # sys.stdin=open('code_test/algo/input.txt', "r")
        
        # correct = 0
        # message = ''            
        # exec_code(line)
        # tc = 0
        # if correct == tc:
        #     message = "pass입니다."
        # else:
        #     message = f'틀렸습니다.테스트케이스 중 {correct}개 맞음'
        # # code = compile(line, 'algo.py', 'eval')
        # alert = {
        #     'message':message,
        # }