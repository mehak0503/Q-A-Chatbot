from bert import QA

model = QA('model')

story = input('Enter story: ')
flag = 'y'
while flag=='y' or flag=='yes':
    ques = input('Enter question: ')
    answer1 = model.predict(story,ques)
    print('Answer is ',answer1['answer'])
    flag = input('Ask more: y/n ')
    
'''
doc = "Hey! I am Mehak. I love dancing. I live in Punjab. I have one brother and one sister. My father is a businessman. My mother is a teacher. I love my family."

q1 = 'What is my name?'
q2 = 'What are my hobbies?'
q3 = 'How many siblings do I have?'
q4 = 'What is the occupation of my mother?'
q5 = 'What is the occupation of my father?'

answer1 = model.predict(doc,q1)
answer2 = model.predict(doc,q2)
answer3 = model.predict(doc,q3)
answer4 = model.predict(doc,q4)
answer5 = model.predict(doc,q5)

print(answer1['answer'])
print(answer2['answer'])
print(answer3['answer'])
print(answer4['answer'])
print(answer5['answer'])
'''