class Protagonist:
    cheated = False
    nStairsClimbed = 0

    def __init__(self,score=0,inv=()):
        self.score = score
        self.inv = inv

    def changeScore(self,points):
        self.score = self.score + points

        s = lambda x: 'point' if (abs(points) == 1) else 'points'

        if points < 0:
            print(f"Your score decreased by {abs(points)} {s(points)}.\n")
        else:
            print(f"Your score increased by {points} {s(points)}.\n")

    def prtScore(self):
        print (f"Your score is {self.score}.")

Player = Protagonist()