from flask import Flask, request, make_response, render_template
#from pylab import plot,show
#import matplotlib.pyplot as plt, mpld3
import matplotlib.pyplot as pyplot
import cgi
import cStringIO
from numpy import vstack,array
#from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
import csv
#import pandas as pd
#import pygal
#from pygal.style import LightStyle
app = Flask(__name__)
#app = Flask(__name__, static_url_path = "", static_folder = "static")


@app.route('/')
def hello_world():
	return app.send_static_file('index.html')

@app.route('/plotter', methods=['POST','GET'])
def plotter():
	a= str(request.form['a'])
	b= str(request.form['b'])
	k= str(request.form['k'])
	k= int(k)
	
	data_points=[]

	csv_file = csv.reader(open('earthquakes.csv', "rb"), delimiter=",")

	headers = csv_file.next()
	#print headers

	#print headers.index("Y")	
	a= headers.index(a)
	b= headers.index(b)
	count=0	
	next(csv_file,None)	
	for row in csv_file:
		vector_element=[]
		if row[a] != '' and row[b]!='':
			#print (row[a]), ' ' , (row[b])
			#if float(row[a])>500:
			#	print row[a]
			vector_element.append(float(row[a]))
			vector_element.append(float(row[b]))
			data_points.append(vector_element)
			count=count+1
	print count		
	data_points
			

	data = vstack(data_points)

	#  with K = 4 (4 clusters)
	centroids,_ = kmeans(data,k)
	idx,_ = vq(data,centroids)
	colors=['red','green','blue','orange','black']
	mark=['o']
	
	for i in range(0,k):
		pyplot.plot(data[idx==i,0],data[idx==i,1],color=colors[i],marker=mark[0], ls='none')
	
	#plot(data[idx==0,0],data[idx==0,1],'ob')
	#plot(data[idx==1,0],data[idx==1,1],'or')
	#plot(data[idx==2,0],data[idx==2,1],'sg')
	#plot(data[idx==3,0],data[idx==3,1],'rd') 
	pyplot.plot(centroids[:,0],centroids[:,1],'sm',markersize=8)
	print 'Displaying chart'
	
	# save file on server
	pyplot.savefig('output.png')
	
	#display on browser locally 1
	#mpld3.show()
	
	# display on browser 
	format = "png"
	sio = cStringIO.StringIO()
	pyplot.savefig(sio, format=format)
	
	print "Content-Type: text/html\n"
	return """<html><body>
	...a bunch of text and html here...
	<img src="data:image/png;base64,%s"/>
	...more text and html...
	</body></html>""" % sio.getvalue().encode("base64").strip()
	
	#return app.send_static_file('output.html')
	

@app.route('/scatter', methods=['POST','GET'])
def scatter():
	
	a= str(request.form['a'])
	b= str(request.form['b'])

	csv_file = csv.reader(open('earthquakes.csv', "rb"), delimiter=",")

	headers = csv_file.next()
	a= headers.index(a)
	b= headers.index(b)

	render = pd.read_csv("earthquakes.csv")

	#Scatter Plot
	xy_chart = pygal.XY(stroke=False)
	xy_chart.title = 'Depth versus Magnitude where Earthquake magnitude was between 3.0 & 6.0'
	#next(render,None)
	for index, row in render.iterrows():
		xy_chart.add('', [(row[a], row[b])])
	xy_chart.render_to_file('scatter.svg')
	
	return "Success, check output"
	
	
if __name__ == '__main__':
	app.run(debug=True)

