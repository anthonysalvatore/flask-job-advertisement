from flask import Flask, render_template, request, redirect
from utils import gen_docVecs
from bs4 import BeautifulSoup
import gensim.downloader as api
import pickle

from utils import gen_docVecs

# load in gogglenews300 model
preTW2v_wv = api.load('word2vec-google-news-300')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/accounting')
def accounting():
    return render_template('accounting.html')

@app.route('/engineering')
def engineering():
    return render_template('engineering.html')

@app.route('/healthcare')
def healthcare():
    return render_template('healthcare.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/<folder>/<filename>')
def job(folder, filename):
    return render_template('/' + folder + '/' + filename + '.html')

@app.route('/add_job', methods = ['GET', 'POST'])
def add_job():
    if request.method == 'POST':

            # Read the .txt file
            f_title = request.form['title']
            f_content = request.form['description']

            # Classify the content
            if request.form['button'] == 'Classify':

                # Tokenize the content of the .txt file so as to input to the saved model - can do more complicated things here but as an example in the exercise, we just stop here
                tokenized_data = f_content.split(' ')

                # Generate vector representation of the tokenized data
                preTW2v_dvs = gen_docVecs(preTW2v_wv, [tokenized_data])

                # Load the LR model
                pkl_filename = "preTW2v_LR.pkl"
                with open(pkl_filename, 'rb') as file:
                    model = pickle.load(file)

                # Predict the label of tokenized_data
                y_pred = model.predict(preTW2v_dvs)
                y_pred = y_pred[0]

                target_dict = {'0':'accounting', '1':'engineering', '2':'healthcare', '3':'sales'}
                y_pred = target_dict[y_pred]

                return render_template('add_job.html', prediction=y_pred, title=f_title, description=f_content)

            elif request.form['button'] == 'Save':

                # First check if the recommended category is empty
                cat_recommend = request.form['category']
                cat_recommend = cat_recommend.lower()
                if cat_recommend == '':
                    return render_template('add_job.html', prediction=cat_recommend,
                                        title=f_title, description=f_content,
                                        category_flag='Recommended category must not be empty.')

                elif cat_recommend not in ['accounting', 'engineering', 'healthcare', 'sales', 'finance', 'nursing']:
                    return render_template('add_job.html', prediction=cat_recommend,
                                        title=f_title, description=f_content,
                                        category_flag='Recommended category must belong to: accounting, finances, engineering, healthcare, nursing or sales.')

                else:
                    if cat_recommend == 'finance':
                        cat_recommend = 'accounting'
                    elif cat_recommend == 'nursing':
                        cat_recommend == 'healthcare'

                    # First read the html template
                    soup = BeautifulSoup(open('templates/job_template.html'), 'html.parser')
                    
                    # Then adding the title and the content to the template
                    # First, add the title
                    div_page_title = soup.find('div', { 'class' : 'title' })
                    title = soup.new_tag('h1', id='data-title')
                    title.append(f_title)
                    div_page_title.append(title)

                    # Second, add the content
                    div_page_content = soup.find('div', { 'class' : 'data-job' })
                    content = soup.new_tag('p')
                    content.append(f_content)
                    div_page_content.append(content)

                    # Finally write to a new html file
                    filename_list = f_title.split()
                    filename = '_'.join(filename_list)
                    filename =  cat_recommend + '/' + filename + ".html"
                    with open("templates/" + filename, "w", encoding='utf-8') as file:
                        print(filename)
                        file.write(str(soup))

                    # Clear the add-new-entry form and ask if user wants to continue to add new entry
                    return redirect('/' + filename.replace('.html', ''))

    else:
        return render_template('add_job.html')

# REFERENCES:
# M. Li, RMIT, 'Advanced Programming for Data Science', 2022. [Online]. Available: https://www.rmit.edu.au/. [Accessed 19 October 2022].