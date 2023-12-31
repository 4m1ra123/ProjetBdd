from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import make_password,check_password
#Utile pour les requetes SQL
from django.db import connection
#Pour recuperer sous format JSON
from django.http import JsonResponse

from datetime import datetime


#Connexion Client
def login(request):
        if request.method=='POST':
            
            email=request.POST['email']
            password=request.POST['password']

            with connection.cursor() as cursor:
                try:
                    cursor.execute("Select password from client Where email=%s",[email])
                    #recupere le tuple
                    client_pass_db= cursor.fetchone()
                    pass_db=client_pass_db[0]
                    if(pass_db):
                        if (check_password(password,pass_db)):
                            return render(request,'accueil.html',{"exist":"yesss"})
                        else:
                            return render(request,'login.html',{'erreur':'Mot de passe incorrect'})
                except:
                    return render(request,'login.html',{'inexistant':'Cliquez sur signup pour vous inscrire'})

    
        context={}
        return render (request,'login.html',context)


#Inscription Client
def signup(request):
    #Si lutilisateur clique sur signup
    if  request.method=='POST' :
            #Mettre le first name qu'on a nomme 'prenom'(html) dans la var fname
            fname= request.POST['prenom']
            lname=request.POST['nom']
            email=request.POST['email']
            phone=request.POST['tel']
            password=request.POST['pass']
            confirm=request.POST['confirm']

            with connection.cursor() as cursor:
                 cursor.execute("Select 1 from client Where email=%s",[email])
                 cli= cursor.fetchone()
                 if (cli):
                      return render(request,'signup.html',{"exist":"Bah t'existes deja toi "})
                 


            if confirm!=password:
                context={'mdp': "Les mots de passe ne sont pas similaires"}
                return render(request,'signup.html',context)

            else:
            
                # Creation d'un objet curseur qui me permettra d'executer des requetes SQL
                with connection.cursor() as cursor:
                #Stocker la requete SQL dans une var

                #&S est juste un parametre de substiution
                    sql_query = """
                    INSERT INTO client (Password_client, N_tel, Email_client, fname_client,lname_client)
                    VALUES (%s, %s, %s, %s, %s)"""
                    # Executer la requete
                    cursor.execute(sql_query, [make_password(password), phone, email, lname,fname])
                    connection.commit()
    #make_password pour stocker le mdp "hache" dans la bdd
                    context={'Created': True}
                    return render (request,'login.html',context)
    
    #Utilisateur vient de naviguer vers signup
    return render(request,'signup.html')


#Retourner la page du profil
def utilisateur(request):
    context={'':''}

    return render(request,"utilisateur.html",context)


 #Recuperer tous les types d'evenements sous format JSON a partir de la BDD de la table Team
def get_type_event(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Team")  
        result = cursor.fetchall()

    # Format the result into a list of dictionaries
    data = [{'type_team': row[0], 'nbr_employee': row[1]} for row in result]

    return JsonResponse({'data': data})



def get_json_team(request,*args,**kwargs):
    #Recuperer a partir de l'HTML l'element avec l'ID "typeEvent"
    selected_type= kwargs.get('typeEvent')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Events  WHERE type_team=%s GROUP BY Events.date_event ORDER BY date_event",[selected_type]) 

        #Recupere toutes les lignes retournees par la requete SQL et les met dans la variable result 
        result = cursor.fetchall()

    #Creer un dictionnaire des instances de la table Creneau pour pouvoir les manipuler dans le JS
    data = [{'id_creneau': row[0], 'date_a': row[1],'heure_a':row[2],'taken':row[3],'type_team':row[4]} for row in result]

    print(data)
    return JsonResponse({'data':data})



def get_json_hour(request,*args,**kwargs):
    #Recuperer a partir de l'HTML l'element avec l'ID "typeEvent"
    selected_type= kwargs.get('typeEvent')
    selected_date_str= kwargs.get('appDate')
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    print(selected_type)
    print(selected_date)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Creneau  WHERE type_team=%s AND Creneau.date_a=%s ORDER BY Creneau.heure_a",[selected_type,selected_date]) 

        #Recupere toutes les lignes retournees par la requete SQL et les met dans la variable result 
        result = cursor.fetchall()

    #Creer un dictionnaire des instances de la table Creneau pour pouvoir les manipuler dans le JS
    data = [{'id_creneau': row[0], 'date_a': row[1],'heure_a':row[2],'taken':row[3],'type_team':row[4]} for row in result]

    
    return JsonResponse({'data':data})




def get_available_hours_for_date(request, *args, **kwargs):
    try:
        selected_type = kwargs.get('typeEvent')
        selected_date_str = kwargs.get('appDate')
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except Exception as e:
        print(f"Error parsing date: {e}")
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Obtenez les heures déjà présentes dans la table Creneau pour la date spécifiée
    with connection.cursor() as cursor:
        cursor.execute("SELECT Creneau.heure_a FROM Creneau WHERE type_team=%s AND Creneau.date_a=%s ORDER BY Creneau.heure_a", [selected_type, selected_date])

        # Recupere toutes les lignes retournees par la requete SQL et les met dans la variable result
        result = cursor.fetchall()

    # Creer un dictionnaire des instances de la table Creneau pour pouvoir les manipuler dans le JS
    dataa = [{'heure_a': row[0].strftime('%H:%M')} for row in result]

    # Obtenez toutes les heures possibles
    all_hours = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00"]

    # Obtenez les heures disponibles (qui ne sont pas déjà réservées)
    available_hours = [hour for hour in all_hours if hour not in [h['heure_a'] for h in dataa]]

    data = [{'value': hour, 'label': hour} for hour in available_hours]

    # Formattez la réponse JSON pour inclure les heures disponibles
   
    return JsonResponse({'data':data})





def create_appointment(request):
    if request.method=='POST':
        nameEvent=request.POST.get('nom')
        typeEvent=request.POST.get('type')
        dateEvent=request.POST.get('datee')
        descriptionEvent=request.POST.get('description')
        appDate=request.POST.get('datea')
        appTime=request.POST.get('heurea')
        
        

    pass