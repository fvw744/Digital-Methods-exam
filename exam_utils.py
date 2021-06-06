def extract_dict(string,out):
    """Helper function to extract from list or dict from string if string exists 
    else the function returns out (either list or dict) (Thanks, Tweepy...)"""
    import ast
    try:
        out=ast.literal_eval(string)
    except:
        out=out
    return out

def extract_from_entities(tweet,ent_key,tag_key):
    """Helper function to extract information from tweet_entities.
    tweet_entities is a dict-of-dicts containing all information on 
    twitter entities from a given tweet.
    ent_key: key used to access the dictionary of interest e.g. "hastags"
    tag_key: key used to access value of interest e.g. "text"
    Why, Tweepy? WHY?!"""
    try:
        out=[tag[tag_key] for tag in tweet[ent_key] if tweet[ent_key]!=ent_key]
    except:
        out=list()
    return out

def remove_stopwords(sentence):
    """
    Removes stopwords imported from spacy and returns filtered string
    """  
    tokens = sentence.split(" ")
    tokens_filtered= [word for word in tokens if not word in all_stopwords]
    return (" ").join(tokens_filtered)

def preproccessor(string, verb_noun_only=False):
    """
    Helper function for lemmatizer().
    Preprocesses the string by:
    1) lowercasing string
    2) removing urls
    3) remove mentions, hashtags, and RT
    4) remove non-alphanumerical values
    5) remove multiple whitespaces
    6) remove trailing whitespaces
    7) remove stop words
    """  
    # Lowercase
    string=string.lower()
    
    # Remove url
    string=re.sub(
        r"(https|http?):\/\/(\w|\.|\/|\?|\=|\&|\%)*\b",
        "", 
        string)
    
    # Remove weird remaining http
    string = re.sub(r'https?', '', string)
    
    # Remove mentions, hashtags, and RT
    string=re.sub("@\w+|#\w+|^rt","", string)
    
    # Remove non-alphanumerical values
    string=re.sub(r"\W"," ", string)
 
    # Remove more than one whitespace
    string=re.sub(r"\s{2,}", " ", string)
    
    # Remove trailing whitespaces
    string=string.strip()
    
    # Remove stopwords
    string=remove_stopwords(string)
    
    # Create and return doc object
    return nlp(string)  
   
def lemmatizer(string):
    """
    Lemmatize the preprocessed string using spacy's lemmatizer
    """
    doc=preproccessor(string)
    
    lemma=" ".join(
        [token.lemma_ for token in doc if len(str(token.lemma_))]
    )
    return lemma

def lemmatizer_reduced(string):
    """
    Reduce the allready lemmatized string by only including proper nouns, nouns, and verbs
    """
    doc=nlp(string)
    verb_and_noun=" ".join(
    [token.lemma_ for token in doc if token.pos_ in ["PROPN","NOUN","VERB"]]
    )
    return verb_and_noun

def timeParser(string):
    """
    Helper function to extract time in format date month year. 
    """
    import datetime
    from dateutil.parser import parse
    dt=parse(string)
    dt=dt.strftime("%d-%m-%Y")
    return datetime.datetime.strptime(dt,"%d-%m-%Y")

