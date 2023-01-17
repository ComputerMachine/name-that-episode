from pvleopard import create
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


leopard = create(access_key="nk9fLX10chKKm7GoLD5LXM9C/R+Wluajw4p7mgmSA3gCEL11u6DVVA==")

def is_guessable(text):
    """Return a boolean whether the text provides at the very least some information to make it guessable."""
    data = pos_tag(word_tokenize(text))
    # jj - adjectives, nn - nouns
    adjectives = 0
    nouns = 0

    for word in data:
        if word[1] == "JJ":
            adjectives += 1
        elif word[1] == "NN":
            nouns += 1

    # Arbitrarly declare that the presence of 5 adjectives and nouns combined is a good enough sample to be guessed without going ham into speech processing
    if adjectives + nouns >= 5:
        #print ("Provided sample has potential for being guessed... Continuing...")
        return True
    else:
        #print ("Provided sample is unlikely to be guessed.")
        return False