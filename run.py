#This is an Index file 
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True,port=3000)
