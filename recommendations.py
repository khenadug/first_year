
# Khena Dungu 2462068D

# read in the information from the book file

def read_file(myfile):
    book_info = []
    with open (myfile) as f:
        for line in f:
            line = line.rstrip()
            book_info.append(line)
    return book_info

# read in the data from the ratings file

def get_ratings(rfile):
    users_rating = {}
    with open (rfile) as f:
        for line in f:
            b = line.rstrip().split()
            try:
                int(b[0])
                users_rating[username] = b
            except ValueError:
                username = line.rstrip()
                users_rating.update({username : []})
                
    return users_rating

#sorting algorithm to get the similairy between the user and other ratings

def sorting_algorithm(name,user,ratings,books):
    similarity = 0
    dict1 = {}
    simdict = {}
    sortedlist  = []

 
    for x in ratings:
#skip the users own ratings         
        if name == x:
            continue
        else:
#calculate the similarity of the user and the other users
            for a in range(len(user[name])):
                similarity += int(user[name][a]) * int(ratings[x][a])
        
        sortedlist.append(similarity)      
        dict1.update({x: similarity})
        similarity = 0

    sortedlist = sorted(sortedlist, reverse=True)
    
#sort the dictionary by highest similarity
    for x in range(len(sortedlist)):
        for y in dict1:
            if dict1[y] == sortedlist[x]:
                simdict.update({y : sortedlist[x]})

  
    return simdict

def get_new_r(name,books,users_rating):
    import random
    new_r = []
#get a random selection of 11 of the books from the books file
    books_to_rate = random.choices(books, k=11)
    print("Ratings: -5 Hated it!, -3 Didn’t like it, 0 Haven’t read it, 1 OK, 3 Liked it!, 5 Really liked it!")
#ask the user to rate the books
    for x in range(11):
            new_r.append(input("What did you think of {book}?".format(book=books_to_rate[x])))
#save their ratings to the main ratings dictionary 
    users_rating.update({name : new_r})

    return users_rating

def book_recs(user,users_rating,simdict,books,numofrecs):
    listB = []
    listZ = []
    listOfBooks = []
    lOfBooks = []
    book_r = {}
#count how many of the books the user hasnt read
    for elt in user:
        for recs in range(len(user[elt])):
            if int(user[elt][recs]) == 0:
                listZ.append(recs)
#check from the similairty dictionary how many high ratings they gave books
    for x in simdict:   
        for i in range(len(users_rating[x])):
            if int(users_rating[x][i]) == 5:
                listB.append(i)
                
            elif int(users_rating[x][i]) == 3:
                listB.append(i)
                
            else:
                continue
#add the book that were rated highly to a list           
        for num in range(len(listZ)):
            if listZ[num] in listB and books[num] not in listOfBooks:
                    listOfBooks.append(books[num])
                    lOfBooks.append(books[num])

        if len(listOfBooks) > numofrecs:
            break
#then add that list to a dictionary with the user who recommended the book as they key and the list of recomendations
        if lOfBooks == []:
            continue
        else:
            book_r.update({x :lOfBooks})
        lOfBooks = []    
        listB = []

        
        
    return book_r

#write all the info to the output file
def output_writing(simdict,books,name,book_r,numofrecs):
    
    with open("output.txt","w") as y:
        y.write("What is your name? {name}\r\n".format(name=name))
        y.write("How many recommendations would you like? {numofrecs}\r\n".format(numofrecs=numofrecs))
        y.write(" \r\n")

        for elt in simdict:
            y.write("{name} has a similarity of {num} with {user}\r\n".format(name=name, num=simdict[elt],user=elt))

        y.write("\r\n")
        y.write("\r\n")

        for user in book_r:
            y.write("User {user} recommends:{books}\r\n".format(user=user,books=book_r[user]))
            

        y.close()
    return simdict


#main program begins here
def main_program():
# set up main variables
    books = read_file("books.txt")
    users_rating = get_ratings("ratings.txt")

#ask the user for their input

    user = input("What is your name?")
#if they are already a user use their ratings
    if user in users_rating:
        name = user
        user = {user : users_rating[user]}
#if theyre new ask them to rate some books
    else:
        name = user
        get_new_r(name,books,users_rating)
        user = {name : users_rating[user]}
        
    try:
#if the user enters a number save it 
        numofrecs = input("How many reccomendations would you like?")
        numofrecs = int(numofrecs)
    except ValueError:
#if they don't just use the deafult number 10
        nextumofrecs = 10
        
#set up the dictionary with the similarities between the user and the ratings 
    simdict = sorting_algorithm(name, user, users_rating, books)

    book_r = book_recs(user,users_rating,simdict,books,numofrecs)
    
#print out reccommendations and user similarities
    output_writing(simdict,books,name,book_r,numofrecs)

    




    
