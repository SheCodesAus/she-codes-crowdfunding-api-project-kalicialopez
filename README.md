# {{ EducAid }}

{{ EducAid is a non-for-profit online crowdfunding platform that aims to make highly rated, online educational courses/learning more accessible to those who are trying to better themselves, yet are limited by their financial situation. If it's a career change you're seeking Regardless of an individuals' highest level of education, current occupation/industry, EducAid can assist. 


Potential donors: Private enterprise, philanthropists and the general public, and even the participating institutions themselves could donate to get the ball rolling.
 }}

## Features

### User Accounts

- [X] Username
- [X] Email Address
- [X] Password

### Project

- [X] Create a project
  - [X] Title
  - [X] Owner (a user)
  - [X] Description
  - [X] Image
  - [X] Target Amount to fundraise
  - [X] Open/Close (Accepting new supporters)
  - [X] When was the project created
- [X] Ability to pledge to a project
  - [X] An amount
  - [X] The project the pledge is for
  - [X] The supporter
  - [X] Whether the pledge is anonymous
  - [X] A comment to go with the pledge
  
### Implement suitable update delete

**Note: Not all of these may be required for your project, if you have not included one of these please justify why.**

- Project
  - [X] Create
  - [X] Retrieve
  - [X] Update
  - [X] Destroy
- Pledge
  - [X] Create
  - [X] Retrieve
  - [x] Update
  - [x] Destroy
- User
  - [X] Create
  - [X] Retrieve
  - [ ] Update
  - [ ] Destroy

### Implement suitable permissions

**Note: Not all of these may be required for your project, if you have not included one of these please justify why.**

- Project
  - [x] Limit who can create *Default - must have authentication to create a project*
  - [ ] Limit who can retrieve *No authentication required to view projects*
  - [X] Limit who can update
  - [X] Limit who can delete
- Pledge
  - [x] Limit who can create *Default - must have an authentication to create a pledge*
  - [ ] Limit who can retrieve *No authentication required to view other users pledges*
  - [x] Limit who can update
  - [x] Limit who can delete
- User
  - [ ] Limit who can retrieve *Users cannot view other users User profile details, list view only hide personal details in list view?*
  - [X] Limit who can update
  - [x] Limit who can delete 

### Implement relevant status codes

- [x] Get returns 200
- [x] Create returns 201
- [x] Not found returns 404

### Handle failed requests gracefully 

- [x] 404 response returns JSON rather than text

### Use token authentication

- [X] implement /api-token-auth/

## Additional features

- [X] {Filtering }

{{ Filtering through existing project list based on a number of parameters }}

- [X] {Local search function}

{{ Search Function currently embedded into Filter }}

- [x] {Global Search Function} 

{{ Site-wide search function through both users and projects models }}

### External libraries used

- [x] django-filter


## Part A Submission

- [X] A link to the deployed project. https://little-silence-1263.fly.dev/
- [X] A screenshot of Insomnia, demonstrating a successful GET method for any endpoint.
- [X] A screenshot of Insomnia, demonstrating a successful POST method for any endpoint.
- [X] A screenshot of Insomnia, demonstrating a token being returned.
- [X] Your refined API specification and Database Schema. 
  
      *API Spec: https://docs.google.com/document/d/15uhUWko3P4Z2_bwiIbDz3tKzQwObk-tJgQqC9SFlBtA/edit?usp=sharing

      *Database Schema and MVP in 'Ben'.

### Step by step instructions for how to register a new user and create a new project (i.e. endpoints and body data).

1. Create User

```shell
curl --request POST \
  --url http://localhost:8000/users/ \
  --header 'Authorization: Token 7a56f8811047d79b47498ed97445a4a7ac7fcbc3' \
  --header 'Content-Type: application/json' \
  --data '{
	"first_name": "Harriette",
	"last_name": "Wells",
	"date_of_birth": "1998-08-09",
	"profile_picture": "http://t0.gstatic.com/licensed-image?q=tbn:ANd9GcSl2g-ek1913YE-0UKoWmzr1y-nXzJ59fBAWDH7klvHtc1saFzy8ynISmHCzc-S3n5ELMCPUf8xlomN2-w",
	"bio": "Hi, I'\''m Harriete :)",
	"country_of_residence": "Switzerland",
	"highest_level_of_education": "Technical entry",
	"username": "Harriette",
	"email": "harriettewells@gmail.com",
	"password": "harriettewells",
	"repeat_password": "harrygeorge"
}'
```



2. Sign in User

```shell
curl --request POST \
  --url http://localhost:8000/api-token-auth/ \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "admin",
	"password": "bigboss2"
}'
```

3. Create Project

```shell
curl --request POST \
  --url http://localhost:8000/projects/ \
  --header 'Authorization: Token 7a56f8811047d79b47498ed97445a4a7ac7fcbc3' \
  --header 'Content-Type: application/json' \
  --data '{
	"title": "Fat panda",
	"description": "Squish the fat panda!",
	"goal": 12.5,
	"image": "https://cff2.earth.com/uploads/2022/01/18083629/Giant-pandas2-960x640.jpg",
	"is_open": true,
	"date_created": "2023-01-29T04:01:05.630Z"
}'
```