from datetime import timezone, timedelta

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from perevalAPI.models import SpecificationOfPereval, User, Coordinates, Level, Images
from perevalAPI.serializers import SpecificationOfPerevalSerializer


class ObjectsForTests(APITestCase):
    def setUp(self):
        self.pereval1 = SpecificationOfPereval.objects.create(
            beauty_title='гора.',
            title='Эльбрус',
            other_titles='Вершина',
            connect='',
            user=User.objects.create(
                username='user1',
                email='user1@mail.ru',
                fam='Фамилия',
                name='Имя',
                otc='Отчество',
                phone='+0 000 000-00-00'
            ),
            coords=Coordinates.objects.create(
                latitude='43.348788',
                longitude='42.445124',
                height='5642'
            ),
            level=Level.objects.create(
                winter='V',
                spring='V',
                summer='V',
                autumn='V'
            ),
        )

        self.image_1 = Images.objects.create(
            data='https://turfirmarus.ru/assets/galleries/233/2.jpg',
            title='Описание',
            pereval=self.pereval1
        )

        self.pereval2 = SpecificationOfPereval.objects.create(
            beauty_title='гора.',
            title='Эльбрус',
            other_titles='Седловина',
            connect='',
            user=User.objects.create(
                username='user2',
                email='user1@mail.ru',
                fam='Фамилия',
                name='Имя',
                otc='Отчество',
                phone='+0 000 000-00-00'
            ),
            coords=Coordinates.objects.create(
                latitude='43.348788',
                longitude='42.445124',
                height='5642'
            ),
            level=Level.objects.create(
                winter='IV',
                spring='IV',
                summer='VI',
                autumn='VI'
            ),
        )

        self.image_1 = Images.objects.create(
            data='https://cdn.culture.ru/images/beaf2c77-3b60-5c9f-97e6-e850fe5d8ec5',
            title='Красивый вид на Эльбрус',
            pereval=self.pereval2
        )


class PerevalAPITestCase(ObjectsForTests):
    def test_get_list(self):
        url = f'{reverse("specificationofpereval-list")}?get_all=true'
        response = self.client.get(url)
        serializer_data = SpecificationOfPerevalSerializer([self.pereval1, self.pereval2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse('specificationofpereval-detail', args=(self.pereval1.id,))
        response = self.client.get(url)
        serializer_data = SpecificationOfPerevalSerializer(self.pereval1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class PerevalSerializerTestCase(ObjectsForTests):
    @staticmethod
    def formatting(date):
        moscow = timezone(timedelta(hours=3))
        date = date.astimezone(moscow)
        date = date.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')  # .isoformat()
        return date[:26] + date[29:]

    def test_get_list(self):
        serializer_data = SpecificationOfPerevalSerializer([self.pereval1, self.pereval2], many=True).data
        expected_data = [
            {
                'beauty_title': 'гора.',
                'title': 'Эльбрус',
                'other_titles': 'Вершина',
                'connect': '',
                'add_time': self.formatting(self.pereval1.add_time),
                'user': {
                    'email': 'user1@mail.ru',
                    'fam': 'Фамилия',
                    'name': 'Имя',
                    'otc': 'Отчество',
                    'phone': '+0 000 000-00-00'
                },
                'coords': {
                    'id': self.pereval1.coords.id,
                    'latitude': '43.348788',
                    'longitude': '42.445124',
                    'height': 5642
                },
                'status': 'new',
                'level': {
                    'id': self.pereval1.level.id,
                    'spring': 'V',
                    'summer': 'V',
                    'autumn': 'V',
                    'winter': 'V'
                },
                'images': [
                    {
                        'data': 'https://turfirmarus.ru/assets/galleries/233/2.jpg',
                        'title': 'Описание'
                    },
                ]
            },
            {
                'beauty_title': 'гора.',
                'title': 'Эльбрус',
                'other_titles': 'Седловина',
                'connect': '',
                'add_time': self.formatting(self.pereval2.add_time),
                'user': {
                    'email': 'user1@mail.ru',
                    'fam': 'Фамилия',
                    'name': 'Имя',
                    'otc': 'Отчество',
                    'phone': '+0 000 000-00-00'
                },
                'coords': {
                    'id': self.pereval2.coords.id,
                    'latitude': '43.348788',
                    'longitude': '42.445124',
                    'height': 5642
                },
                'status': 'new',
                'level': {
                    'id': self.pereval2.level.id,
                    'spring': 'IV',
                    'summer': 'VI',
                    'autumn': 'VI',
                    'winter': 'IV'
                },
                'images': [
                    {
                        'data': 'https://cdn.culture.ru/images/beaf2c77-3b60-5c9f-97e6-e850fe5d8ec5',
                        'title': 'Красивый вид на Эльбрус'
                    },
                ]
            },
        ]
        self.assertEqual(serializer_data, expected_data)
