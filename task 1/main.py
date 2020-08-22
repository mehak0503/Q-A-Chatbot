import os

import pprint
import tensorflow as tf

from data import read_data, pad_data,read_data_story,read_all_data
from model import MemN2N
import numpy as np
pp = pprint.PrettyPrinter()


def main(_):
    word2idx = {}
    max_words = 0
    max_sentences = 0

    checkpoint_dir = "./checkpoints"
    data_dir = "./bAbI/en-valid"
    babi_task = 1
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)

    #train_stories, train_questions, max_words, max_sentences = read_all_data('{}/qa{}_train.txt'.format(data_dir, babi_task), word2idx, max_words, max_sentences)
    #valid_stories, valid_questions, max_words, max_sentences = read_all_data('{}/qa{}_valid.txt'.format(data_dir, babi_task), word2idx, max_words, max_sentences)
    #test_stories, test_questions, max_words, max_sentences = read_all_data('{}/qa{}_test.txt'.format(data_dir, babi_task), word2idx, max_words, max_sentences)
    train_stories, train_questions, max_words, max_sentences = read_all_data('train', word2idx, max_words, max_sentences)
    valid_stories, valid_questions, max_words, max_sentences = read_all_data('valid', word2idx, max_words, max_sentences)
    test_stories, test_questions, max_words, max_sentences = read_all_data('test', word2idx, max_words, max_sentences)

    pad_data(train_stories, train_questions, max_words, max_sentences)
    pad_data(valid_stories, valid_questions, max_words, max_sentences)
    pad_data(test_stories, test_questions, max_words, max_sentences)

    idx2word = dict(zip(word2idx.values(), word2idx.keys()))
    #FLAGS.nwords = len(word2idx)
    #FLAGS.max_words = max_words
    #FLAGS.max_sentences = max_sentences
    
    #pp.pprint(flags.FLAGS.__flags)
    print(word2idx)
    is_test = True
    with tf.Session() as sess:
        model = MemN2N(is_test,len(word2idx),max_words,max_sentences, sess)
        model.build_model()
        
        if is_test:
            model.run(valid_stories, valid_questions, test_stories, test_questions)
        else:
            model.run(train_stories, train_questions, valid_stories, valid_questions)

        #predictions, target = model.predict(test_stories, test_questions)
        #cnt = 0
        #for i in range(len(target)):
            #print(idx2word[np.argmax(predictions[i])],idx2word[np.argmax(target[i])])
            #if np.argmax(predictions[i])==np.argmax(target[i]):
            #    cnt+=1
        #print("Test set accuracy ",cnt/len(target))
        print(word2idx)
        idx2word = dict(zip(word2idx.values(), word2idx.keys()))
        stry = input("Enter the story: ")
        flag = 'y'
        while flag=='y':
            que = input("Enter the quest: ")
            print(stry,type(stry),que,type(que))
            story,quest = read_data_story(stry.lower(),que.lower(),word2idx,max_sentences,max_words)
            pad_data(story,quest,max_words,max_sentences)
            #print(story,quest,word2idx)
            prediction,target1 = model.predict(story,quest)
            print(idx2word[np.argmax(prediction[0])])
            flag = input('You want to continue: y or n ')



if __name__ == '__main__':
    tf.app.run()
