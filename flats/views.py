import jwt

# Create your views here.
from rest_framework import viewsets, views, status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import Flat, Resident, Invoice
from .serializers import FlatSerializer, ResidentSerializer, \
    MakePaymentSerializer, CreateFlatSerializer, InvoiceSerializer, ViewPaymentSerializer
from .match_operations import match_bulk, unmatch_bulk

# class IsSuperUser(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user and request.user.is_superuser
#
#
# class IsOwner(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user


class IsAuthorised(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        payload = jwt.decode(request.token, settings.SECRET_KEY)
        print(obj.building)
        print(payload)
        return obj.building == payload['building'], payload


class FlatViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny, )

    def retrieve(self, request, pk):
        instance = Flat.objects.get(pk=pk)
        serializer = FlatSerializer(instance)
        return Response(serializer.data)

    def list(self, request):
        queryset = Flat.objects.all()
        serializer = FlatSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = CreateFlatSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk):
        data = request.data
        instance = Flat.objects.get(pk=pk)
        serializer = CreateFlatSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResidentListViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ResidentSerializer
    queryset = Resident.objects.all()


class InvoiceAPIView(views.APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        order_by_list = ['flat', 'date']
        queryset = Invoice.objects.exclude(balance=0).order_by(*order_by_list)
        serializer = InvoiceSerializer(queryset, many=True)
        return Response(serializer.data)


class PaymentAPIView(views.APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = Flat.objects.all()
        serializer = ViewPaymentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        pk = request.data.pop('id', None)
        print(request.data)
        if pk is not None:
            instance = Flat.objects.get(pk=pk)
            serializer = MakePaymentSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({"error": "invalid flat"}, status=status.HTTP_400_BAD_REQUEST)


class BillMatchAPI(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        action = request.data.get('action', None)
        flat_ids = request.data.get('flat_ids', [])
        flats = Flat.objects.filter(pk__in=flat_ids)
        for flat in flats:
            if action == "match":
                match_bulk(flat)
            elif action == "unmatch":
                unmatch_bulk(flat)
            else:
                return Response({"error": "invalid operation"})
        return Response({"message": "update successful"}, status=status.HTTP_200_OK)
