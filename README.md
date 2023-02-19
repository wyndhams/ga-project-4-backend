# General Assembly Project Four - Festi: a Python Django API and React App

# Project Overview

This was my final project built on the Immersive Software Engineering course with General Assembly. It was a solo endeavour; all functionality within the site being coded by me from scratch over the course of a week.

Festi is a full-stack application designed to help users search for new music festivals for the summer months. This is the first project I have built using Django as the backend framework for api routing and using PostGreSQL to create the database of festivals. The app leverages React as a frontend framework and implements Material UI and CSS for styling.

Please find the full deployment of the app [here](https://festi-front-end.netlify.app/).

# Brief

- Build a full-stack application by making your own backend and your own front-end
- Use a Python Django API using Django REST Framework to serve your data from a Postgres database
- Consume your API with a separate front-end built with React
- Be a complete product which most likely means multiple relationships and CRUD functionality for at least a couple of models
- Implement thoughtful user stories/wireframes that are significant enough to help you know which features are core MVP and which you can cut
- Be deployed online so it's publicly accessible.
- Write your code DRY and build your APIs RESTful.
- Timeframe: 7 days

# Getting Started

Clone the backend repo using the SSH Key contained within the Code button above, then follow the steps below in a local Terminal window:

```sh
git clone <COPIED_SSH_KEY>
cd <NEWLY_CLONED_GIT_REPO>
```

Now you have navigated into the cloned git repo you can run the following commands:

```sh
pipenv install
```

```sh
pipenv shell
```

```sh
python manage.py makemigrations
```

```sh
python manage.py migrate
```

```sh
python manage.py runserver
```

Now you have the backend installed correctly and the server is running we can move onto the frontend:

Navigate to frontend repo [here](https://github.com/wyndhams/ga-project-4-frontend) then clone the repo on your local machine as above. Once you have changed your current directory to the newly cloned repo, use the following commands in your terminal window to install the necessary packages and launch the frontend on a localhost:

```sh
npm install
```

```sh
npm start
```

# Technologies Used

## Backend:

- Python
- Django
- Django REST Framework
- Psycopg2
- pyJWT

## Frontend:

- React
- Axios
- Material UI
- SCSS
- Http-proxy-middleware
- Nodemon
- React Router Dom

## Development tools:

- VS code
- npm
- Git
- Github
- Google Chrome dev tools
- Heroku (deployment)
- Netlify (deployment)
- Trello Board (planning and timeline)
- Excalidraw (wireframing)

# Planning

Once I had developed the initial concept for the application I undertook some market research to understand what products were out there already and what the unique selling point of my application was going to be. I looked at websites such as Resident Advisor, Skiddle and Festival Finder (.eu) for inspiration and to better understand where a niche could be found. As I was perusing these sites my main takeaway was either there were far too many results to choose from or the results that were being displayed when I was filtering for specific genres / artists were not relevant. A lot of festivals that I have been to which I would consider some of the better, albeit smaller, festivals were not showing up or were being lost in a noisy / crowded set of results.

I therefore set out to create a curated database of festivals, initially for electronic dance music (as this is my own area of interest / passion), that could be perused by an audience to find a new festival for the summer. I also wanted to display information about the festival including location, cost, size, time of year etc. in order for users to make an informed decision. Another concept that I wanted to embed in the design of the application was the ability for users to favourite festivals which could then be displayed in their own account page.

I was aware that working solo would make some of these targets unachievable given the limited time available so I created a wireframe, as below, of each of the pages and features that I wanted to include and (in orange) stretch targets should I have any addtional time at the end fo the project. I used the free online tool, Excallidraw to create the below wireframe.

<img src="./README_images/excalidraw-wireframe.png">

Before diving into Visual Studio Code I also had a think about the backend models that I was going to need to create and wrote this down in Excallidraw to explore the different interdependencies.

<img src="./README_images/app-relationships.png">

# Build Process

## Backend

The backend leveraged a Django REST Framework to build the web browsable API's for the application along with PostgreSQL for database build and manipulation. Firstly, I created a superuser (admin) prior to creating each of the separate apps.

### User Model

```py
class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        print(user_to_create)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({'message': "Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail='Invalid Credentials')
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Invalid Credentials')

        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode(
            {'sub': user_to_login.id, 'exp': int(dt.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return Response({'token': token, 'message': f"Welcome back {user_to_login.username}"})
```

This added functionality for registering an account with Festi and also gives the user the ability to login to their account. This uses a post request that I then tested in Postman to check that I was able to register and indeed login. I also tested this within the localhost devtools which showed a stored token within the Network section once logged in.

### Festivals Model

The main model for my application was the Festivals model. I added functionality into the view.py file which included routing for getting all festival data from the db, getting a single festival and included CRUD functionality. I wanted to gate the CRUD functionality to either admin users or registered non-admins, which I decided to do in the frontend (to be discussed below). I also added search functionality into the backend for which I created a new class as this required a new routing to call from the API. With reference to the below code, the query is a get request that filters the festivals model based upon the user inputted text, genres and artists.

```py
class FestivalSearch(APIView):
    def get(self, request):
        query = request.GET.get('search')
        print(query)
        results = Festival.objects.filter(Q(name__icontains=query) | Q(genres__icontains=query) | Q(artists__icontains=query))
        serialized_results = FestivalSerializer(results, many=True)
        return Response(serialized_results.data)
```

The festivals model needed to contain a number of different attributes that users could utilise to filter festivals and read information about them. See below models.py file excerpt which illustrates the various characteristics.

```py
class Festival(models.Model):
    name = models.CharField(max_length=100)
    cover_image = models.CharField(max_length=300)
    genres = models.ManyToManyField(
        'genres.Genre', related_name="festivals",  blank=True)
    artist = models.ForeignKey(
        'artists.Artist', related_name="festivals", on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    cost = models.CharField(max_length=100)
    month = models.CharField(max_length=30)
    capacity = models.CharField(max_length=30)
    owner = models.ForeignKey(
      'jwt_auth.User',
      related_name="festivals",
      on_delete=models.CASCADE
    )
```

## Frontend

I built the frontend of the application using React and a mix of Material UI and CSS for the styling. I created components for each of the respective pages where information was being displayed then hooked up the backend by adding a proxy in the package.json and creating a separate api.js file which utilised axios for hosting all of the necessary api routing for the app.

```js
const ENDPOINTS = {
  allFestivals: `${process.env.REACT_APP_BASE_URL}/api/festivals/`,
  ...,
  search: (query) =>
    `${process.env.REACT_APP_BASE_URL}/api/festivals/search?search=${query}`,
  cloudinary: `https://api.cloudinary.com/v1_1/${process.env.REACT_APP_CLOUDINARY_CLOUD_NAME}/image/upload/`,
};

const getHeaders = () => ({
  headers: {
    authorization: `Bearer ${AUTH.getToken()}`,
  },
});

const GET = (endpoint) => axios.get(endpoint);
const POST = (endpoint, body, headers) =>
  headers ? axios.post(endpoint, body, headers) : axios.post(endpoint, body);
const PUT = (endpoint, body, headers) => axios.put(endpoint, body, headers);
const DELETE = (endpoint, headers) => axios.delete(endpoint, headers);

export const API = { GET, POST, PUT, DELETE, ENDPOINTS, getHeaders };
```

I created a separate auth.js file to deal with jwt authorisation which perform the following functions:

- Storing the token in local storage when logging in / registering
- Removing the token from local storage when logging out
- Created a function to get the payload which I exported for utilisation in a custom hook useAuthenticated.js. This enabled gating for certain functionality within the app, e.g. only allowing admin to delete festivals or non-admin users to create festivals.

I have included the frontend functionality for a user search for a festival using words below.

```js
const filterFestivals = () => {
  const regex = new RegExp(searchQuery, 'i');
  const filteredFestivals = festivals.filter((festival) => {
    return festival.name.match(regex);
  });
  return filteredFestivals;
};
```

# Challenges

I utilised cloudinary for cloud storage of images uploaded for each of the festivals and user profile pictures. I also wanted to allow users to upload images of their profile and festivals they created to cloudinary to then be available for an api call to display on the Festivals pages and Account page. It took me a while to get this functionality to work.

# Highlights

I was particularly proud of the logic I implemented for calling a random new festival when the user is on the Single Festival information page.

```js
const getRandomFestival = (e) => {
  e.preventDefault();
  API.GET(API.ENDPOINTS.allFestivals)
    .then(({ data }) => {
      setNewFestivals(data);
      var randomInteger = Math.ceil(Math.random() * data.length - 1);
      if (randomInteger === 0) {
        randomInteger = 1;
      }
      navigate(`/festivals/${randomInteger}`);
    })
    .catch(({ message, response }) => {
      console.error(message, response);
    });
};
```

I included a button in the return statement and used the onClick() functionality to call the getRandomFestival function. This function makes an API call to get all festivals from the database then proceeds to get a random integer using Math.random() which is then used to navigate to the new festival. This works as the routing for each of the festivals is '/festivals/{Festival ID}'.

I was also pleased with the conditional logic I implemented for handling which festivals on the All Festivals page had been favourited. This added each of the selected festivals into an array in the selected constant. The function checks for whether the festival is already within the array and if it is, removes the festival.

```js
const [selected, setSelected] = useState([]);

const handleFavourite = (festival) => {
  if (selected.includes(festival)) {
    const newSelection = selected.filter((i) => i !== festival);
    setSelected(newSelection);
    console.log('SELECTED', selected);
  } else {
    setSelected([...selected, festival]);
    console.log('SELECTED', selected);
  }
};
```

Then in the return statement I had the following code again using the onClick() function to toggle the class of the button to change the color so the user could easily see which festivals had been favourited.

```js
{isLoggedIn && (
  <div key={festival.id}>
    <button
      key={festival.id}
     className={
     selected.includes(festival)
        ? classes.root
        : classes.notSelected
      }
      variant='contained'
      color='inherit'
      onClick={() => handleFavourite(festival)}
    >
    FAVOURITE
    </button>
  </div>
)}
```

# Future Development

Givent the challenging timescales associated with this final project I was not able to implement all of the functionality that I wanted to. I have listed below additional functionality that I will be continuing to work on for this application in the future.

- Enhance filter functionality to enable filtering from the home page using each of the different festival model attributes i.e. Country, Cost, Month etc.
- Display festivals that the user has favourited on the website within their Account page. At present I have hardcoded this for illustrative purposes. 
- Give users the ability to create reviews for each of the festivals and have these display within the user Account page as well as on the Single Festival pages. 
- Create a festival journal / blog component on the Account page. This will have a setting to either display publically or be private for the user. 