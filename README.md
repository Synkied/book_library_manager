# BookLibrary Manadger  
An online library.  

## Installation  

### Backend  

`sh  
    virtualenv . --python=python3  
    source ./bin/activate  
    pip install -r requirements.txt  
    make feed_db
`

### Frontend  

`sh  
    cd ./frontend
    yarn
`


## Usage  

### Backend  

`sh  
    source ./bin/activate  
    make export_start_flask  
`

### Frontend  

`sh  
    cd ./frontend
    yarn serve
`


Go to (http://localhost:8080/) and use the frontend.

## Launching Tests  

`sh  
    source ./bin/activate  
    cd ./invoice_parser  
    python manage.py test  
`