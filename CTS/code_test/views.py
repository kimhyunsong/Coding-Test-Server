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
        c = exec_with_return(eval(lines[0]))

        response = {
            "points": json.dumps(c)
        }
        return Response(response, status=status.HTTP_201_CREATED)