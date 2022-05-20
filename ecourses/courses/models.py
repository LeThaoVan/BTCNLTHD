from django.db import models
from django.contrib.auth.models import AbstractUser

from ckeditor.fields import RichTextField


class User(AbstractUser):

    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Driver(ModelBase):  # tài xế
    name = models.CharField(max_length=100, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    phone_number = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=500)
    date_of_bird = models.DateField(null=True, blank=True, verbose_name=('Ngày sinh'))

    def __str__(self):
        return self.name


class Category(ModelBase):
    name = models.CharField(max_length=50, unique=True, verbose_name=('Điểm xuất phát'))  # xuat phat tu

    def __str__(self):
        return self.name


class Route(ModelBase):  # tuyen xe
    destination = models.CharField(max_length=100, unique=True, verbose_name=('Tên tuyến xe'))  # ten tuyen xe
    name = models.CharField(max_length=100, verbose_name=('Điểm đến'))  # diem den
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, verbose_name=('Điểm xuất phát'))

    def __str__(self):
        return self.destination

    class Meta:
        unique_together = ('destination', 'category')


class Buses(ModelBase):  # chuyến xe
    #content = RichTextField()
    name = models.CharField(max_length=100, unique=True, verbose_name=('Tên xe khách'))
    image = models.ImageField(null=True, blank=True, upload_to='buses/%Y/%m')
    time = models.TimeField(null=True, blank=True,
                            verbose_name=('Thời gian xuất phát')) #thoi gian xuất phát
    route_name = models.ForeignKey(Route, related_name='buses1',
                                    related_query_name='my_buses',
                                    on_delete=models.CASCADE, verbose_name=('Tên tuyến xe')) #tuyến xe
    price = models.IntegerField(null=True, verbose_name=('Giá'))
    driver_name = models.ForeignKey(Driver, unique=True, on_delete=models.CASCADE,
                                    verbose_name=('Tài xế chuyến xe')) #tài xế
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=('Ngày tạo'))
    updated_date = models.DateTimeField(auto_now=True, verbose_name=('Ngày cập nhật'))
    tags = models.ManyToManyField('Tag', blank=True,
                                  related_name='buses')
    viewers = models.ManyToManyField(User, through='UserBusesView')
    seats_status = models.BooleanField(default=True, verbose_name=('Tình trạng số ghế'))

    def __str__(self):
        return f'{self.name} ({self.price}đ)'

    class Meta:
        unique_together = ('name', 'route_name')


class UserBusesView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buses = models.ForeignKey(Buses, on_delete=models.CASCADE)
    counter = models.IntegerField(default=0)
    reading_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'buses')


class Ticket(ModelBase):
    name = models.CharField(max_length=22, verbose_name=('Họ tên người mua vé')) #tên người mua vé
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user nguoi mua ve
    buses = models.ForeignKey(to=Buses, on_delete=models.CASCADE, related_name='buses2',
                                    related_query_name='my_buses2',verbose_name=('Tên chuyến xe')) #chuyến xe
    phone_number = models.CharField(max_length=10, null=False)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=('Ngày tạo'))
    successful = models.BooleanField(default=False, verbose_name=('Tình trạng thanh toán'))

    def __str__(self):
        return self.name


class Comment(ModelBase):
    content = models.TextField()
    buses = models.ForeignKey(Buses, related_name='comments',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
         return self.content


class Tag(ModelBase):
        name = models.CharField(max_length=50, unique=True)

        def __str__(self):
            return self.name

class ActionBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buses = models.ForeignKey(Buses, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'buses')
        abstract = True


class Like(ActionBase):
    active = models.BooleanField(default=False)


class Rating(ActionBase):
    rate = models.SmallIntegerField(default=0)

