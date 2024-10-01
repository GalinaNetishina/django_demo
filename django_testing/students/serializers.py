from rest_framework import serializers

from students.models import Course, Student
from django_testing.settings import MAX_STUDENTS_PER_COURSE


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"

    students = StudentSerializer(read_only=True, many=True)

    def validate_students(self, students):
        if len(students) > 3:
            raise Exception(f"too many students for course {self.name}")
