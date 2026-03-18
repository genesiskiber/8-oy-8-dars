from rest_framework.generics import ListAPIView
from .models import Course
from .serializers import CourseSerializer


class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        teacher = self.request.GET.get('teacher')

        if teacher:
            queryset = queryset.filter(teacher=teacher)

        return queryset