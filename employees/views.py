from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee

@csrf_exempt  # Eğer API dışarıdan çağrılacaksa, bunu kaldırıp frontend'de CSRF token ekleyebilirsin.
def register_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES.get('photo')

        if not name or not photo:
            return JsonResponse({'error': 'Name and photo are required'}, status=400)

        try:
            employee = Employee.objects.create(name=name, photo=photo)
            return JsonResponse({'message': 'Employee registered successfully', 'id': employee.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
