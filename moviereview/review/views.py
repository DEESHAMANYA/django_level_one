from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from review.models import Movie_details
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def basic(request):
    return HttpResponse("hello world")

def movie_info(request):
    movie = request.GET.get('movie')
    date = request.GET.get('date')
    return JsonResponse({'status':'success','result':{'movie_name':movie,'release_date':date}},status=200)
    
@csrf_exempt
def movies(request):
    if request.method == 'GET':
        Movie_info = Movie_details.objects.all() # FROM THAT TABLE IT WILL GET THE ALL THE AVAILABLE OBJECTS
        movie_list = []
        for movie in Movie_info:
            movie_list.append({
                "movie_name":movie.movie_name,
                "release_date":movie.release_date,
                "budget":movie.budget,
                "rating":movie.ratings
            })
        return JsonResponse({'status':'sucess','data':movie_list},status=200) 
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        print('PUT DATA',data)
        if data.get('movie_name'):
           ref_id = data.get('id')
           print('REFERENCE_ID: ',ref_id)
           existing_movie = Movie_details.objects.get(id = ref_id)
           print('existing data:',existing_movie)
           if data.get('movie_name'):
               new_movie_name = data.get('movie_name')
               existing_movie.movie_name = new_movie_name
               existing_movie.save()
           elif data.get('release_date'):
               new_release_date = data.get('release_date')
               existing_movie.release_date = new_release_date
               existing_movie.save()
           elif data.get('budget'):
               new_budget = data.get('budget')
               existing_movie.budget = new_budget
               existing_movie.save()
           elif data.get('rating'):
               new_rating = data.get('rating')
               existing_movie.ratings = new_rating
               existing_movie.save()
           return JsonResponse({'sattus':'success','message':'movie record updated sucessfully','data':data},status=400)

    elif request.method == 'DELETE':
        data = request.GET.get('id')
        ref_id = int(data)
        existing_movie = Movie_details.objects.get(id=ref_id)
        existing_movie.delete()
        return JsonResponse({'status':'success','message':'movie record deleted successfully'},status=200)

    elif request.method == 'POST':
        # data= json.loads(request.body) # whenever we send the data in json format we have to use this 
        data = request.POST # when we send data in from-data fromat we have to use this
        movie = Movie_details.objects.create(
            movie_name=data.get('movie_name'),
            release_date=data.get("release_date"),
            budget=data.get("budget"),
            ratings=data.get("rating")
            )
        return JsonResponse({"sattus":"success","message":"movie record inserted successfully","data":movie.id},status=200)
    return JsonResponse({"error":"error occured"},status=200)


