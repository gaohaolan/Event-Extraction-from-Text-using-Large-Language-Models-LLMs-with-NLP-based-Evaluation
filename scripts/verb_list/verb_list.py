#verb list version 1
act_verbs = {
    "walk", "travel", "go", "move", "climb", "descend", "leap", "run", "ride", 
    "reach", "arrive", "ascend", "decide", "conduct", "track", "tear", 
    "approach", "explore", "continue", "proceed", "advance", 
    "enter", "cross", "wander", "hike", "survey", "round",
    "lead", "stretch", "extend", "wind", "bend", "curve", "open", "narrow", "lie", "border", "dine"
}

obs_verbs = {
    "see", "hear", "note", "observe", "find", "witness", "represent",
    "describe", "identify", "recognize", "perceive", "remark", "record", 
    "mention", "gaze"
}

nat_verbs = {
    "flow", "fall", "erupt", "roar", "howl", "crash", "glow", "shine", "blow", 
    "foam", "surge", "gush", "cascade", "tumble", "drift", "slide", "creep", 
    "swirl", "trickle", "overflow", "subside", "recede", "accumulate", "pass"
}


# geography terms v1
geo_subjects = {
    "river", "stream", "valley", "ridge", "hill", "cliff", 
    "path", "road", "track", "trail", "bridge", "lake", 
    "shore", "mountain", "waterfall", "peak", "summit", "canyon", "bay", "branch"
}



#verb list version 2

# act_verbs_v2
act_verbs = {
    "walk", "travel", "go", "move", "climb", "descend", "leap", "run", "ride",
    "reach", "arrive", "ascend", "decide", "conduct", "track", "tear",
    "approach", "explore", "continue", "proceed", "advance",
    "enter", "cross", "wander", "hike", "survey", "round",
    "lead", "stretch", "extend", "wind", "bend", "curve", "open", "narrow", "lie", "border", "dine",
   
    "make", "take", "come", "give", "leave", "build", "get", "bring", "cover", "follow", "keep", "turn",
    "return", "begin", "visit", "meet", "break", "carry", "command", "live", "bear", "hold", "set",
    "receive", "obtain", "use", "call", "distinguish", "mistake", "fare", "cut", "dig", "search"
}

# obs_verbs_v2
obs_verbs = {
    # Perception
    "see", "hear", "notice", "observe", "witness", "perceive", "gaze",
    "look", "watch", "glimpse", "feel", "sense", "spot",
    
    # Cognition
    "know", "think", "believe", "suppose", "consider", "remember", 
    "forget", "realize", "recognize", "understand", "guess", "expect", 
    "resolve", "determine", "imagine", "suspect", "deem", 
    "conclude", "appreciate", "prefer", "wonder", "ponder", "reflect", 
    "figure", "reckon", "assess", "estimate", "intend", "assume", 
    "speculate", "interpret", "deduce", "infer", "discover", "identify", 
    "detect", "note",
    
    # Emotion / feeling
    "fear", "hope", "wish", "desire", "regret", "enjoy", "like", 
    "dislike", "love", "hate", "admire", "suffer", "endure", 
    "resent", "delight", "marvel", "rejoice", "dread",
    
    # Speech
    "say", "tell", "describe", "mention", "remark", "record", 
    "state", "declare", "announce", "proclaim", "explain", "utter", 
    "reply", "respond", "advise", "admit", "reveal", "recount", 
    "narrate", "assert", "disclose", "promise", "report",
    "express", "complain", "confess", "object", "argue", 
    "insist", "plead",
    
    # Other cognitive actions
    "find", "pursue", "acquire", "appear", "seem"
}

# nat_verbs_v2
nat_verbs = {
    "flow", "fall", "erupt", "roar", "howl", "crash", "glow", "shine", "blow",
    "foam", "surge", "gush", "cascade", "tumble", "drift", "slide", "creep",
    "swirl", "trickle", "overflow", "subside", "recede", "accumulate", "pass",
    "appear", "rise", "seem", "stand", "remain", "grow", "surround", "situate",
    "hang", "belong", "contain", "become"
}


# geography terms v2
geo_subjects = {
    
    "mountain", "hill", "peak", "summit", "ridge", "range", "bluff", "escarpment",
    "knoll", "slope", "cliff", "crag", "crest", "promontory", "headland",

    
    "river", "stream", "brook", "creek", "lake", "pond", "bay", "gulf", "lagoon",
    "channel", "canal", "pool", "spring", "cascade", "waterfall", "estuary",
    "delta", "inlet", "marsh", "swamp", "bog",

    
    "shore", "coast", "beach", "shoreline", "bank", "harbor", "cove", "fjord",
    "spit", "sandbar", "reef",

    
    "valley", "canyon", "gorge", "ravine", "hollow", "basin", "dell", "depression",

    
    "plain", "plateau", "prairie", "meadow", "field", "moor", "heath", "steppe",
    "desert", "dune", "wasteland", "tundra", "scrubland",

    
    "forest", "wood", "woodland", "jungle", "grove", "thicket", "bushland", "shrubland",

    
    "rock", "boulder", "outcrop", "slab", "ledge", "shelf", "scree", "rubble",
    "gravel", "bedrock",

    
    "glacier", "icefield", "snowfield", "iceberg",

    
    "volcano", "crater", "caldera", "geyser", "fumarole", "hotspring",

    
    "cave", "cavern", "grotto", "tunnel", "shaft",

    
    "path", "trail", "track", "road", "bridge", "pass", "divide", "corridor",
    "terrace", "expanse", "surface", "margin", "fringe", "verge", "boundary",
    "edge", "bed", "floor", "wall", "bottom",

    # more...
    "river bank", "mountain pass", "lake shore", "valley floor",
    "canyon wall", "forest edge", "cliff face", "hill top",
    "river bed", "ocean surface", "desert sands", "glacier front",

    # Lake District
    "duddon", "esk", "eden", "derwent", "kent", "cocker", "caldew", "irthing",
    "lune", "brathay", "crake", "emont", "mint", "rothay", "glenderamackin",

    
    "windermere", "coniston", "ullswater", "thirlmere", "wastwater",
    "buttermere", "bassenthwaite", "grasmere", "rydal", "brotherswater",
    "loweswater", "ennerdale water", "haweswater", "blea tarn", "elterwater",

    
    "scafell", "scafell pike", "helvellyn", "skiddaw", "blencathra",
    "great gable", "bowfell", "langdale pikes", "pillar", "grisedale pike",
    "glaramara", "red screes", "lonscale fell", "catbells", "dove crag",
    "seat sandal", "fairfield", "st sunday crag", "harter fell",

    
    "langdale", "borrowdale", "ennerdale", "wasdale", "eskdale",
    "duddon valley", "grisedale", "newlands valley", "martindale",
    "glencoyne", "deepdale", "patterdale",

    
    "wrynose gap", "hardknott pass", "kirkstone pass", "honister pass",
    "whinlatter pass", "dunmail raise", "newlands pass",

    
    "grizedale forest", "whinlatter forest",

    
    "sty head", "esk hause", "stake pass", "nan bield pass"
}