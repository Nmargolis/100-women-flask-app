import itertools
import spacy
import textacy
nlp = spacy.load('en')

from empath import Empath
lexicon = Empath()


### helper functions to convert text into the right formats
def to_spacy_doc(raw_doc):
    '''Converts a raw string into a spaCy document'''
    return nlp(raw_doc)

def to_textacy_doc(raw_doc):
    '''Converts a raw string into a spaCy doc, then a textacy doc'''
    if isinstance(to_spacy_doc("test"), spacy.tokens.doc.Doc):
        return textacy.Doc(raw_doc)
    else:
        return textacy.Doc(nlp(raw_doc))



### helper functions to extract useful information
def get_words(doc):
    '''Gets the word tokens for a textacy document, excluding stopwords and punc'''
    if type(doc) == str:
        doc = to_textacy_doc(doc)
    return list(textacy.extract.words(doc))


def get_content_words(doc):
    if not isinstance(doc, textacy.doc.Doc):
        doc = to_textacy_doc(doc)
    return list(textacy.extract.words(doc, filter_stops=True, filter_punct=True, filter_nums=False, include_pos=None, exclude_pos=None, min_freq=1))

def get_named_entities(doc):
    if not isinstance(doc, textacy.doc.Doc):
        doc = to_textacy_doc(doc)
    nes = textacy.extract.named_entities(doc)
    return [ne for ne in nes]

def get_sentences(doc):
    '''Returns a list of spacy spans.'''
    if not isinstance(doc, textacy.doc.Doc):
        doc = to_textacy_doc(doc)
    return list(doc.sents)

def get_semantic_key_terms(doc, top_n_terms=10, filtered=True):
    '''Gets key terms from semantic network. '''
    if not isinstance(doc, textacy.doc.Doc):
        doc = to_textacy_doc(doc)
    term_prob_pairs = textacy.keyterms.key_terms_from_semantic_network(doc)
    max_keyterm_weight = term_prob_pairs[0][1]

    # keep keyterms if they're at least half as important as the most important keyterm
    # term[0] is the word, term[1] is its keyterm-ness.
    if filtered:
        terms = [[term[0], term[1]] for term in term_prob_pairs if term[1] >= 0.5*(max_keyterm_weight)]
    else:
        terms = term_prob_pairs

    return [term[0] for term in terms[:top_n_terms]]

def extract_pos_tagged_sents_from_corpus(textacy_corpus):
    '''Returns a list of documents, each composed of list of sentences.
    Sentences are lists of tuples of the form (token, POS)'''
    return [doc.pos_tagged_text for doc in textacy_corpus]


def extract_verbs(doc):
    '''Returns a list of strings that are verb-tagged tokens.'''
    if not isinstance(doc, textacy.doc.Doc):
        doc = to_textacy_doc(doc)
    all_token_pos_pairs = itertools.chain(*doc.pos_tagged_text) #flatten list
    verbs = [token for token, pos in all_token_pos_pairs if pos.startswith("V")]
    return verbs
print(extract_verbs(doc))


def bag_of_words(doc, as_strings=True):
    '''Returns a dictionary with word:count pairs. Words are grouped by lemma.'''
    if not isinstance(doc, textacy.doc.Doc):
        doc = to_textacy_doc(doc)
    return doc.to_bag_of_words(as_strings=as_strings)



#### Empath functions
def get_semantic_categories(raw_text):
    category_analysis = lexicon.analyze(raw_text, normalize=True, tokenizer='default')
    top_cats = [[cat[0], cat[1]] for cat in category_analysis.items()]
    top_cats.sort(key=lambda x: x[1], reverse=True)
    return top_cats
