D = {
	'-' : 'img/empty.gif',
	'B' : 'img/blueend.gif',
	'O' : 'img/orangeend.gif',
	'R' : 'img/redend.gif',
	'G' : 'img/greenend.gif',
	'r' : 'img/lrred.gif',
	'g' : 'img/lrgreen.gif',
	'b' : 'img/lrblue.gif',
	'z' : 'img/tbblue.gif',
	'x' : 'img/tlblue.gif',
	'c' : 'img/trblue.gif',
	'v' : 'img/lbblue.gif',
	'n' : 'img/rbblue.gif',
	'o' : 'img/lrorange.gif',
	'9' : 'img/cirno.gif',
	'Z' : 'img/tborange.gif',
	'X' : 'img/tlorange.gif',
	'C' : 'img/trorange.gif',
	'V' : 'img/lborange.gif',
	'N' : 'img/rborange.gif',
	'q' : 'img/tbgreen.gif',
	'w' : 'img/tlgreen.gif',
	'e' : 'img/trgreen.gif',
	't' : 'img/lbgreen.gif',
	'y' : 'img/rbgreen.gif',
	'Q' : 'img/tbred.gif',
	'W' : 'img/tlred.gif',
	'E' : 'img/trred.gif',
	'T' : 'img/lbred.gif',
	'Y' : 'img/rbred.gif',


}
#lee un archivo con los parametros de la matriz
def FlowRead(MAP_FILE):
	MAP_FILE = open(MAP_FILE,"r")
	MAP_MATRIX = [j.strip() for j in MAP_FILE]
	MAP_FILE.close()
	return MAP_MATRIX
	
#muestra la matriz flow free (una vez aplicado flowread)
def FlowPrint(MAP_MATRIX):
	import turtle
	#recibe una matriz de FlowFree y la muestra
	FlowWindow = turtle.Screen()
	FlowWindow.setup(500,500)
	FlowWindow.title("FlowFree")
	FlowWindow.tracer(0)
	for k in D.keys():
   		FlowWindow.addshape(D[k])
	cell = turtle.Turtle()
	cell.pu()
	cell.ht()
	y = 200
	for CELL in MAP_MATRIX:
		cell.sety(y)
		x = -200
		for TYPE in CELL:
			cell.setx(x)
			try:
				cell.shape(D[TYPE])
			except:
				cell.shape(D['9'])
			cell.stamp()
			x += 100
		y-=100 
	FlowWindow.exitonclick()
	
