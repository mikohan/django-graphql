import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Quizzes, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category", "quiz")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")


class Query(graphene.ObjectType):

    elastic = graphene.String()

    def resolve_elastic(root, info):
        return f"this is elastic"

    one_quiz = graphene.Field(QuizzesType, id=graphene.Int())

    def resolve_one_quiz(root, info, id):
        return Quizzes.objects.get(id=id)

    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)


schema = graphene.Schema(query=Query)
