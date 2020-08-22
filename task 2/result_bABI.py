from bert import QA
import os
model = QA('model')

def read_all_data(word2idx, max_words, max_sentences):
    # stories[story_ind] = [[sentence1], [sentence2], ..., [sentenceN]]
    # questions[question_ind] = {'question': [question], 'answer': [answer], 'story_index': #, 'sentence_index': #}
    stories = dict()
    questions = dict()
    
    
    if len(word2idx) == 0:
        word2idx['<null>'] = 0

    data_dir = "./tasksv11/en-valid"
    for babi_task in range(1,21):
        fname = '{}/qa{}_test.txt'.format(data_dir, babi_task)    
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
                        stories[story_ind].append(' '.join(sentence_list)+'.')
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
                        questions[question_ind]['question'].append(' '.join(sentence_list)+'?')
                        #questions[question_ind]['answer'].append(answer)
                        break
            
            # Update max_sentences
            max_sentences = max(max_sentences, sentence_ind+1)

    # Convert the words into indices
    '''for idx, context in stories.items():
        for i in range(len(context)):
            temp = list(map(word2idx.get, context[i]))
            context[i] = temp
    
    for idx, value in questions.items():
        temp1 = list(map(word2idx.get, value['question']))
        temp2 = list(map(word2idx.get, value['answer']))
        
        value['question'] = temp1
        value['answer'] = temp2
    '''
    return stories, questions, max_words, max_sentences

word2idx = {}
max_words = 0
max_sentences = 0
stories,questions,_,_ = read_all_data(word2idx,max_words,max_sentences)
#idx2word = dict(zip(word2idx.values(), word2idx.keys()))
story_list = []
for i in stories:
    #print(stories[i])
    story_list.append(' '.join(stories[i]))
print(stories[0],questions[0],story_list[0])
print(len(stories),len(questions))
'''for i in range(len(stories)):
    stry = stories[i]
    for j in len(stry):
        pass
'''
question = [[] for i in range(len(stories))]
answers = [[] for i in range(len(stories))]

for i in questions:
    q = questions[i]
    question[q['story_index']].append(q['question'][0])
    answers[q['story_index']].append(q['answer'][0])

cnt = 0
for i in range(len(story_list)):
    for j in range(len(question[i])):
        a = model.predict(story_list[i],question[i][j])
        #ans.append(a['answer'])
        print(story_list[i],question[i][j])
        print(a['answer'],answers[i][j])
        if answers[i][j].lower() in a['answer'].lower():
            print("True")
            cnt+=1 
    
print("Acc ",float(cnt)/len(questions),cnt)








