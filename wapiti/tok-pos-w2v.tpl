# feature extraction patterns for CRF
# see https://wapiti.limsi.fr/manual.html#patterns
# Only the first character (U, B, *) and the %x[,] %t[,] %m[,] specifications are significant

# TOKEN SHAPE
# binary
*:punct:1,0:%t[0,0,"\p"]
*:digit:1,0:%t[0,0,"\d"]
*:upper:1,0:%t[0,0,"^\u"]
*:lower:1,0:%t[0,0,"^\l"]
*:allupper:1,0:%t[0,0,"^\u+$"]
*:alllower:1,0:%t[0,0,"^\l+$"]
# the feature is the punctuation or digit itself
*:punctM:1,0:%m[0,0,"\p"]
*:digitM:1,0:%m[0,0,"\d"]

# seems redundant with punctM?
U:comma:1,0:%t[0,0,"\,"]
U:period:1,0:%t[0,0,"\."]
U:equal:1,0:%t[0,0,"\="]

# bigram
# binary
U:punct:2,0:%t[0,0,"\p"]/%t[1,0,"\p"]
U:digit:2,0:%t[0,0,"\d"]/%t[1,0,"\d"]
U:punct:2,-1:%t[-1,0,"\p"]/%t[0,0,"\p"]
U:digit:2,-1:%t[-1,0,"\d"]/%t[0,0,"\d"]
# the feature is the punctuation or digit itself
U:punctM:2,0:%m[0,0,"\p"]/%m[1,0,"\p"]
U:digitM:2,0:%m[0,0,"\d"]/%m[1,0,"\d"]
U:punctM:2,-1:%m[-1,0,"\p"]/%m[0,0,"\p"]
U:digitM:2,-1:%m[-1,0,"\d"]/%m[0,0,"\d"]

# TOKEN
*:tok:1,-1:%x[-1,0]
*:tok:1,0:%x[0,0]
*:tok:1,1:%x[1,0]
# bigram
*:tok:2,-1:%x[-1,0]/%x[0,0]
*:tok:2,0:%x[0,0]/%x[1,0]

# 3-char PREFIX and SUFFIX
U:pref:%m[0,0,"^..."]
U:suff:%m[0,0,"...$"]
# 1-4-char PREFIX and SUFFIX
# U:pref:%m[0,0,"^..?.?.?"]
# U:suff:%m[0,0,".?.?.?.$"]

# POS tag: universal
# *:Upos:0,1:%x[0,2]
# *:Upos:2,-1:%x[-1,2]/%x[0,2]
# *:Upos:2,0:%x[0,2]/%x[1,2]
# POS tag: language-specific (Penn Treebank)
*:tag:0,1:%x[0,3]
*:tag:2,-1:%x[-1,3]/%x[0,3]
*:tag:2,0:%x[0,3]/%x[1,3]

# word2vec cluster ID
*:w2v:0,1:%x[0,4]
*:w2v:2,-1:%x[-1,4]/%x[0,4]
*:w2v:2,0:%x[0,4]/%x[1,4]

# label itself (U), including label bigram (B)
*
