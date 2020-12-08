import random

#TODO Make dictionnary
pipod=[]
pipod.append(["Face à","Relativement à","Pour optimiser","Pour accentuer","Afin de maîtriser","Au moyen d#","Depuis l'émergence d#","Pour challenger", "Pour défier","Pour résoudre","En termes de redynamisation d#","Concernant l'implémentation d#","À travers","En s'orientant vers","En termes de process, concernant","En rebondissant sur","Pour intégrer","Une fois internalisée","Pour externaliser","Dans la lignée d#","En synergie avec","Là où les benchmarks désignent","Au cœur d#","En auditant","Une fois evaluée","Partout où domine","Pour réagir à","En jouant","Parallèlement à","Malgré","En réponse à","En réaction à","Répliquant à","En phase de montée en charge d#", "En réponse à","En phase de montée en charge d#", "Grâce à", "Perpendiculairement à", "Indépendamment d#", "Corrélativement à", "Tangentiellement à", "Concomitamment à","Par l'implémentation d#"])
pipod.append(["la problématique","l'opportunité","la mondialisation","une globalisation","la bulle","la culture","la synergie","l'efficience","la compétitivité","une dynamique","une flexibilité","la revalorisation","la crise","la stagflation","la convergence","une réactivité","une forte croissance","la gouvernance","la prestation","l'offre","l'expertise","une forte suppléance","une proposition de valeur","une supply chain","la démarche", "une plate-forme", "une approche", "la mutation","l'adaptabilité", "la pluralité", "une solution", "la multiplicité","la transversalité","la mutualisation"])
pipod.append(["opérationnelle,","quantitative,","des expertises,","porteuse,","autoporteuse,","collaborative,","accélérationnelle,","durable,","conjoncturelle,","institutionnelle,","managériale,","multi-directionnelle,","communicationnelle,","organisationnelle,","entrepreneuriale,","motivationnelle,","soutenable,","qualitative,","stratégique,","interne / externe,","online / offline,","situationnelle,","référentielle,","institutionnelle,","globalisante,","solutionnelle,","opérationnelle,","compétitionnelle,","gagnant-gagnant,","interventionnelle,","sectorielle,","transversale,","des prestations,","ambitionnelle,","des sous-traitances,", "corporate,", "asymétrique,", "budget", "référentielle"])
pipod.append(["les cadres doivent ","les personnels concernés doivent ","les personnels concernés doivent ","les N+1 doivent ","le challenge consiste à","le défi est d#","il faut","on doit","il faut","on doit","il faut","on doit","il faut","on doit","chacun doit","les fournisseurs vont","les managers décident d#","les acteurs du secteur vont","les responsables peuvent","la conjecture peut","il est impératif d#","un meilleur relationnel permet d#","une ambition s'impose :","mieux vaut","le marché exige d#","le marché impose d#","il s'agit d#","voici notre ambition :","une réaction s'impose :","voici notre conviction :","les bonnes pratiques consistent à","chaque entité peut","les décideurs doivent","il est requis d#","les sociétés s'engagent à","les décisionnaires veulent","les experts doivent","la conjecture pousse les analystes à","les structures vont","il faut un signal fort :","la réponse est simple :","il faut créer des occasions :","la réponse est simple :","l'objectif est d#","l'objectif est évident :","l'ambition est claire :","chaque entité doit","une seule solution :","il y a nécessité d#","il est porteur d#","il faut rapidement","il faut muscler son jeu : ","la réponse client permet d#","la connaissance des paramètres permet d#", "les éléments moteurs vont"])
pipod.append(["challenger","optimiser","faire interagir","capitaliser sur","prendre en considération","anticiper ","intervenir dans","imaginer","solutionner","piloter","dématerialiser","délocaliser","coacher","investir sur","valoriser","flexibiliser","externaliser","auditer","sous-traiter","revaloriser","habiliter","requalifier","revitaliser","solutionner","démarcher","budgetiser","performer","incentiver","monitorer","segmenter","désenclaver",  "décloisonner", "déployer", "réinventer", "flexibiliser", "optimiser", "piloter","révolutionner", "gagner", "réussir", "connecter", "faire converger", "planifier", "innover sur", "monétiser", "concrétiser","impacter", "transformer", "prioriser", "chiffrer", "initiativer", "budgetiser", "rénover", "dominer"])
pipod.append(["les deadlines","les solutions","les issues","l'axes mobilisateurs","les problématiques","les cultures","les alternatives","l'interactions","les issues","les expertises","le focus","les démarches","les alternatives","les thématiques","les atouts","les ressources","les applications","les applicatifs","les architectures","les prestations","les process","les performances","les bénéfices","les facteurs","les paramètres","les capitaux","les sourcing","les émergences","les kick-off","les recapitalisations","les produits","les frameworks","les focus", "les challenges","les décisionnels","les ouvertures","les fonctionnels","les opportunités","les potentiels","les territoires","les leaderships","les applicatifs","les prestations","les plans sociaux","les wordings","les harcèlements","les monitorings","les montées en puissance","les montées en régime","les facteurs","les harcèlements","les référents", "les éléments", "les nécessités", "les partenariats", "les retours d'expérience", "les dispositifs", "les potentiels", "les intervenants","les directives","les perspectives","les contenus","les implications","les kilo-instructions","les mind mappings", "les thématiques","les workshops","les cœurs de mission", "les managements", "les orientations", "les cibles", "les synergies"])
pipod.append(["métier","prospect","customer","back-office","client","envisageables","à l'international","secteur","client","vente","projet","partenaires","durables","à forte valeur ajoutée","soutenables","chiffrables","évaluables","force de vente","corporate","fournisseurs","bénéfices","convivialité","compétitivité","investissement","achat","performance","à forte valeur ajoutée","dès l'horizon 2020","à fort rendement","qualité", "logistiques", "développement", "risque", "terrain", "mobilité", "praticables", "infrastructures", "organisation", "projet", "recevables", "investissement", "conseil", "conseil", "sources", "imputables", "intermédiaires", "leadership","pragmatiques","framework","coordination","d'excellence","stratégie","de confiance", "crédibilité", "compétitivité", "méthodologie", "mobilité", "efficacité", "scalable","utilisateur"])

def harmonize(pipo):
    harmonic = 'aeiouyhéèà'
    while pipo.find("#") != -1:
        idx = pipo.find("#");
        if idx+2 < len(pipo):
            char = pipo[idx+2]
            pipobegin = pipo[:idx]
            pipoend   = pipo[idx+1:]
            if char in harmonic:
                pipo = pipobegin + "'" +pipoend
            else :
                pipo = pipobegin + "e" +pipoend
    return pipo

def play_pipo():
    pipo = ""
    for i in range(7):
        pipo=pipo+" "+random.choice(pipod[i])
    pipo = harmonize(pipo).strip()
    return (pipo)

async def cmd(message):
    msg = play_pipo()
    await message.channel.send(msg)
