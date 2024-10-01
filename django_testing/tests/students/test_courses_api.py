from random import sample, choice

import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Student, Course
from django_testing import settings


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture()
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_create(client, student_factory):
    studs = student_factory(_quantity=3)
    count = Course.objects.count()
    data = {"name": "python", "students": [person.id for person in studs]}
    response = client.post("/api/v1/courses/", data)

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_retrieve(client, course_factory):
    course = course_factory(_quantity=1)

    response = client.get(f"/api/v1/courses/{course[0].id}/")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == course[0].name


@pytest.mark.django_db
def test_delete(client, course_factory):
    _course = course_factory(_quantity=1)
    count = Course.objects.count()

    response = client.delete(f"/api/v1/courses/{_course[0].id}/")

    assert response.status_code == 204
    assert Course.objects.count() == count - 1


@pytest.mark.django_db
def test_update(client, course_factory, student_factory):
    studs = student_factory(_quantity=3)
    _course = course_factory(_quantity=1, students=[studs[0]])
    count = Course.objects.count()
    data = {"students": [studs[0].id, studs[2].id]}

    response = client.patch(f"/api/v1/courses/{_course[0].id}/", data)
    res = response.json()

    assert response.status_code == 200
    assert Course.objects.count() == count
    assert res["name"] == _course[0].name


@pytest.mark.django_db
def test_list_retrieve(client, course_factory, student_factory):
    students_set = baker.prepare(Student, _quantity=3)
    _courses = course_factory(_quantity=3, students=students_set)

    response = client.get("/api/v1/courses/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    for i, course in enumerate(data):
        assert course["name"] == _courses[i].name


@pytest.mark.django_db
def test_filter_name(client, course_factory, student_factory):
    students_set = baker.prepare(Student, _quantity=16)
    _courses = course_factory(_quantity=8, students=sample(students_set, 2))
    target = choice(_courses)
    response = client.get(f"/api/v1/courses/?name={target.name}/")
    data = response.json()

    assert response.status_code == 200
    for course in data:
        assert course["name"] == target.name


@pytest.mark.django_db
def test_filter_id(client, course_factory, student_factory):
    students_set = baker.prepare(Student, _quantity=10)
    _courses = course_factory(_quantity=8, students=sample(students_set, 2))
    target = choice(_courses)
    response = client.get(f"/api/v1/courses/?id={target.id}")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == target.id


@pytest.mark.django_db
def test_max_count(client, settings):
    settings.MAX_STUDENTS_PER_COURSE = 3
    students = baker.prepare(Student, _quantity=10)
    data = {
        "name": "python",
        "students": [person.id for person in Student.objects.all()],
    }
    response = client.post("/api/v1/courses/", data)

    assert response.status_code == 201
    # response = client.patch('/api/v1/courses/', {
    #     'name': 'python',
    #     'students': [person.id for person in students[5]]
    # })
    # assert response.status_code != 201
