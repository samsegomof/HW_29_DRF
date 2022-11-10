import json

from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ads.models import Ad
from avito import settings
from users.models import User, Location


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    model = User
    qs = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(self, *args, **kwargs)
        self.object_list = self.object_list.order_by("username")

        paginator = Paginator(object_list=self.object_list, per_page=settings.TOTAL_ON_PAGE)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)

        result_method = []
        user_qs = Ad.objects.annotate(total_ads=Count("is_published"))

        for user in page_obj:
            result_method.append(
                {"id": user.id,
                 "first_name": user.first_name,
                 "last_name": user.last_name,
                 "username": user.username,
                 "password": user.password,
                 "role": user.role,
                 "age": user.age,
                 "locations": [user.location.name],
                 "total_ads": user_qs[user.id].total_ads,
                 })

        return JsonResponse(
            {"users": result_method,
             "Current_page": page_obj.number,
             "Total_users": page_obj.paginator.count
             },
            safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            password=data["password"],
            role=data["role"],
            age=data["age"]
        )

        for loc in data["locations"]:
            location, _ = Location.objects.get_or_create(name=loc)
            user.location.add(location)

        return JsonResponse(
            {"id": user.id,
             "first_name": user.first_name,
             "last_name": user.last_name,
             "username": user.username,
             "password": user.password,
             "role": user.role,
             "age": user.age,
             "locations": [str(u) for u in user.location.name],
             })


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.first_name = data["first_name"]
        self.object.last_name = data["last_name"]
        self.object.username = data["username"]
        self.object.password = data["password"]
        self.object.role = data["role"]
        self.object.age = data["age"]
        self.object.save()

        return JsonResponse(
            {"id": self.object.id,
             "first_name": self.object.first_name,
             "last_name": self.object.last_name,
             "username": self.object.username,
             "password": self.object.password,
             "role": self.object.role,
             "age": self.object.age,
             },
            safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "delete"}, status=204)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse(
            {"id": user.id,
             "first_name": user.first_name,
             "last_name": user.last_name,
             "username": user.username,
             "password": user.password,
             "role": user.role,
             "age": user.age,
             "locations": [user.location.name],
             "total_ads": user.ads.count(),
             },
            safe=False, json_dumps_params={"ensure_ascii": False})
