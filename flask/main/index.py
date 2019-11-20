
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)



#route to the main page
@app.route('/') 
def index():
    return render_template('index.html')

#route to the page to select which model
@app.route('/model')
def selectModel():
    return '<h1>hey1</h1>'

#route to the input page
@app.route('/input')
def inputMessage():
    return render_template('input.html')

#route to the results page
@app.route('/results')
def messageResults():
    return '<h1>hey3</h1>'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

#allows the program to execute from terminal
if __name__ == '__main__':
    #allows for dynamic updating, makes debugging faster 
    app.run(debug=True)

