from rest_framework import serializers
from .models import Book, Gender
from copies.models import Copy
from rest_framework.views import Response


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = [
            "id",
            "name",
        ]


class BookSerializer(serializers.ModelSerializer):
    copies_count = serializers.IntegerField(write_only=True)
    copies = serializers.SerializerMethodField()
    folowers_count = serializers.SerializerMethodField()
    genders = GenderSerializer(many=True)

    def get_copies(self, obj: Book) -> dict:
        copies_count = obj.copies.count()

        copies_avaliable_count = obj.copies.filter(avaliable=True).count()

        return {
            "copies_count": copies_count,
            "copies_avaliable": copies_avaliable_count,
        }

    def get_folowers_count(self, obj: Book) -> int:
        folowers_count = obj.folowers.count()

        return folowers_count

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "synopsis",
            "genders",
            "language",
            "published_at",
            "added_at",
            "folowers_count",
            "copies_count",
            "copies",
        ]
        read_only_fields = [
            "copies",
            "folowers_count",
        ]

    def create(self, validated_data) -> Book:
        copies_number = validated_data.pop("copies_count")
        genders_list = validated_data.pop("genders")

        book_obj = Book.objects.create(**validated_data)

        copies_obj = [Copy(book=book_obj) for _ in range(copies_number)]

        for gender_dict in genders_list:
            gender_obj = Gender.objects.filter(name__iexact=gender_dict["name"]).first()

            if not gender_obj:
                gender_obj = Gender.objects.create(**gender_dict)

            book_obj.genders.add(gender_obj)

        Copy.objects.bulk_create(copies_obj)

        return book_obj


class BookDetailSerializer(serializers.Serializer):
    copies = serializers.IntegerField()
