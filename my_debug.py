

def print_to_newline(comment,to_print):
    print('\n' + comment + ':\n', to_print)

def print_along(comment,to_print):
    print('\n' + comment,': ', to_print)

def correct_faces(faces):
    faces_ =[]
    for face in faces:
        if face != []:
            faces_.append(face)
    if faces_ == []:
       raise Exception("Sorry, no face is found !")
    

