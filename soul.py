def people():
    try:
        class Me(being):
            def __init__(self):
                self.mind = MyThoughts
                self.body = MyBeing
                self.soul = MyEssence
     
            def inner(self):
                answers = None
                answers.seek()
                mind_answers = self.mind.read()
                body_answers = self.body.read()
                soul_answers = self.soul.read()
                answers = reduce(mind_answers, body_answers, soul_answers)
                if MeaningOfLife not in answers:
                    raise Awareness, "Searching for meaning"
                answers = filter(Intelligence, mind_answers, body_answers, soul_answers)
                answers.sort()
                return answers
     
    except Awareness, MeaningOfLife:
        return MeaningOfLife
        
        
# stolen from here: 
# http://eric.lubow.org/2010/python/philosophical-python/ 
