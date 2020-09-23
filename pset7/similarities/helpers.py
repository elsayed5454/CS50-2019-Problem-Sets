from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    return list({line for line in a.splitlines() if line in b.splitlines()})


def sentences(a, b):
    """Return sentences in both a and b"""

    return list({sen for sen in sent_tokenize(a) if sen in sent_tokenize(b)})


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    sub_a = []
    sub_b = []
    ans = []
    for i in range(len(a) - n + 1):
        sub_a.append(a[i:i+n])
    for i in range(len(b) - n + 1):
        sub_b.append(b[i:i+n])
    for sub in sub_a:
        if sub in sub_b and sub not in ans:
            ans.append(sub)
    return ans
