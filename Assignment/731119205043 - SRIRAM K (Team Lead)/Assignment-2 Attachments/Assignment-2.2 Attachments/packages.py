from flask import Flask
from emoji import emojize
import matplotlib.pyplot as plt
import numpy as np
from translate import Translator
from googlesearch import search

app=Flask(__name__)

@app.route('/')
def login():
    emojione=("Thumbs up emoji using the pakage emoji:"+emojize(":thumbs_up:"))
    
    x = [1,2,3] 
    y = [2,4,1] 
    plt.plot(x, y) 
    plt.xlabel('x - axis') 
    plt.ylabel('y - axis') 
    plt.title('Using Matplotlib')
    plt.show()
    a = np.array([0, np.pi/2, np.pi])
    
    translator= Translator(to_lang="ta")
    translation = ("English to Tamil translation using the package translate:"+translator.translate("How are you?"))
    
    query = "IBM Cloud"
    tmp=search(query, tld="co.in", num=10, stop=10, pause=2)
    res=[]
    for i in tmp:
        res.append(i+"\n")
        
    return ("<center>"+"<h1>"+emojione+"</br></br></br>"+translation+"</br></br></br>"+str(np.sin(a))+"</h1></br></br></br>"+str(res)+"</center>")

if __name__ == '__main__':
	app.run('127.0.0.1',3898,debug=True)
