import os
from collections import Counter


def read_data(fname, word2idx, max_words, max_sentences):
    # stories[story_ind] = [[sentence1], [sentence2], ..., [sentenceN]]
    # questions[question_ind] = {'question': [question], 'answer': [answer], 'story_index': #, 'sentence_index': #}
    stories = dict()
    questions = dict()
    
    
    if len(word2idx) == 0:
        word2idx['<null>'] = 0

    
    if os.path.isfile(fname):
        with open(fname) as f:
            lines = f.readlines()
    else:
        raise Exception("[!] Data {file} not found".format(file=fname))

    for line in lines:
        words = line.split()
        max_words = max(max_words, len(words))
        
        # Determine whether the line indicates the start of a new story
        if words[0] == '1':
            story_ind = len(stories)
            sentence_ind = 0
            stories[story_ind] = []
        
        # Determine whether the line is a question or not
        if '?' in line:
            is_question = True
            question_ind = len(questions)
            questions[question_ind] = {'question': [], 'answer': [], 'story_index': story_ind, 'sentence_index': sentence_ind}
        else:
            is_question = False
            sentence_ind = len(stories[story_ind])
        
        # Parse and append the words to appropriate dictionary / Expand word2idx dictionary
        sentence_list = []
        for k in range(1, len(words)):
            w = words[k].lower()
            
            # Remove punctuation
            if ('.' in w) or ('?' in w):
                w = w[:-1]
            
            # Add new word to dictionary
            if w not in word2idx:
                word2idx[w] = len(word2idx)
            
            # Append sentence to story dict if not question
            if not is_question:
                sentence_list.append(w)
                
                if '.' in words[k]:
                    stories[story_ind].append(sentence_list)
                    break
            
            # Append sentence and answer to question dict if question
            else:
                sentence_list.append(w)
                
                if '?' in words[k]:
                    answer = words[k + 1].lower()
                    
                    if answer not in word2idx:
                        word2idx[answer] = len(word2idx)
                    
                    questions[question_ind]['question'].extend(sentence_list)
                    questions[question_ind]['answer'].append(answer)
                    break
        
        # Update max_sentences
        max_sentences = max(max_sentences, sentence_ind+1)
    
    
    
    # Convert the words into indices
    for idx, context in stories.items():
        for i in range(len(context)):
            temp = list(map(word2idx.get, context[i]))
            context[i] = temp
    
    for idx, value in questions.items():
        temp1 = list(map(word2idx.get, value['question']))
        temp2 = list(map(word2idx.get, value['answer']))
        
        value['question'] = temp1
        value['answer'] = temp2
    #print("Stories ",stories[0])
    #print("Questions ",questions[0])
    
    return stories, questions, max_words, max_sentences


def pad_data(stories, questions, max_words, max_sentences):

    # Pad the context into same size with '<null>'
    for idx, context in stories.items():
        for sentence in context:           
            while len(sentence) < max_words:
                sentence.append(0)
        while len(context) < max_sentences:
            context.append([0] * max_words)
    
    # Pad the question into same size with '<null>'
    for idx, value in questions.items():
        while len(value['question']) < max_words:
            value['question'].append(0)


def depad_data(stories, questions):

    for idx, context in stories.items():
        for i in range(len(context)):
            if 0 in context[i]:
                if context[i][0] == 0:
                    temp = context[:i]
                    context = temp
                    break
                else:
                    index = context[i].index(0)
                    context[i] = context[i][:index]

    for idx, value in questions.items():
        if 0 in value['question']:
            index = value['question'].index(0)
            value['question'] = value['question'][:index]



def read_data_story(story,question,word2idx,max_sentences,max_words):
    sentences = story.split('.')
    sentences = [i for i in sentences if i]
    sentences2idx = []
    for sentence in sentences:
        words = sentence.split(' ')
        tmp = []
        for w in words:
            if w in word2idx:
                tmp.append(word2idx[w])
            else:
                word2idx[w]=len(word2idx)
                tmp.append(word2idx[w])
        sentences2idx.append(tmp)
    '''for sent in sentences2idx:
        while len(sent)<max_words:
            sent.append(0)''' 
    #while len(sentences2idx)<max_sentences:
    #    sentences2idx.append([0]*max_words)
    
    q2idx = []
    qwords = question.split(' ')
    print(qwords)
    for w in qwords:
        if '?' in w:
            w = w[:-1]
        if w in word2idx:
            q2idx.append(word2idx[w])
        else:
            word2idx[w]=len(word2idx)
            q2idx.append(word2idx[w])
    #while len(q2idx)<max_words:
    #    q2idx.append(0)
    storie = dict()
    quest = dict()
    storie[0] = sentences2idx
    quest[0] = {'question':q2idx,'answer':[1],'story_index':0,'sentence_index':0}
    return storie,quest


def read_all_data(ftype, word2idx, max_words, max_sentences):
    # stories[story_ind] = [[sentence1], [sentence2], ..., [sentenceN]]
    # questions[question_ind] = {'question': [question], 'answer': [answer], 'story_index': #, 'sentence_index': #}
    stories = dict()
    questions = dict()
    
    
    if len(word2idx) == 0:
        word2idx['<null>'] = 0

    data_dir = "./bAbI/en-valid"
    for babi_task in range(1,21):
        fname = '{}/qa{}_{}.txt'.format(data_dir, babi_task,ftype)    
        if os.path.isfile(fname):
            with open(fname) as f:
                lines = f.readlines()
        else:
            raise Exception("[!] Data {file} not found".format(file=fname))

        for line in lines:
            words = line.split()
            max_words = max(max_words, len(words))
            
            # Determine whether the line indicates the start of a new story
            if words[0] == '1':
                story_ind = len(stories)
                sentence_ind = 0
                stories[story_ind] = []
            
            # Determine whether the line is a question or not
            if '?' in line:
                is_question = True
                question_ind = len(questions)
                questions[question_ind] = {'question': [], 'answer': [], 'story_index': story_ind, 'sentence_index': sentence_ind}
            else:
                is_question = False
                sentence_ind = len(stories[story_ind])
            
            # Parse and append the words to appropriate dictionary / Expand word2idx dictionary
            sentence_list = []
            for k in range(1, len(words)):
                w = words[k].lower()
                
                # Remove punctuation
                if ('.' in w) or ('?' in w):
                    w = w[:-1]
                
                # Add new word to dictionary
                if w not in word2idx:
                    word2idx[w] = len(word2idx)
                
                # Append sentence to story dict if not question
                if not is_question:
                    sentence_list.append(w)
                    
                    if '.' in words[k]:
                        stories[story_ind].append(sentence_list)
                        break
                
                # Append sentence and answer to question dict if question
                else:
                    sentence_list.append(w)
                    
                    if '?' in words[k]:
                        answer = words[k + 1].lower()
                        answer = answer.split(',')
                        answer = [i for i in answer if i]
                        for ans in answer:
                            if ans=='s':
                                ans = 'south'
                            elif ans=='n':
                                ans = 'north'
                            elif ans=='e':
                                ans = 'east'
                            elif ans=='w':
                                ans = 'west'
                            if ans not in word2idx:
                                word2idx[ans] = len(word2idx)
                            questions[question_ind]['answer'].append(ans)                        
                        questions[question_ind]['question'].extend(sentence_list)
                        #questions[question_ind]['answer'].append(answer)
                        break
            
            # Update max_sentences
            max_sentences = max(max_sentences, sentence_ind+1)
        
    
    
    # Convert the words into indices
    for idx, context in stories.items():
        for i in range(len(context)):
            temp = list(map(word2idx.get, context[i]))
            context[i] = temp
    
    for idx, value in questions.items():
        temp1 = list(map(word2idx.get, value['question']))
        temp2 = list(map(word2idx.get, value['answer']))
        
        value['question'] = temp1
        value['answer'] = temp2
    
    return stories, questions, max_words, max_sentences
