Le projet est une application sous forme d'API permettant d'accéder à une base de données de cartes Yu-Gi-Oh! 

Après authentification, il est possible à l'utilisateur de créer son propre deck de cartes et de le stocker en base de données.

Commande Docker pour lancer le projet : ./start.sh

Objectifs de sécurité de l'application : Evaluer l'impact d'une vulnérabilité sur C, I, D ou T.

La surface d'attaque représentée par un graph MermaidJS se trouve dans le fichier mermaid_js.jpg à la racine de l'application.

Excel

Concernant la sécurité, l'objectif est de protéger ce projet vulnérable contre au moins 3 des 10 principales attaques web 
définies par l'OWASP :

    -   Le cross-site scripting (XSS) :
    
        Voir commentaire (A-1) dans router.py
        
        """ Mécanisme de sécurité : Validation de données ; Echappement des caractères spéciaux interprétables en Javascript
        et en SQL.
    
        Principe de sécurité : Minimiser la surface d'attaque / Principe de moindre confiance ; Les champs de saisies sont
        une passerelle vers le Javascript exécuté côté client, vers le code backend et vers la base de données. Il faut
        donc restreindre au maximum les possibilités de l'utilisateur.
    
        ----------------------------------------------------------------------------------------------------------------
    
        On peut choisir de retourner des fichiers statiques (HTML, CSS, JS) avec la ligne ci-dessous
    
        return app.send_static_file('html/sign-up.html')
    
        Il est préférable de faire du Server Side Rendering en utilisant le moteur de template Jinja2 intégré à Flask.
        Cette méthode permet un échappement automatique des caractères spéciaux dans les champs de saisies. Il n'est pas
        possible d'inclure de balise <script> ou de quotes pour exécuter du code Javascript ou SQL malicieux. Il est donc
        plus  difficile d'exploiter les failles XXS et les injections SQL"""
        
        ----------------------------------------------------------------------------------------------------------------
        
        Test de faille : tenter d'insérer <script>alert('attention aux failles')</script> dans un champ de saisie
        
        Impact sur le business : dans le cas d'une attaque via une faille XSS, l'attaque peut rediriger l'utilisateur
                                 vers un site frauduleux pour tenter du phising. Il peut également lui voler ses cookies
                                 de session pour accéder à des pages protégées.







    -   L'injection SQL :
    
        Voir commentaires (B-1), (B-2) dans db_driver.py 
                          (A-1) dans router.py
                          
        """ Mécanisme de sécurité : Validation de données ; Echappement des caractères spéciaux interprétables en
        Javascript et en SQL.


        Principe de sécurité : Minimiser la surface d'attaque / Principe de moindre confiance ; Les champs de saisies
        sont une passerelle vers le Javascript exécuté côté client, vers le code backend et vers la base de données.
        Il faut donc restreindre au maximum les possibilités de l'utilisateur.

        ----------------------------------------------------------------------------------------------------------------

        (B-1) : On ne concatène pas directement les paramètres de la méthode dans la requête SQL. Le paramètre provient
        d'un champ de saisie, il peut donc contenir du code malicieux et exécuter des requêtes SQL dangereuses. Il faut
        donc remplacer les paramètres de la requête SQL par un ?, puis ajouter les paramètres dans un tuple à la suite
        de la requête SQL.

        (B-2) : On utilise une requête préparée, qui va compiler la requête avant qu'on ne lui ajoute des paramètres.
        Cela va empêcher toute interprétation d'un code malicieux lors de l'exécution de la requête."""
    
        ----------------------------------------------------------------------------------------------------------------
        
        Test de faille : tenter d'insérer les caractères ';-- dans un champ de saisie
        
        Impact sur le business : dans le cas d'une attaque par injection SQL, les dommages peuvent être très élevés car
                                    l'attaquant à accès à toute la base de données de l'application. Si les données
                                    stockées n'ont pas été cryptées ou hashées au préalable, l'attaquant se retrouve
                                    en possession d'une grande quantité de données sensibles.
    
    
    
    
    
    
    
    -   L'attaque du Man in the Middle :
    
        Mécanisme de sécurité : Chiffrement ; les données qui transistent entre le client et le serveur sont cryptés par
                                le principe du chiffrement asymétrique.
        
        Principe de sécurité : Défense en profondeur.
        
        ----------------------------------------------------------------------------------------------------------------
    
        Dans une communication entre deux correspondants, l'attaque du Man in the Middle a pour but d'imiter l'identité
        d'un des deux correspondants. Il est ensuite en mesure de lire et de modifier les messages sans être découvert.
        
        Une des solutions pour contrer cette faille réside dans le chiffrement des communications via le protocole HTTPS.
        La clé de voûte de ce chiffrement est le certificat SSL/TLS, qui doit être signé par une autorité de certification
        fiable et reconnue. Dans le cadre de ce projet, j'ai généré un certificat auto-signé grâce à l'utilitaire openssl.
        On peut également se procurer un certificat SSL gratuitement grâce au projet LetsEncrypt.
        
        ----------------------------------------------------------------------------------------------------------------
        
        Test de faille : tenter d'intercepter une communication entre deux correspondants grâce à des logiciels sniffers
                         de trames tels Wireshark.
                         
        Impact sur le business : dans le cas d'une attaque du Man in the Middle, l'attaquant peut lire les 
                                 communications, les modifiers, imiter l'identité de quelqu'un. Il y a de grands risques
                                 de vols de données ou d'attaque par ingénieurie sociale.
        
        
        

    
    

    -   L'accès directe à des objets non sécurisés (IDOR)
    
        Voir commentaire (C-1)
        
        Mécanisme de sécurité : Gestion de sessions ; le routeur va vérifier la présence d'un cookie de session dans 
                                chaque requête entrante, puis redirigé la requête vers la page adaptée.
                                
        Principe de sécurité : Principe de moindre confiance.
        
        ----------------------------------------------------------------------------------------------------------------
        
        (C-1) : Pour empêcher les attaques par référence direct d'objets non sécurisées (dites IDOR), on va stocker un
        cookie de session dans le navigateur de l'utilisateur lorsque celui-ci va se connecter ou se créer un compte.
        Tous les requêtes entrantes passent par le routeur qui va vérifier la présence de ce cookie de session pour
        accéder à certaines pages à accès réservé, comme par exemple le dashboard personnel d'un utilisateur. Dans le 
        cas où un utilisateur tente une attaque IDOR en renseignant directement l'URL qui est censé ammené à une page
        à accès réservé, celui-ci se vera rediriger vers la page d'index.
        
        ----------------------------------------------------------------------------------------------------------------
        
        Test de faille : tenter d'accèder à une URL à accès restreint comme https://127.0.0.1:5000/user-dashboard
        
        Impact sur le business : dans le cas d'une attaque IDOR, l'attaquant peut avoir accès à des pages à accès 
                                 réservés et donc potentiellement des informations sensibles sur l'utilisateur.
    
