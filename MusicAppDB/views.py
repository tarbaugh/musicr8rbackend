from django.shortcuts import render
from .forms import RegistrationForm, RetrieveForm
from .models import Users, ArtistAttributes, Artists, Ratings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers

@csrf_exempt
def registration(request):
	if request.method == 'POST':
		password = request.POST.get("password");
		username = request.POST.get("username");
		
		try:
			user = Users.objects.get(username = username)
		except Users.DoesNotExist:
			user = None

		if(user == None and username != "" and password != ""):
			newUser = Users(username = username, password = password)
			newUser.save()
		else:
			return HttpResponse("failure");
	else:
		return HttpResponse("failure");

	return HttpResponse("success");

@csrf_exempt
def rate(request):
	if(request.method == 'POST'):
		username = request.POST.get("username");
		songname = request.POST.get("songname");
		rating = request.POST.get("rating");
		artistname = request.POST.get("artistname");

		user = None;

		try:
			user = Users.objects.get(username=username);
		except Users.DoesNotExist:
			return HttpResponse("Failure: User nonexistant!")
		
		#Get the artist for the song, create if nonexistant
		try:
			song = Artists.objects.get(song = songname, artist=artistname);
		except Artists.DoesNotExist:
			try:
				artist = ArtistAttributes.objects.get(name = artistname);
			except ArtistAttributes.DoesNotExist:
				artist = ArtistAttributes(name = artistname, genre = "", birth_location = "", birth_year = 0);
				artist.save();
			song = Artists(song = songname, artist = artist);
			song.save();
		#Try and get the rating for that user and that song, return error if it exists
		try:
			rating = Ratings.objects.get(username=Users.objects.get(username=username),song=Artists.objects.get(song=songname, artist=ArtistAttributes.objects.get(name=artistname)));
			if(rating != None):
				rating.update(rating=rating);
				rating.save();
				return HttpResponse("Rating updated!");
		except Ratings.DoesNotExist:
			rating = Ratings(username=Users.objects.get(username=username),song=Artists.objects.get(song=songname),rating=rating);
			rating.save();
			return HttpResponse("Rating success!");

	
def averagerating(songname):
		ratings = Ratings.objects.filter(song=songname);
		totalrating = 0;
		if(ratings.count() == 0):
			return 0;
		for rating in ratings:
			totalrating += rating.rating;
		return totalrating/ratings.count();

@csrf_exempt
def songret(request):
	reg_form = RegistrationForm
	ret_form = RetrieveForm
	if request.method == 'POST':
		form = RetrieveForm(request.POST)
		if form.is_valid():
			ratings = Ratings.objects.get()
			context = {'reg_form': reg_form, 'ret_form': ret_form}

	else:
		context = {'reg_form': reg_form, 'ret_form': ret_form}

	return render(request, 'MusicAppDB/index.html', context)

@csrf_exempt
def getallsongs(request):
	if(request.method == 'GET'):
		qs = Artists.objects.all();
		for q in qs:
			q.avgrating = averagerating(q.song);
		qs_json = serializers.serialize('json', qs);
		return HttpResponse(qs_json, content_type='application/json')

@csrf_exempt
def artistret(request):
	reg_form = RegistrationForm
	ret_form = RetrieveForm
	if request.method == 'POST':
		form = RetrieveForm(request.POST)
		if form.is_valid():
			pass

	else:
		pass

	context = {'reg_form': reg_form, 'ret_form': ret_form}
	return render(request, 'MusicAppDB/index.html', context)

@csrf_exempt
def index(request):
	reg_form = RegistrationForm
	ret_form = RetrieveForm
	context = {'reg_form': reg_form, 'ret_form': ret_form}
	return render(request, 'MusicAppDB/index.html', context)

@csrf_exempt
def deletesong(request):
	if(request.method == 'POST'):
		songname = request.POST.get("song");
		Ratings.objects.filter(song=songname).delete();
		Artists.objects.filter(song=songname).delete();
		return HttpResponse("success");