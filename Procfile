# foreman start -m gateway=1,restaurants=3,users=3 -p 5000

# API Gateway that forwards requests upstream to services
gateway: FLASK_APP=gateway flask run -p $PORT

# Users service
users: FLASK_APP=users_app flask run -p $PORT

# Resturaunts Service  
restaurants: FLASK_APP=restaurants_app flask run -p $PORT

# Carts service
carts: FLASK_APP=carts_app flask run -p $PORT