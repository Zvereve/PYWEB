from datetime import datetime
from rest_framework import serializers
from blog.models import Note, Comment


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Note
        fields = (
            'title', 'message', 'date_add',
            'date_up', 'public', 'author', 'relevant', 'rating'
        )


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('author', 'note_id',  'comment')


class NoteDetailSerializer(serializers.ModelSerializer):
    """ Одна статья блога """
    author = serializers.SlugRelatedField(
        slug_field="username",  # указываем новое поле для отображения
        read_only=True  # поле для чтения
    )
    comment_set = CommentSerializer(many=True, read_only=True)  # one-to-many-relationships

    class Meta:
        model = Note
        fields = (
            'title', 'message', 'date_add', 'date_up', 'public', 'relevant', 'rating',  # из модели
            'author', 'comment_set',  # из сериализатора
        )

    def to_representation(self, instance):
        """ Переопределение вывода. Меняем формат даты в ответе """
        ret = super().to_representation(instance)
        # Конвертируем строку в дату по формату
        create_at = datetime.strptime(ret['date_add'], '%Y-%m-%dT%H:%M:%S.%f')
        create_up = datetime.strptime(ret['date_up'], '%Y-%m-%dT%H:%M:%S.%f')
        # Конвертируем дату в строку в новом формате
        ret['date_add'] = create_at.strftime('%d %B %Y %H:%M:%S')
        ret['date_up'] = create_at.strftime('%d %B %Y %H:%M:%S')
        return ret


class NoteUpdateSerializer(serializers.ModelSerializer):
    ...  # todo update fields

class QueryParamsCommentFilterSerializer(serializers.Serializer):
    ... #rating = serializers.ListField(child=)