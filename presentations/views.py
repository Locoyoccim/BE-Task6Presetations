from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import User, Presentation, PresentationUser, Slide
import json

# Create your views here.
# vista presentation_list
@csrf_exempt
def presentation_list(request):
    if request.method == 'GET':
        return get_presentations(request)
    elif request.method == 'POST':
        return create_presentation(request)
    elif request.method == 'DELETE':
        return delete_presentation(request)

# functions presentation_list
def get_presentations(request):
    presentations = Presentation.objects.all().values()
    
    data = []
    for presentation in presentations:
        user = User.objects.get(id=presentation['creator_id'])
        presentation['creator_id'] = user.nickname
        data.append(presentation)

    return JsonResponse(data, safe=False)

def create_presentation(request):
    body = json.loads(request.body)
    title = body.get('title')
    nickname = body.get('nickname')

    if not title or not nickname:
        return JsonResponse({'error': 'Title and nickname are required'}, status=400)

    user = User.objects.get(nickname=nickname)
    presentation = Presentation.objects.create(title=title, creator=user)
    PresentationUser.objects.create(user=user, presentation=presentation, role='CREATOR')

    response = {
        'id': presentation.id,
        'title': presentation.title,
        'creator_id': user.nickname,
        'created_at': presentation.created_at,
        'updated_at': presentation.updated_at

    }

    return JsonResponse(response, status=201)

def delete_presentation(request):
    body = json.loads(request.body)
    id = body.get('id')

    if not id:
        return JsonResponse({'error': 'id is required'}, status=400)
    presentation = Presentation.objects.get(id=id)

    presentation.delete()

    return JsonResponse({'message': 'Presentation deleted'}, status=200)

# vistas para join_presentation
@csrf_exempt
def join_presentation(request, presentation_id):
    if request.method == 'POST':
        return add_user_to_presentation(request, presentation_id)

# funciones para join_presentation
def add_user_to_presentation(request, presentation_id):
    body = json.loads(request.body)
    nickname = body.get('nickname')

    if not nickname:
        return JsonResponse({'error': 'Nickname is required'}, status=400)

    user = User.objects.create(nickname=nickname)
    presentation = get_object_or_404(Presentation, id=presentation_id)
    PresentationUser.objects.create(user=user, presentation=presentation, role='VIEWER')

    return JsonResponse({'message': f'User {nickname} joined presentation {presentation.title}'}, status=201)

#View slides presentation
def presentation_slides(request, presentation_id):
    if request.method == 'GET':
        return get_slides(request, presentation_id)
    
#FUNCTION PRESENTATION SLIDES
def get_slides(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    slides = list(Slide.objects.filter(presentation=presentation).values())
    return JsonResponse(slides, safe=False)

# Editar diapositiva
@csrf_exempt
def edit_slide(request, presentation_id, slide_id):
    if request.method == 'PUT':
        return update_slide(request, presentation_id, slide_id)

def update_slide(request, presentation_id, slide_id):
    body = json.loads(request.body)
    content = body.get('content')

    if content is None:
        return JsonResponse({'error': 'Content is required'}, status=400)

    slide = get_object_or_404(Slide, id=slide_id, presentation_id=presentation_id)
    slide.content = content
    slide.save()

    return JsonResponse({'message': f'Slide {slide_id} updated successfully'}, status=200)

# Gestionar usuarios en una presentación
@csrf_exempt
def manage_users(request, presentation_id):
    if request.method == 'GET':
        return get_users(request, presentation_id)
    elif request.method == 'PUT':
        return update_user_role(request, presentation_id)

def get_users(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    participants = list(PresentationUser.objects.filter(presentation=presentation).values())
    return JsonResponse(participants, safe=False)

def update_user_role(request, presentation_id):
    body = json.loads(request.body)
    user_id = body.get('user_id')
    role = body.get('role')

    if not user_id or not role:
        return JsonResponse({'error': 'User ID and role are required'}, status=400)

    participant = get_object_or_404(PresentationUser, id=user_id, presentation_id=presentation_id)
    participant.role = role
    participant.save()

    return JsonResponse({'message': f'Role for user {participant.user.nickname} updated to {role}'}, status=200)

# Unirse a una presentación
@csrf_exempt
def join_presentation(request, presentation_id):
    if request.method == 'POST':
        return add_user_to_presentation(request, presentation_id)

def add_user_to_presentation(request, presentation_id):
    body = json.loads(request.body)
    nickname = body.get('nickname')

    if not nickname:
        return JsonResponse({'error': 'Nickname is required'}, status=400)

    user = User.objects.create(nickname=nickname)
    presentation = get_object_or_404(Presentation, id=presentation_id)
    PresentationUser.objects.create(user=user, presentation=presentation, role='VIEWER')

    return JsonResponse({'message': f'User {nickname} joined presentation {presentation.title}'}, status=201)


# Diapositivas de una presentación
@csrf_exempt
def presentation_slides(request, presentation_id):
    if request.method == 'GET':
        return get_slides(request, presentation_id)

def get_slides(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    slides = list(Slide.objects.filter(presentation=presentation).values())
    return JsonResponse(slides, safe=False)

# Editar diapositiva
@csrf_exempt
def edit_slide(request, presentation_id, slide_id):
    if request.method == 'PUT':
        return update_slide(request, presentation_id, slide_id)

def update_slide(request, presentation_id, slide_id):
    try:
        body = json.loads(request.body)
        content = body.get('content')

        if not isinstance(content, dict):
            return JsonResponse({'error': 'Content must be a valid JSON object'}, status=400)

        slide = get_object_or_404(Slide, id=slide_id, presentation_id=presentation_id)

        slide.content = json.dumps(content)
        slide.save()

        return JsonResponse({'message': f'Slide {slide_id} updated successfully'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




# Gestionar usuarios en una presentación
@csrf_exempt
def manage_users(request, presentation_id):
    if request.method == 'GET':
        return get_users(request, presentation_id)
    elif request.method == 'PUT':
        return update_user_role(request, presentation_id)

def get_users(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    participants = list(PresentationUser.objects.filter(presentation=presentation).values())
    return JsonResponse(participants, safe=False)

def update_user_role(request, presentation_id):
    body = json.loads(request.body)
    user_id = body.get('user_id')
    role = body.get('role')

    if not user_id or not role:
        return JsonResponse({'error': 'User ID and role are required'}, status=400)

    participant = get_object_or_404(PresentationUser, id=user_id, presentation_id=presentation_id)
    participant.role = role
    participant.save()

    return JsonResponse({'message': f'Role for user {participant.user.nickname} updated to {role}'}, status=200)

# Modo de presentación
def presentation_mode(request, presentation_id):
    if request.method == 'GET':
        return view_presentation(request, presentation_id)

def view_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    slides = list(Slide.objects.filter(presentation=presentation).values())
    return JsonResponse({'presentation': presentation.title, 'slides': slides})

#LOGIN FUNCTION
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data= json.loads(request.body)
        nickname = get_object_or_404(User, nickname=data["nickname"])

        user_data = {
            "id": nickname.id,
            'nickname': nickname.nickname,
            'created_at': nickname.created_at,
            'updated_at': nickname.updated_at
        }
        
        return JsonResponse(user_data, safe=False)

        