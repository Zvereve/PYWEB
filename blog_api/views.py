from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from blog.models import Note, Comment
from . import serializers, filters


class NoteListCreateAPIView(APIView):
    """ Представление, которое позволяет вывести весь список записей и добавить новую запись. """

    def get(self, request: Request):
        objects = Note.objects.all()
        serializer = serializers.NoteSerializer(
            instance=objects,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request: Request):
        # Передаем в сериалайзер (валидатор) данные из запроса
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
        serializer = serializers.NoteDetailSerializer(
            instance=note,
        )

        return Response(serializer.data)

    def put(self, request, pk):
        """Обновления записи"""
        note = Note.objects.get(pk=pk)
        if self.request.user != note.author:
            return Response('Вы не автор')

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
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return Response("/")
        except Note.DoesNotExist:
            return Response("<h2>Note not found</h2>")


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset\
            .order_by("date_add")\
            .select_related("author") \
            .prefetch_related("comment_set")

    def filter_queryset(self, queryset):
        public = self.request.query_params.get("Public", True)

        return filters.public_filter(queryset, public)

        # # todo выполняем оптимизацию many-to-one
        # return queryset \
        #     .filter(public=True) \
        #     .order_by("-create_at")\
        #     .select_related("author")

        # # todo выполняем оптимизацию one-to-many
        # return queryset \
        #     .filter(public=True) \
        #     .order_by("-create_at")\
        #     .select_related("author")\
        #     .prefetch_related("comment_set")

class CommentListCreateAPIView(APIView):
    """ Представление, которое позволяет вывести весь список записей """

    def get(self, request: Request):
        objects = Comment.objects.all()
        serializer = serializers.CommentSerializer(
            instance=objects,
            many=True,
        )
        return Response(serializer.data)