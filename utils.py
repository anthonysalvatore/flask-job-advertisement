import pandas as pd

def gen_docVecs(wv,tk_txts): # generate vector representation for documents
    docs_vectors = pd.DataFrame() # creating empty final dataframe

    for i in range(0,len(tk_txts)):
        tokens = tk_txts[i]
        temp = pd.DataFrame()  # creating a temporary dataframe(store value for 1st doc & for 2nd doc remove the details of 1st & proced through 2nd and so on..)
        for w_ind in range(0, len(tokens)): # looping through each word of a single document and spliting through space
            try:
                word = tokens[w_ind]
                word_vec = wv[word] # if word is present in embeddings(goole provides weights associate with words(300)) then proceed
                temp = pd.concat([temp,pd.DataFrame(word_vec).T], ignore_index = True) # if word is present then append it to temporary dataframe
            except:
                pass
        doc_vector = pd.DataFrame(temp.sum()) # take the sum of each column
        docs_vectors = pd.concat([docs_vectors,doc_vector.T], ignore_index = True) # append each document value to the final dataframe
    return docs_vectors