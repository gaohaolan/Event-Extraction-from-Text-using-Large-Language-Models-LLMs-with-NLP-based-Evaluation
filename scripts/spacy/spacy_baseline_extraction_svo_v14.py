import spacy
import json
from tqdm import tqdm

doc_path = "processed/processed_paragraphs_100.jsonl"
output_path = "results/spacy-result/spacy_svo_para100.jsonl"

# Load Spacy 
nlp = spacy.load("en_core_web_sm")

# act_verbs_v2
act_verbs = {
    "walk", "travel", "go", "move", "climb", "descend", "leap", "run", "ride",
    "reach", "arrive", "ascend", "decide", "conduct", "track", "tear",
    "approach", "explore", "continue", "proceed", "advance",
    "enter", "cross", "wander", "hike", "survey", "round",
    "lead", "stretch", "extend", "wind", "bend", "curve", "open", "narrow", "lie", "border", "dine",
    # more...
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


# geography terms
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

def get_verb_category(verb_lemma):
    if verb_lemma in act_verbs:
        return "action"
    elif verb_lemma in obs_verbs:
        return "mental"
    elif verb_lemma in nat_verbs:
        return "nature"
    else:
        return "other"

def adjust_category(subj, initial_category):
    if initial_category == "action" and subj:
        subj_lower = subj.lower()
        for term in geo_subjects:
            if term in subj_lower:
                return "nature"
    return initial_category

def is_time_expression(token):
    time_keywords = {"day", "night", "morning", "evening", "hour", "minute", "second", "time", "year", "century"}
    return token.lemma_.lower() in time_keywords or token.ent_type_ in {"DATE", "TIME"}

def get_noun_phrase(token):
    for chunk in token.doc.noun_chunks:
        if token in chunk:
            return chunk.text
    return token.text

def get_subject(token, depth=0, max_depth=10):
    if depth > max_depth:
        return None
    for child in token.children:
        if child.dep_ in ("nsubj", "nsubjpass"):
            return get_noun_phrase(child)
        if child.dep_ == "csubj":
            inner = get_subject(child, depth=depth+1, max_depth=max_depth)
            if inner:
                return inner
    if token.dep_ == "conj":
        return get_subject(token.head, depth=depth+1, max_depth=max_depth)
    if token.dep_ == "acl":
        return get_noun_phrase(token.head)
    if token.head != token:
        return get_subject(token.head, depth=depth+1, max_depth=max_depth)
    return None

def get_object_phrase(child):
    if child.pos_ == "NOUN" or child.pos_ == "PROPN":
        return get_noun_phrase(child)
    for chunk in child.doc.noun_chunks:
        if child in chunk:
            return chunk.text
    span = list(child.subtree)
    phrase = " ".join([t.text for t in span if not is_time_expression(t)])
    return phrase

def get_phrasal_verb(token):
    verb_base = token.text
    particles = []
    preps = []
    phrasal_preps = {"about", "across", "along", "around", "through", "over", "off", "onto", "into", "out", "upon", "up", "down"}
    for child in token.children:
        if child.dep_ == "prt":
            particles.append(child.text)
        elif child.dep_ == "prep" and child.text.lower() in phrasal_preps:
            preps.append(child.text)
    verb_phrase = verb_base
    if particles:
        verb_phrase += " " + " ".join(particles)
    if preps:
        verb_phrase += " " + " ".join(preps)
    return verb_phrase

def extract_svo(token, inherited_subj=None, visited=None):
    events = []
    if token.i in visited:
        return events
    visited.add(token.i)

    verb_lemma = token.lemma_.lower()
    if verb_lemma not in act_verbs | obs_verbs | nat_verbs:
        return events
    if token.dep_ == "acl":
        return events

    subj = get_subject(token)
    if subj is None and inherited_subj is not None:
        subj = inherited_subj

    is_neg = any(child.dep_ == "neg" for child in token.children)
    verb_phrase = get_phrasal_verb(token)
    if is_neg:
        verb_phrase += " (neg)"
    verb_category = get_verb_category(verb_lemma)
    verb_category = adjust_category(subj, verb_category)

    objs = []
    for child in token.children:
        if child.dep_ in ("dobj", "attr"):
            objs.append(get_object_phrase(child))
            for conj in child.children:
                if conj.dep_ == "conj":
                    objs.append(get_object_phrase(conj))
            break
    if not objs:
        for prep in token.children:
            if prep.dep_ == "prep":
                for pobj in prep.children:
                    if pobj.dep_ == "pobj" and not is_time_expression(pobj):
                        objs.append(get_object_phrase(pobj))
                        for conj in pobj.children:
                            if conj.dep_ == "conj":
                                objs.append(get_object_phrase(conj))
                        break
                if objs:
                    break

    if subj and objs:
        for obj in objs:
            if obj.lower() not in {"which", "that"}:
                events.append({
                    "subject": subj,
                    "verb": verb_phrase,
                    "object": obj,
                    "verb_category": verb_category
                })

    if subj and not objs:
      events.append({
         "subject": subj,
         "verb": verb_phrase,
         "object": None,
         "verb_category": verb_category
      })

    for child in token.children:
        if child.dep_ in ("xcomp", "ccomp", "advcl", "conj") and (child.pos_ == "VERB" or child.tag_.startswith("VB")):
            events.extend(extract_svo(child, inherited_subj=subj, visited=visited))
    
    return events

def extract_relcl(doc):
    events = []
    for token in doc:
        if token.dep_ == "relcl" and token.pos_ == "VERB":
            verb_lemma = token.lemma_.lower()
            if verb_lemma not in act_verbs | obs_verbs | nat_verbs:
                continue
            subj = None
            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subj = get_noun_phrase(child)
                    break
            obj = get_noun_phrase(token.head)
            if subj and obj:
                verb_phrase = get_phrasal_verb(token)
                verb_category = get_verb_category(verb_lemma)
                verb_category = adjust_category(subj, verb_category)
                events.append({
                    "subject": subj,
                    "verb": verb_phrase,
                    "object": obj,
                    "verb_category": verb_category
                })
    return events

def process():
    with open(doc_path, "r", encoding="utf-8") as f_in, open(output_path, "w", encoding="utf-8") as f_out:
        for line in tqdm(f_in):
            item = json.loads(line)
            text = item["text"]
            doc = nlp(text)
            events = []
            visited = set()

            for token in doc:
                if token.pos_ == "VERB" or token.tag_.startswith("VB"):
                    events.extend(extract_svo(token, visited=visited))
            events.extend(extract_relcl(doc))

            item["events"] = events
            f_out.write(json.dumps(item, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    process()

