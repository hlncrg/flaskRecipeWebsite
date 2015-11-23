from flask import render_template, request, send_file, Flask
import pymysql as mdb

app = Flask(__name__)
app.debug = True

#db = mdb.connect(user="root", host="localhost", db="world", charset='utf8')
con = mdb.connect('localhost', 'root', 'njnICfOw', 'recipesDB') #host, user, password, #database

@app.route('/')
@app.route('/index')
@app.route('/catagory/<int:catagoryId>')
def index(catagoryId=None):
    catagoryIdToNames={0:'Cookies',
			1:'Pies',
                        2:'Cakes',
                        3:'Pudding and Fudge',
                        4:'Bars and Brownies',
                        5:'Lasagna',
                        6:'Crips/Cobbler/Dumplings',}
    with con:
        cur = con.cursor()
	if catagoryId>=0 and catagoryId<=6:
	        cur.execute("SELECT recipeId,recipeName FROM Recipes WHERE catagory="+str(catagoryId))
		catagoryName=catagoryIdToNames[catagoryId]
	else:
		cur.execute("SELECT recipeId,recipeName FROM Recipes")
		catagoryName='All'
	
	


        query_results = cur.fetchall()
    recipeIds=[]
    recipeNames=[]
    for result in query_results:
        recipeIds.append(result[0])
        recipeNames.append(result[1])
    impWords=[]
    modWords=[]
    #for recipeId in recipeIds:
    #    with con:
    #        cur = con.cursor()
    #        cur.execute("SELECT words,neg,pos,mov FROM ImpWords"+str(recipeId))
    #        query_results = cur.fetchall()  
    #        for result in query_results:
    #            impWords.append((recipeId,result))
    #for recipeId in recipeIds:
    #    with con:
    #        cur = con.cursor()
    #        cur.execute("SELECT words,modWord,inc_addWord,incWord,decWord,addWord,subWord FROM modWords"+str(recipeId))
    #        query_results = cur.fetchall()
    #        for result in query_results:
    #            modWords.append((recipeId,result))
    return render_template("index.html",recipeIds=recipeIds,recipeNames=recipeNames,catagoryName=catagoryName
    #        impWords=impWords,modWords=modWords
        )


@app.route('/about')
def about():

	return render_template("about.html")


@app.route('/recipe/<int:recipeId>')
def recipe(recipeId=None):
    print 'here'
    recipeId=str(recipeId)
    foodwordResults=[]
    suggestions=[]
    additions=[]
    ingredients=[]
    impWords=[]
    suggestionsSentences=[]
    additionsSentences=[]
    actions=['reviews are mixed for','increase','decrease','add']
    with con:
        cur = con.cursor()
	print ("SELECT  words,mixWord,incWord,decWord,addWord,ModWords"+recipeId+".numTot,modFoodEx,inc_addFoodEx,incFoodEx,decFoodEx,subFoodEx FROM ModWords"+recipeId+
                    " INNER JOIN RecipesCount"+recipeId+
                    " ON ModWords"+recipeId+".words=RecipesCount"+recipeId+".foodword")
        cur.execute("SELECT  words,mixWord,incWord,decWord,addWord,ModWords"+recipeId+".numTot,modFoodEx,inc_addFoodEx,incFoodEx,decFoodEx,subFoodEx FROM ModWords"+recipeId+
                    " INNER JOIN RecipesCount"+recipeId+
                    " ON ModWords"+recipeId+".words=RecipesCount"+recipeId+".foodword")
        query_results = cur.fetchall()
        for results in query_results:
            foodwordResults.append(results)
        for word in foodwordResults:
            m = max(word[1:5])
            if m>.9 and word[5]>15:
                index=[i for i, j in enumerate(word) if j == m][0]-1
                if index!=3 and len(suggestions)<=5:
                    suggestions.append(actions[[i for i, j in enumerate(word) if j == m][0]-1]+" "+word[0])
		    if index==0:
			wordstoadd=[word[6],'','','','']
			if word[7] not in wordstoadd:
				wordstoadd[1]=word[7]
			if word[8] not in wordstoadd:
				wordstoadd[2]=word[8]
			if word[9] not in wordstoadd:
                                wordstoadd[3]=word[9]
                        if word[10] not in wordstoadd:
                                wordstoadd[4]=word[10]
                    	suggestionsSentences.append(wordstoadd)
                    if index==1:
			if word[7]!=word[8]:
                        	suggestionsSentences.append(['',word[7],word[8],'',''])
			else:
				suggestionsSentences.append(['',word[7],'','',''])
                    if index==2:
			if word[9]!=word[10]:
                        	suggestionsSentences.append(['','','',word[9],word[10]])
			else:
				suggestionsSentences.append(['','','',word[9],''])
                elif len(additions)<=5: 
                    additions.append(word[0])
		    if word[7]==' ' and word[8]==' ' and word[9]==' ' and word[10]==' ':
			additionsSentences.append([word[6],word[7],word[8],word[9],word[10]])
		    else:
                    	additionsSentences.append(['',word[7],word[8],word[9],word[10]])

    with con:
        cur = con.cursor()
        cur.execute("SELECT  recipeName FROM Recipes WHERE recipeId="+recipeId)
        query_results = cur.fetchall()
        for results in query_results:
            name=results[0]
    with con:
        cur = con.cursor()
        cur.execute("SELECT  ingredients FROM Ingredients"+recipeId)
        query_results = cur.fetchall()
        for results in query_results:
            ingredients.append(results[0])
    with con:
        cur = con.cursor()
	cur.execute("SELECT words,negEx,posEx FROM ImpWords WHERE recipeId="+str(recipeId))
	query_results = cur.fetchall()
        for result in query_results:
            impWords.append((result))
    return render_template("individual.html",recipeId=recipeId,
            suggestionsSentences=suggestionsSentences,additionsSentences=additionsSentences,
            additions=additions,impWords=impWords,ingredients=ingredients,name=name,suggestions=suggestions)




#######Picture Function#########
@app.route('/images/<string:nameID>')
def photo(nameID=None):
    return send_file('images/'+nameID,mimetype='image/gif')

if __name__ == "__main__":
	#app.run(host='0.0.0.0', port=5000)
	app.run(host='0.0.0.0', port=80)
