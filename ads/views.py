import json

from django.db.models import Q
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from ads.models import Category, Ad
from ads.serializers import AdCreateSerializer, AdSerializer, AdUpdateSerializer, AdImageSerializer


def root(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(self, *args, **kwargs)
        qs = Category.objects.all()
        result_method = []

        for category in qs:
            result_method.append({"id": category.id, "name": category.name})
        return JsonResponse(result_method, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):
        data = json.loads(request.body)
        new_category = Category.objects.create(name=data["name"])

        return JsonResponse({"id": new_category.id, "name": new_category.name},
                            safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        category = Category.objects.create(name=data["name"])
        return JsonResponse({"id": category.id, "name": category.name},
                            safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()

        return JsonResponse({"id": self.object.id, "name": self.object.name},
                            safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=204)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({"id": category.id, "name": category.name},
                            safe=False, json_dumps_params={"ensure_ascii": False})


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        """Фильтр по id категории"""
        categories = request.GET.getlist('cat', None)
        cat_query = None

        for cat_id in categories:
            if cat_query is None:
                cat_query = Q(category__id__exact=cat_id)
            else:
                cat_query |= Q(category__id__exact=cat_id)

        if cat_query:
            self.queryset = self.queryset.filter(cat_query)

        """Фильтр по тексту объявления"""
        ad_name = request.GET.get('text', None)
        if ad_name:
            self.queryset = self.queryset.filter(
                name__icontains=ad_name
            )

        """Фильтр по местоположению пользователя"""
        user_location = request.GET.get('location', None)
        if user_location:
            self.queryset = self.queryset.filter(
                author__location__name__icontains=user_location
            )

        """Фильтр по цене"""
        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        if price_from:
            self.queryset = self.queryset.filter(
                price__gte=price_from
            )
        if price_to:
            self.queryset = self.queryset.filter(
                price__lte=price_to
            )

        return super().get(self, *args, **kwargs)


class AdCreateView(CreateAPIView):
    """Создание пользователя"""
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdDetailView(RetrieveAPIView):
    """Показ объявление по id"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdUpdateView(UpdateAPIView):
    """Обновить объявление по id"""
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer


class AdUploadImageView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdImageSerializer


class AdDeleteView(DestroyAPIView):
    """Удалить объявление по id"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
