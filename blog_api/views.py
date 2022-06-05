from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from blog.models import Note, Comment
from . import serializers, filters
from django.db.models import Q


class NoteListCreateAPIView(APIView):
    """ Представление, которое позволяет вывести весь список записей и добавить новую запись. """
    #permission_classes = (IsAuthenticated, )

    def get(self, request: Request):
        objects = Note.objects.all()
        objects =objects.filter(Q(public=True) | Q(author=self.request.user))
        serializer = serializers.NoteSerializer(
            instance=objects,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request: Request):
        """ Передаем в сериалайзер (валидатор) данные из запроса"""
        serializer = serializers.NoteSerializer(data=request.data)

        # Проверка параметров
        if not serializer.is_valid():  # serializer.is_valid(raise_exception=True)
            return Response(
                serializer.errors,  # serializer.errors будут все ошибки
                status=status.HTTP_400_BAD_REQUEST
            )

        # Записываем новую статью и добавляем текущего пользователя как автора
        serializer.save(author=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class NoteDetailAPIView(APIView):
    """ Представление, которое позволяет вывести отдельную запись. """
    def get(self, request, pk):

        note = get_object_or_404(Note, pk=pk)
        if not((note.public == True) or (self.request.user == note.author)):
            return Response(f"У вас нет прав на просмотр {self.request.user == note.author}", status.HTTP_403_FORBIDDEN)

        serializer = serializers.NoteDetailSerializer(
            instance=note,
        )

        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        """Обновления записи"""
        note = Note.objects.get(pk=pk)
        if self.request.user != note.author:
            return Response('Вы не автор', status.HTTP_403_FORBIDDEN)

        serializer = serializers.NoteSerializer(
            instance=note, data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Не верные данные", status=status.HTTP_409_CONFLICT)

    def patch(self, request, pk):
        """Добавление комментария"""
        serializer = serializers.CommentSerializer(data=request.data)

        # Проверка параметров
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(author=request.user, note_id=pk)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )

    def delete(self, request, pk):
        note = Note.objects.get(pk=pk)
        if self.request.user != note.author:
            return Response('Вы не автор', status.HTTP_403_FORBIDDEN)
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return Response("Удален", status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response("Запись не найдена", status.HTTP_404_NOT_FOUND)


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NoteFilter
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(public=True) | Q(author=self.request.user))
        return queryset\
            .order_by("date_add")\
            .select_related("author") \
            .prefetch_related("comment_set")




class CommentListCreateAPIView(APIView):
    """ Представление, которое позволяет вывести весь список записей """

    def get(self, request: Request):
        objects = Comment.objects.all()
        serializer = serializers.CommentSerializer(
            instance=objects,
            many=True,
        )
        return Response(serializer.data)