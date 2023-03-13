from rest_framework import serializers
from .models import Book, Gender, Follower, Avaliation
from copies.models import Copy
from .exceptions import ConflitcError
from statistics import mean


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
    followers_count = serializers.SerializerMethodField()
    genders = GenderSerializer(many=True)
    satisfaction_stars = serializers.SerializerMethodField()

    def get_copies(self, obj: Book) -> dict:
        copies_count = obj.copies.count()

        copies_avaliable_count = obj.copies.filter(avaliable=True).count()

        return {
            "copies_count": copies_count,
            "copies_avaliable": copies_avaliable_count,
        }

    def get_followers_count(self, obj: Book) -> int:
        followers_count = obj.followers.count()

        return followers_count

    def get_satisfaction_stars(self, obj: Book):
        star_list = [
            int(stars.satisfaction_stars)
            for stars in Avaliation.objects.filter(book=obj)
        ]
        return round(mean(star_list or [0]), 2)

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
            "followers_count",
            "satisfaction_stars",
            "copies_count",
            "copies",
        ]
        read_only_fields = [
            "copies",
            "followers_count",
        ]

    def create(self, validated_data) -> Book:
        book_obj = Book.objects.filter(
            title=validated_data["title"], language=validated_data["language"]
        ).first()

        if book_obj:
            raise ConflitcError

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


class FollowerSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Follower
        fields = ["id", "book_title", "username"]


class AvaliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliation
        fields = "__all__"
