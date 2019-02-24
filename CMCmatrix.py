RNAfullset = mtgsdk.Card.where(set='RNA').all()

cardbase=pd.DataFrame(0, index=range(0,len(RNAfullset)), columns= ['name','mana_cost','text'])
for i,card in enumerate(RNAfullset):
    cardbase.loc[i,'name']=card.name
    cardbase.loc[i,'cost']=card.mana_cost
    cardbase.loc[i,'name']=card.text
    
cmc_list = ['W/B', 'B/R', 'W/U', 'G/U','R/G','B','G','U','W','R']

def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    
    return  mainString 

#function for turning the mtgsdk mana cost column into generic converted mana cost( formated {num}{color}{color} etc. can handle hybrid mana of form {W/B} as long as cmc_list variable is properly defined earlier to include all 10 possible formats. This ignores variable costs of {x} for spells like fireball for now.
def cmc_col_gen (mana_cost):
    mana_as_num=replaceMultiple(str(mana_cost), cmc_list, '1').replace('{','').replace('X','').replace('None','').split('}')
    cmc = sum( list(map(int,[x for x in mana_as_num if x] )) )
    return(cmc)

cardbase['cmc'] = np.vectorize(cmc_col_gen)(cardbase['mana_cost'])
