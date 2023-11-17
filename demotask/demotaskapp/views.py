from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import requests

from .models import QueryResult


@csrf_exempt
@require_POST
def query(request):
    data = request.POST
    cadastre_number = data.get('cadastre_number')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    # Сохранение данных запроса пользователя в БД
    result = QueryResult.objects.create(cadastre_number=cadastre_number, latitude=latitude, longitude=longitude)
    result.save()
    # Отправка запроса на внешний сервис
    send_request_to_external_service(request, result)
    return JsonResponse({'id_request': result.id })

@csrf_exempt
@require_POST
def send_request_to_external_service(request, query_data):     # Функция отправки запроса на внешний сервис
    cadastre_number = request.POST.get('cadastre_number')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    url = 'http://localhost:8001/proccedquery/'  # URL второго сервиса
    try:
        response = requests.post(
            url, json={'cadastre_number': cadastre_number, 'latitude': latitude,
                       'longitude': longitude}, timeout=60
        )
        response_data = response.json()
        query_data.response = response_data.get('response')
        query_data.save()
        return JsonResponse({'message': "Response from external servise saved successfully"})
    except requests.exceptions.Timeout:
        return JsonResponse({'message': "Request timeout"})

@csrf_exempt
@require_POST
def get_result(request):   # Получение результата запроса со внешнего сервера
    data = request.POST
    id_request = data.get('id_request')
    response = QueryResult.objects.get(id=id_request)
    result = response.response
    return JsonResponse({'response': result})

@require_GET
def history(request):   # История всех запросов
    results = QueryResult.objects.all()
    history_list = []
    for result in results:
        history_list.append({
            'id': result.id,
            'cadastre_number': result.cadastre_number,
            'latitude': result.latitude,
            'longitude': result.longitude,
            'response': result.response,
            'timestamp': result.timestamp
        })
    return JsonResponse({"history": history_list})

@require_GET
def ping(request):   # Проверка, что  сервер запустился
    url = 'http://127.0.0.1:8001/check/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return JsonResponse({'message': "Server is running"})
    except requests.exceptions.RequestException:
        return JsonResponse({'message':"Server is not available"})