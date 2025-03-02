from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee, Attendance
from .serializers import EmployeeSerializer
from django.core.exceptions import ValidationError

@api_view(['POST'])
def register_employee(request):
    """
    Çalışan kaydetme API'si
    """
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=201)
    return Response({"status": "error", "errors": serializer.errors}, status=400)

@api_view(['POST'])
def record_attendance(request):
    """
    Yoklama kaydetme API'si
    """
    employee_id = request.data.get("employee_id")
    attendance_type = request.data.get("type", "IN")  # Varsayılan giriş

    if not employee_id:
        return Response({"status": "error", "message": "Employee ID is required"}, status=400)

    employee = get_object_or_404(Employee, id=employee_id)

    try:
        attendance = Attendance.objects.create(employee=employee, type=attendance_type)
        return Response({
            "status": "success",
            "message": f"Attendance recorded for {employee.name}",
            "data": {"timestamp": attendance.timestamp, "type": attendance.get_type_display()}
        }, status=201)
    except ValidationError as e:
        return Response({"status": "error", "message": str(e)}, status=400)
    except Exception as e:
        return Response({"status": "error", "message": "An unexpected error occurred: " + str(e)}, status=500)
