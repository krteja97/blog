from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from .models import User,Tweet,TweetLikes 
from django.template import RequestContext
import datetime

# Create your views here.

def index(request):
	if(checkUserSessionExists(request)):
		return redirect(userhome);
	else:
		message = 'Enter 8791';
		return render(request,'twitter/index.html', {'message' : message});
	

def register(request):
	if(checkUserSessionExists(request)):
		return HttpResponseNotFound("first logout you soab");

	if(request.method == 'GET'):
		return render(request,'twitter/register.html');
	if(request.method == 'POST'):
		name = request.POST['name'];
		username = request.POST['username']
		password = request.POST['password']
		dob = request.POST['dateofbirth']
		city = request.POST['city'];

		isProperUser = checkProperUserDetails(request);
		if(isProperUser == False):
			return HttpResponse("send valid parameters");
		if(isProperUser == True):
			try:
				newUser = User.objects.create(name = name,user_name = username,password = password,city = city,dob = dob);
				return HttpResponseRedirect("/twitter/login");
			except:
				return HttpResponseNotFound("send proper details");
		return isProperUser;


def login(request):
	if(request.method == 'GET'):
		if(checkUserSessionExists(request)):
			return redirect(userhome);
		else:
			return render(request,'twitter/login.html');

	if(request.method == 'POST'):
		myvar = checkValidityOfUser(request);
		if(myvar == False):
			return HttpResponseRedirect("/twitter/login");

		#proper user in this case
		elif(myvar == True):
			username = request.POST['username'];
			request.session['username'] = username;
			return redirect(userhome);
		else:
			return myvar;


def logout(request):
	try:
		if(checkUserSessionExists(request)):
			del request.session['username'];
		else:
			return HttpResponseNotFound("behenchod naatak math karna??");
	except:
		return redirect(index);
	return redirect(index);

def userhome(request):
	if(checkUserSessionExists(request)):
		return render(request,'twitter/userhome.html',{'username' : request.session['username']});
	else:
		return redirect(index);



####################---------------helper methods--------------################

#register
def checkProperUserDetails(request):
	name = request.POST['name'];
	username = request.POST['username']
	password = request.POST['password']
	dob = request.POST['dateofbirth']
	city = request.POST['city'];

	try:
		userInDbdetails = User.objects.get(user_name = username);
		return HttpResponse("choose other username");
	except:
		if(name == ''):
			return False;
		if(len(username) <= 6):
			return False;
		if(len(password) <= 8):
			return False;
		if(city == ''):
			return False;
		return True;


#login
def checkValidityOfUser(request):
	username = request.POST['username'];
	password = request.POST['password'];

	try:
		userInDbdetails = User.objects.get(user_name = username);
		if(password != userInDbdetails.password):
			return HttpResponseNotFound("wrong password");
		return True;
	except:
		return HttpResponseNotFound("send proper details");

def checkUserSessionExists(request):
	if(request.session.has_key('username')):
		#print(request.session['username']);
		return True;
	else:
		return False;



##################------postage of tweets----------################

def postTweet(request): 
	if(request.method == 'GET'):
		return HttpResponseNotFound("what the hell are you thinking??");
	if(request.method == 'POST'):
		heading = request.POST['heading']
		tweettext = request.POST['tweettext']

		myvar = checkProperTweet(request)
		if(myvar == False ):
			return HttpResponseNotFound("post proper tweet you ssoab");
		elif(myvar == True):
			#try:
				author = User.objects.get(user_name = request.session['username']);
				newTweet = Tweet.objects.create(heading = heading,tweettext = tweettext, 
					publish_date = datetime.datetime.now(), author = author);
				return HttpResponse("successfully posted");
			#except:
				return HttpResponseNotFound("sorry error occured");
		else:
			return myvar;




def tweets(request):
	if(checkUserSessionExists(request) == False):
		return redirect(index);
	else:
		myrecords = Tweet.objects.order_by('-publish_date')[0:10];
		# for x in myrecords:
		# 	print(x.tweettext);
		# 	print(x.author.user_name);
		# 	print(x.id);
		
		return render(request,'twitter/tweets.html',{'mytweets' : myrecords, 'username' : request.session['username']});


def individualtweet(request, tweetid):
	if(checkUserSessionExists(request) == False):
		return redirect(index);
	try:
		mytweet = Tweet.objects.get(pk=tweetid);
		userinDb = User.objects.get(user_name = request.session['username'] );
		try:
			countoflikes = TweetLikes.objects.filter(tweet = mytweet).count();
		except:
			countoflikes = 0;
		print(countoflikes);

		return render(request, 'twitter/individualtweet.html', {'mytweet' : mytweet, 
			'username' : request.session['username'],  'likescount' : countoflikes});
	except:
		return HttpResponseNotFound("tweet doesnt exist");


############# -------tweets checks -------------############

def checkProperTweet(request):
	heading = request.POST['heading']
	tweettext = request.POST['tweettext']

	try:
		tweetinDb = Tweet.objects.get(heading = heading);
		return HttpResponse("choose other heading");
	except:
		if(len(heading) <= 5):
			return HttpResponseNotFound("choose proper heading");
		if(len(tweettext) > 200 or len(tweettext) < 3):
			return HttpResponseNotFound("choose proper tweettext");
		return True;



############-------------------users------------#############

def users(request, usernamestring):
	if(checkUserSessionExists(request) == False ):
		return redirect(index);
	else:
		if(checkValidUsernameString(usernamestring) == False):
			return HttpResponseNotFound("behenchod gib proper user");
		else:
			userinDb = User.objects.get(user_name = usernamestring);
			mytweetslist = Tweet.objects.filter(author = userinDb).order_by('-publish_date')[:10];
			#return HttpResponse(userinDb.name + " " + userinDb.city + " " + userinDb.user_name + " " + str(userinDb.dob));
			return render(request, 'twitter/users.html',{'userlist' : userinDb, 'mytweets' : mytweetslist});






################-------------users--check----------------#######

def checkValidUsernameString(usernamestring):
	try:
		userinDb = User.objects.get(user_name = usernamestring);
		return True;
	except:
		return False;


#############-----------------tweets-likes-----------############

def checkProperTweetId(tweetid):
	try:
		tweetinDb = Tweet.objects.get(pk= tweetid);
		return True;
	except:
		return False;


def liketweet(request, tweetid):
	if(checkUserSessionExists(request) == False ):
		return redirect(index);
	if(request.method == 'GET'):
		return HttpResponseNotFound("Invalid request");
	if(request.method == 'POST'):
		if(checkProperTweetId(tweetid) == False):
			return HttpResponseNotFound("Invalid request!! tweet not found");
		else:
			## so tweetid is proper ##
			try:
				tweetinDb = Tweet.objects.get(pk=tweetid);
				userinDb = User.objects.get(user_name = request.session['username'] )
				userintweetlikesDb = TweetLikes.objects.get(tweet = tweetinDb,user = userinDb);

				if(userintweetlikesDb):
				## so user already liked the tweet
					TweetLikes.objects.get(tweet = tweetinDb,user = userinDb).delete();
					return HttpResponse("successfully unliked");					
				else:
					## so user hasn't liked the tweet
					TweetLikes.objects.create(tweet = tweetinDb, user = userinDb);

			except TweetLikes.DoesNotExist:
				TweetLikes.objects.create(tweet = tweetinDb, user = userinDb);
				return HttpResponse("successfully liked");
				