import pandas as pd
import numpy as np
import mtgsdk as mtg

text = pd.read_csv(r'c:\Data investigations\mtgo games 2.csv', header=-1)

# generate a list of start and end points (by line) in the mtgo text output that use 'player_name joined the game' as the indicators for when a new game starts.
# The function generates an empty list game_sections. This eventualy be populated into a list of lists of the form [start.1,end.1],[start.2,end.2],etc.
# All games start with (player A has joined the game / Player B has joined the game) on two subsequent lines
# The function uses the 'joined the game' string to identify a new game occurance (first if check skips the second line of the pair (player B)
# Then it appends the ith line start /stop into the game_sections list.

def Logtogamesec (textinput):
    game_sections = []
    start_game_sec = 0
    for i in range(0,len(textinput)):

         stringit = textinput.iloc[i]
         if ('joined the game.' in textinput.iloc[i-1][0]): 
             continue

         if ('joined the game.' in stringit[0]): 
             game_sections = game_sections+[[start_game_sec, i ]] 
             start_game_sec = i
         if i==(len(textinput)-1):
             game_sections = game_sections+[[start_game_sec, i ]] 
             start_game_sec = i
    return(game_sections)

#Identifying the players name, this should be the first two lines from the mtgo text readout which is one line for each players die roll
string1= text.iloc[0][0]
startofname1= string1.find(":",4)+2
player1= string1[startofname1:(string1.find(" ",startofname1))]

string2= text.iloc[1][0]
startofname2= string1.find(":",4)+2
player2= string2[startofname2:(string2.find(" ",startofname2))]

print(player1, player2)
#string.find(":")

print('asdfe'.find('e'))

columnheads= ['p1turn','p2turn','p1land','p2land','p1spell','p2spell']
game_as_df = pd.DataFrame(columns=columheads)

initial_dict= []
p1_turn=0
p2_turn=0

for i in range(0,len(text)):
     #store the ith row in the text csv as stringi. generating the empty dictionary object that will be updated based on stringi contents
     stringi = text.iloc[i][0]
     current_turns = {'p1turn':0,'p2turn':0}
     new_row = {'p1turn':p1_turn,'p2turn':p2_turn,'p1land':0,'p2land':0,'p1spell':0,'p2spell':0, 'p1ability':0, 'p2ability':0, 'p1win':0,        'p2win':0}
     
     #turn is of the form '00:00 AM: Turn x: player', looking at 7 to 15 in the string to prevent instances where turn might appear(player names or spell names or effects resulting in extra turns) 
     if ('Turn' in stringi[6:15] and player1 in stringi): 
         turn_num_start = stringi.find("Turn")+5
         turn_num_end = stringi.find(": ", turn_num_start)
         p1_turn = int( stringi[ turn_num_start : turn_num_end])
     
     if ('Turn' in stringi[6:15] and player2 in stringi): 
         turn_num_start = stringi.find("Turn")+5
         turn_num_end = stringi.find(": ", turn_num_start)
         p2_turn = int( stringi[ turn_num_start : turn_num_end])
     
     #playing lands is of the form 'player plays landname.'
     if ('plays' in stringi and player1 in stringi):
         place = stringi.find("plays")
         new_row['p1land'] = (stringi[place+6:(len(stringi)-1) ] )
                
     if ('plays' in stringi and player2 in stringi):
         place = stringi.find("plays")
         new_row['p2land'] = (stringi[place+6:(len(stringi)-1) ] )
     
     #Spell casting lines are of the form 'player casts spellname.'
     if ('casts' in stringi and player1 in stringi):
         place = stringi.find("casts")
         new_row['p1spell'] = (stringi[place+6:(len(stringi)-1) ] )           
     
     if ('casts' in stringi and player2 in stringi):
         place = stringi.find("casts")
         new_row['p2spell'] = (stringi[place+6:(len(stringi)-1) ] )
     
     #activated abilities of cards 'xx:xx am: playername activates an ability of cardname...'
     if ('activates an ability of' in stringi and player1 in stringi):
         place = stringi.find("activates an ability of")
         new_row['p1ability'] = (stringi [place+24 : stringi.find(" (", place+24) ] )  
                                         
     if ('activates an ability of' in stringi and player2 in stringi):
         place = stringi.find("activates an ability of")
         new_row['p2ability'] = (stringi[ place+24 : stringi.find(" (", place+24) ] )                                    
     
     #winner
     if ('has conceded' in stringi and player2 in stringi):
         new_row['p1win']=1
         new_row['p2win']=-1
     if ('has conceded' in stringi and player1 in stringi):
         new_row['p1win']=-1
         new_row['p2win']=1
     
     #If no values are updated (ie combat results / other effects not included in this dataframe generator) no dict append.           
     
     if ( (new_row['p1ability'] != 0) or (new_row['p2ability'] != 0) or (new_row['p1spell'] != 0) or (new_row['p2spell'] != 0) or 
     (new_row['p1land'] != 0) or (new_row['p2land'] != 0) or (new_row['p2win'] != 0) ):  
         initial_dict.append(new_row)           

#Generate a summary dataframe of the game joined with the mtgsdk library df for a set.
game_summ_df = pd.DataFrame(initial_dict)
        
game_summ_df = game_summ_df.merge(cardbase[['name','cmc']], how='left', left_on='p1spell', right_on='name').rename(columns={'cmc':'p1cmc'}).drop('name',axis=1)
game_summ_df = game_summ_df.merge(cardbase[['name','cmc']], how='left', left_on='p2spell', right_on='name').rename(columns={'cmc':'p2cmc'}).drop('name',axis=1)


#Generate the cmc only dataframe with win/loss as categorical variable from the game summary df. 20 turns assumed 

index = ['player1','player2']
columns = list(range(1,21))
cmc_summ_df = pd.DataFrame(index=index, columns=columns
                           
def cmc_by_turns ( player, turn ):
    if player == 'player1':
        turn_cmc = gamedf[gamedf.p1turn== turn].p1cmc.sum()
        return turn_cmc
    if player == 'player2':
        turn_cmc = gamedf[gamedf.p2turn== turn].p2cmc.sum()
        return turn_cmc                           


for seq in cmcdf.index:
    for seq2 in cmcdf.columns:
        cmcdf.loc[seq, seq2] = cmc_by_turns(player=seq, turn=seq2)

#fill the outcome variable win column of the cmc only df with the first non 0 value in p1win/p2win from game summ df (expecting 0 for all rows until the victor decided row from input text (concedes line)                           
cmcdf.loc['player1','win']=gamedf.p1win[gamedf.p1win.ne(0).idxmax()]                     
cmcdf.loc['player2','win']=gamedf.p2win[gamedf.p2win.ne(0).idxmax()]      
