import sqlite3
import logging
import sys
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('techtrends')

# Initialize global variables
db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        logger.error('Article with id %d not found!', post_id)
        return render_template('404.html'), 404
    else:
        logger.info('Article "%s" retrieved!', post['title'])
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logger.info('About page retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            logger.info('Article "%s" created!', title)
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the healthz endpoint
@app.route('/healthz')
def healthz():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    return response

# Define the metrics endpoint
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
    connection.close()
    post_count = posts[0]

    response = app.response_class(
        response=json.dumps({
            "post_count": post_count,
            "db_connection_count": db_connection_count
        }),
        status=200,
        mimetype='application/json'
    )
    return response

# start the application on port 7111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='7111')
