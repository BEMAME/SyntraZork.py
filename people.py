class Protagonist:
    def __init__(self,score=0,inv=()):
        self.score = score
        self.inv = inv

    def changeScore(self,points):
        self.score = self.score + points
        if points < 0:
            print(f"Your score decreased by {abs(points)} points.\n")
        else:
            print(f"Your score increased by {points} points.\n")

    def prtScore(self):
        print (f"Your score is {self.score}.")

Player = Protagonist()