# stopwords.py

STOPWORDS = {
    # artigos
    "a", "o", "os", "as", "um", "uma", "uns", "umas",

    # preposições
    "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas",
    "por", "para", "com", "sem", "sobre", "entre",

    # conjunções
    "e", "ou", "mas", "porque", "pois", "que", "se", "ao",

    # pronomes comuns
    "eu", "tu", "ele", "ela", "eles", "elas",
    "me", "te", "se", "nos", "vos",
    "meu", "minha", "meus", "minhas",
    "seu", "sua", "seus", "suas",
    "este", "esta", "estes", "estas",
    "esse", "essa", "esses", "essas",
    "aquele", "aquela", "aqueles", "aquelas",

    # palavras funcionais comuns em texto clínico
    "há", "tem", "têm", "foi", "são", "ser", "estar",
    "está", "estão", "estava", "estavam","ao", "desde", "há", 
    "até", "sobre", "entre", "desde",

    # artigos/ruído comum em frases de sintomas
     "paciente", "relata", "apresenta"
}