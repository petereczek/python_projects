from flask import Flask, render_template, send_file
import zipfile
import io
import pathlib

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/contact/')
def contact():
	return render_template('contact.html')

@app.route('/projects/')
def projects():
	return render_template('projects.html')

@app.route('/blocker_readme')
def return_files_blocker_readme():
	return send_file('projects/website_blocker/readme.txt', as_attachment = True, attachment_filename='readme.txt')

@app.route('/blocker_saved')
def return_files_blocker_saved():
	return send_file('projects/website_blocker/saved.txt', as_attachment = True, attachment_filename='saved.txt')

@app.route('/blocker_linux')
def return_files_blocker_linux():
	return send_file('projects/website_blocker/website_blocker.py', as_attachment = True, attachment_filename='website_blocker.py')

@app.route('/blocker_windows')
def return_files_blocker_windows():
	return send_file('projects/website_blocker/website_blocker.pyw', as_attachment = True,  attachment_filename='website_blocker.pyw')

@app.route('/plot/')
def plot():
	from pandas_datareader import data
	import datetime
	from bokeh.plotting import figure, show, output_file
	from bokeh.models.annotations import Title
	from bokeh.embed import components
	from bokeh.resources import CDN

	start = datetime.datetime(2015,11,1)
	end = datetime.datetime(2016,3,10)

	df = data.DataReader(name = 'GOOG', data_source = 'yahoo', start=start, end = end)


	def inc_dec(c,o):
		if c>o:
			value = "Increase"
		elif c<o:
			value = "Decrease"
		else:
			value = "Equal"
		return value
	df["Status"] = [inc_dec(c,o) for c, o in zip(df.Close, df.Open)]

	df["Middle"] = (df.Open+df.Close)/2
	df["Height"] = abs(df.Close - df.Open)

	p = figure(x_axis_type = 'datetime', width = 1000, height = 300, sizing_mode = "scale_width")
	a = Title()
	a.text = "Candlestick Chart"
	p.title = a
	p.grid.grid_line_alpha = 0.3

	#Define rectangles for gray parts of candlestick chart, pass x and y coords of center, as well as length and width
	hours_12 = 12*60*60*1000

	p.segment(df.index, df.High, df.index, df.Low, color = "Black")
	p.rect(df.index[df.Status == 'Increase'],df.Middle[df.Status == "Increase"], hours_12, df.Height[df.Status =="Increase"], fill_color = 'green', line_color = 'black')
	p.rect(df.index[df.Status == 'Decrease'],df.Middle[df.Status == "Decrease"], hours_12, df.Height[df.Status == "Decrease"], fill_color ='red', line_color = 'black')

	script1, div1 = components(p)
	cdn_js = CDN.js_files[0]
	cdn_css = CDN.css_files[0]
	return render_template("plot.html", script1 = script1, div1 = div1, cdn_css = cdn_css, cdn_js= cdn_js)
	output_file('CS.html')
	show(p)

@app.route('/Desktop_DB_App')
def return_files_DB_App():
	#zip all files in oop_Desktop_DB_app recursively, send to requester
	base_path = pathlib.Path('projects/Desktop_DB_App/db_app_oop')
	data = io.BytesIO()
	with zipfile.ZipFile(data, mode='w') as z:
		for f_name in base_path.glob('**/*'):#iterdir():
			z.write(f_name)
	data.seek(0)
	return send_file(data,mimetype='application/zip',as_attachment=True,attachment_filename='Desktop_DB_App.zip')



@app.route('/DB_App_readme')
def return_files_DB_App_readme():
	return send_file('projects/Desktop_DB_App/readme.txt', as_attachment = True, attachment_filename='readme.txt')
	

if __name__ == "__main__":
	app.run(debug = True)
