from pattern import pt_height, pt_weight
from pattern import recognizer
import re

def preprocess(word):
    word = re.sub(r'\D', ' ', word)
    word = re.sub(r'\s+', ' ', word)
    word = re.sub(r'^\s|\s$', '', word)
    return word

def normalize_height(sent):
    match_lst = recognizer(sent, pt_height)
    match_lst = [preprocess(match) for match in match_lst]
    match_lst = [match.split(' ')[-1] for match in match_lst]
    match_lst = [int(match) for match in match_lst]
    match_lst = [100+m*10 if m<9 else m for m in match_lst]
    match_lst = [100+m if m<99 else m for m in match_lst]
    return match_lst

def normalize_weight(sent):
    match_lst = recognizer(sent, pt_weight)
    match_lst = [preprocess(match) for match in match_lst]
    match_lst = [match.split(' ')[0] for match in match_lst]
    match_lst = [int(match) for match in match_lst]
    return match_lst