### Import Modules ###
import os
import re
import nltk
#nltk.download('punkt')
import pandas as pd
from tika import parser
from nltk.tokenize import sent_tokenize, word_tokenize

def main_hans(file,stopword_file,csv_file):
    ### Hansard PDF to TXT ###
    Hansard_read = parser.from_file(file)
    file = file.replace('.pdf','.txt')
    pdf_to_txt = open(file,"w+",encoding='utf-8')
    pdf_to_txt.write(Hansard_read['content'])
    pdf_to_txt.close()

    ### Read MP Names CSV and Remove ASCII ###
    col_list1 = ["Special_Name", "Old_Name"]
    dict1 = pd.read_csv(csv_file, index_col=0, usecols=col_list1, squeeze=True).to_dict()
    dict1 = {k.replace(u'\xa0', ' ') : v.replace(u'\xa0', ' ') for k, v in dict1.items()}

    ### Get Hansard Name and Read the Hansard TXT ###
    fnamelist = file.replace('./','')
    hansard = []
    with open(fnamelist, 'r', encoding='utf-8') as f:
        temp_name = f.read().replace('\n', ' ')
        hansard.append(temp_name)

    ### Create Data frame ###
    df = pd.DataFrame(dict1.items(), columns=['mps', 'mps_old'])
    def separate_blocks(whatblock):
        sepblock = sent_tokenize(string_split[whatblock])

        ### Separate each MP Sentences into Strings; One String One line; Follow order in Hansard ###
        sep_string = ''
        temp_name = ''
        for sent in sepblock:
            x = 0  
            for name in df.mps:
                name = name
                if name in sent:
                    if name == temp_name: 
                        temp_sent = sent.replace(name, '')
                        sep_string = sep_string+temp_sent+' '
                    elif 'tidak hadir]' in sent:
                        sep_string = sep_string+'\n'+sent+' '
                        temp_name = name
                    else:
                        sep_string = sep_string+'\n'+sent+' '
                        temp_name = name
                    x = 1                
            if x == 0:
                sep_string = sep_string+sent+' '
        ##########print(sep_string)
        split_sen = sep_string.split('\n')
        
        ### Remove Unwanted String ###
        for i in split_sen:
            if len(i) == 0:
                split_sen.remove(i)
            if 'tidak hadir]' in i:
                split_sen.remove(i)
            if 'Beberapa Ahli:' in i:
                split_sen.remove(i)

        names = []
        sen = []

        for sent in split_sen:
            for namez in df.mps:
                name = namez
                if name in sent:
                    if '] minta' in sent:
                        x = sent.index('] minta')
                        names.append(namez)
                        sen.append(sent[x+1:])
                        
                    elif ':' in sent:
                        y = sent.index(':')
                        names.append(namez)
                        sen.append(sent[y+1:])
        
        name_ques = [v for i, v in enumerate(names)]
        
        sentence = []
        for i, item in enumerate(sen):
            sentence.append(item)

        global df1
        df1 = pd.DataFrame({'Name':name_ques,'Sentence':sentence,'Hansard':fnamelist})
        df2 = pd.DataFrame()
        df2 = df2.append(df1, ignore_index=True)
        return df2

    count = 0
    for hans in hansard: 
        ### Replace in TXT File ###
        hans = hans.replace('\n', ' ').replace(':   ','. ').replace('’',"'").replace('”','"').replace('“','"').replace('...','.').replace('..','.').replace('Tuan Yang di-Pertua:','Tuan Yang di-Pertua Speaker:').replace('Abd.','Abd').replace("Mohd.",'Mohd').replace("Dr.",'Dr').replace("Md.",'Md')
        hans = hans.replace(' bin ',' ').replace(' Bin ',' ').replace(' binti ',' ').replace(' Binti ',' ').replace(' a/l ',' ').replace(' A/L ',' ').replace(' Anak ',' ').replace(' anak ',' ').replace(' a/k ',' ').replace(' A/K ',' ').replace(' a/p ',' ').replace(' (B) ',' ')
        hans = hans.replace('[Berucap tanpa menggunakan pembesar  suara]','[Berucap tanpa menggunakan pembesar  suara].').replace('[Berucap tanpa menggunakan pembesar suara]','[Berucap tanpa menggunakan pembesar suara].')
        
        ### Remove Hansard name, time stamp & page number ###
        dregex = 'DR\.[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4}'
        boxtimeregex = '■\s?[0-9]{1,4}'
        pageregex = '[0-9]{1,4}\s{3,3}'
        hans = re.sub(dregex,'', hans)
        hans = re.sub(boxtimeregex,'', hans)
        hans = re.sub(pageregex,'', hans)
        
        hans = hans.replace('  ',' ').replace('…','.').replace('..','.')
        hans = hans.replace('[Bangun]','[Bangun].').replace('[Tepuk] ','[Tepuk].').replace('[Ketawa]','[Ketawa].').replace('[Dewan ketawa]','[Dewan ketawa].').replace('[Dewan riuh]','[Dewan riuh].').replace('[Berucap tanpa menggunakan pembesar suara]','[Berucap tanpa menggunakan pembesar suara].')
        hans = hans.replace('[Sesi Pertanyaan-pertanyaan Menteri tamat]','').replace('JAWAPAN-JAWAPAN LISAN BAGI PERTANYAAN-PERTANYAAN','').replace('[Masa untuk Pertanyaan-pertanyaan bagi Jawab Lisan tamat]','').replace('WAKTU MESYUARAT DAN URUSAN DIBEBASKAN DARIPADA PERATURAN MESYUARAT','')
        hans = hans.replace(' Kuala Terengganu  ',' Kuala Terengganu. ').replace('[Berucap tanpa menggunakan pembesar suara]..','[Berucap tanpa menggunakan pembesar suara].').replace('[Menyampuk]','[Menyampuk].').replace('Terima kasih Yang Berhormat Lanang ','Terima kasih Yang Berhormat Lanang.')
        
        ### Replace 'Old_Name' into 'Special_Name' ###
        for word, initial in dict1.items():
            hans = hans.replace(initial,word)
    
        token_txt = sent_tokenize(hans)
        string_all = ''
    
        for i in range(len(token_txt)-1):
            token_word = word_tokenize(token_txt[i])
            if ']' in token_txt[i]:
                if 'ketawa]' and'] minta' in token_txt[i]:
                    string_all = string_all+'\n'+token_txt[i]+' '
                else:
                    string_all = string_all+token_txt[i]+' '
            else:
                string_all = string_all+token_txt[i]+' '
                
        string_split = string_all.split('\n')

        ### Delete Everything Before 'Mesyuarat dimulakan' ###
        for i in string_split:
            if 'Mesyuarat dimulakan' in i:
                string_split.remove(i)
        
        for i in range(len(string_split)):
            df3 = separate_blocks(i)
        count += 1

    ### Merge Rows into One Row for Each MP ### 
    aggregation_functions = {'Sentence':'sum'}
    df4 = df3.groupby(df3["Name"]).aggregate(aggregation_functions)
    read_stop = open(stopword_file, 'r')
    stopwords = read_stop.read().split()
    
    def remove_stopword(text):
        text_nostopword = [char for char in text if char not in stopwords]
        return text_nostopword

    df4['Sentence'] = df4['Sentence'].str.lower()  
    df4['Sentence'] = df4.apply(lambda row: nltk.word_tokenize(row['Sentence']), axis=1)
    df4['Sentence'] = df4.apply(lambda row: remove_stopword(row['Sentence']), axis=1)
    os.remove(file)
    df4.to_csv('irdp/Tokenized_Hansard.csv')