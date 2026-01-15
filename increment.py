# lifted from http://bit.ly/2iJfRou (codereview.stackexchange.com)
def incr_chr(c):
    return chr(ord(c) + 1) if c != 'Z' else 'A'

def incr_str(s):
    lpart = s.rstrip('Z')
    num_replacements = len(s) - len(lpart)
    new_s = lpart[:-1] + incr_chr(lpart[-1]) if lpart else 'A'
    new_s += 'A' * num_replacements
    return new_s