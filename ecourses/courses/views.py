from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Route, Buses, Comment, User, Like, Rating, Ticket
from .perms import CommentOwnerPerms
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from courses.util.charts import months, colorPrimary, colorPalette,colorSuccess, colorDanger, generate_color_palette, get_year_dict,  get_year_dict2

from .serializers import (
    CategorySerializer, RouteSerializer,
    BusesSerializer, BusesDetailSerializer,
    AuthBusesDetailSerializer,
    CommentSerializer, CreateCommentSerializer,
    UserSerializer
)

from .paginators import RoutePaginator
from drf_yasg.utils import swagger_auto_schema
from .perms import CommentOwnerPerms


class CategoryViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    def get_queryset(self):
        q = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)

        return q



class RouteViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Route.objects.filter(active=True)
    serializer_class = RouteSerializer
    pagination_class = RoutePaginator

    def get_queryset(self):
        queryset = self.queryset

        kw = self.request.query_params.get("kw")
        if kw:
            queryset = queryset.filter(destination__icontains=kw)

        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    @swagger_auto_schema(
        operation_description='Get the buses of a route',
        responses={
            status.HTTP_200_OK: RouteSerializer()
        }
    )
    @action(methods=['get'], detail=True, url_path='buses')
    def get_buses(self, request, pk):
        # course = Course.objects.get(pk=pk)
        course = self.get_object()
        buses = course.buses.filter(active=True)

        kw = request.query_params.get('kw')
        if kw:
            buses = buses.filter(destination__icontains=kw)

        return Response(data=BusesSerializer(buses, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class BusesViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Buses.objects.filter(active=True)
    serializer_class = BusesDetailSerializer

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthBusesDetailSerializer

        return BusesDetailSerializer

    def get_permissions(self):
        if self.action in ['like', 'rating']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @swagger_auto_schema(
        operation_description='Get the comments of a buses',
        responses={
            status.HTTP_200_OK: CommentSerializer()
        }
    )
    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        buses = self.get_object()
        comments = buses.comments.select_related('user').filter(active=True)

        return Response(CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        buses = self.get_object()
        user = request.user

        l, _ = Like.objects.get_or_create(buses=buses, user=user)
        l.active = not l.active
        try:
            l.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=AuthBusesDetailSerializer(buses, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='rating', detail=True)
    def rating(self, request, pk):
        buses = self.get_object()
        user = request.user

        r, _ = Rating.objects.get_or_create(buses=buses, user=user)
        r.rate = request.data.get('rate', 0)
        try:
            r.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=AuthBusesDetailSerializer(buses, context={'request': request}).data,
                        status=status.HTTP_200_OK)



class CommentViewSet(viewsets.ViewSet, generics.CreateAPIView,
                     generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [CommentOwnerPerms()]

        return [permissions.IsAuthenticated()]




class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class MyRouteView(generics.ListCreateAPIView):
    lookup_field = ['destination']
    queryset = Route.objects.filter(active=True)
    serializer_class = RouteSerializer


class MyRouteDetailView(generics.RetrieveAPIView):
    queryset = Route.objects.filter(active=True)
    serializer_class = RouteSerializer




@staff_member_required
def get_filter_options(request):
    grouped_purchases = Ticket.objects.annotate(year=ExtractYear('created_date')).values('year').order_by('-year').distinct()
    options = [purchase['year'] for purchase in grouped_purchases]

    return JsonResponse({
        'options': options,
    })


@staff_member_required
def count_buses_chart(request, year):
    purchases = Route.objects.filter(created_date__year__lte=year)
    grouped_purchases = purchases.annotate(buses_count=Count('my_buses')).values('destination', 'buses_count')

    count_buses_dict = get_year_dict2()

    for group in grouped_purchases:
        count_buses_dict[group['destination']] = round(group['buses_count'], 2)

    return JsonResponse({
        'title': f'Thống kê số lượng chuyến xe của tuyến xe {year}',
        'data': {
            'labels': list(count_buses_dict.keys()),
            'datasets': [{
                'label': '',
                'backgroundColor': [colorSuccess, colorDanger],
                'borderColor': [colorSuccess, colorDanger],
                'data': list(count_buses_dict.values()),
            }]
        },
    })



@staff_member_required
def get_sales_chart(request, year):
    purchases1 = Ticket.objects.filter(created_date__year=year)
    purchases = purchases1.filter(successful=True)
    grouped_purchases = purchases.annotate(price=F('buses__price')).annotate(month=ExtractMonth('created_date'))\
        .values('month').annotate(average=Sum('buses__price')).values('month','average').order_by('month')

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group['month']-3]] = round(group['average'], 3)

    return JsonResponse({
        'title': f'Doanh thu từng tháng theo năm {year}',
        'data': {
            'labels': list(sales_dict.keys()),
            'datasets': [{
                'label': 'VND(đ)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(sales_dict.values()),
            }]
        },
    })

@staff_member_required
def get_sales_chart2(request, year):
    purchases1 = Ticket.objects.filter(created_date__year=year)
    purchases = purchases1.filter(successful=True)
    grouped_purchases = purchases.annotate(price=F('buses__price')).annotate(month=ExtractMonth('created_date'))\
        .values('month').annotate(average=Sum('buses__price')).values('month','average').order_by('month')

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group['month']-1]] = round(group['average'], 2)
    a = list(sales_dict.values())
    b=[]
    b.append(a[0] + a[1]+ a[2]+a[3])
    b.append(a[4] + a[5]+ a[6]+a[7])
    b.append(a[11] + a[8]+ a[9]+a[10])

    return JsonResponse({
        'title': f'Doanh thu từng quý theo năm {year}',
        'data': {
            'labels': ["Quý 1", "Quý 2", "Quý 3"],
            'datasets': [{
                'label': 'VND(đ)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': b,
            }]
        },
    })


@staff_member_required
def spend_per_customer_chart(request, year):
    purchases1 = Ticket.objects.filter(created_date__year=year)
    purchases = purchases1.filter(successful=True)
    grouped_purchases = purchases.annotate(busesT=F('buses__name')).values('busesT').annotate(average=Sum('buses__price')).values('busesT', 'average')

    spend_per_customer_dict = get_year_dict2()

    for group in grouped_purchases:
        spend_per_customer_dict[group['busesT']] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Doanh thu từng chuyến xe năm {year}',
        'data': {
            'labels': list(spend_per_customer_dict.keys()),
            'datasets': [{
                'label': 'VND(đ)',
                'backgroundColor': [colorSuccess, colorDanger],
                'borderColor': [colorSuccess, colorDanger],
                'data': list(spend_per_customer_dict.values()),
            }]
        },
    })
