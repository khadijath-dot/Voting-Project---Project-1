class VotingLogic:
    def __init__(self):
        self.votes = {'John': 0, 'Jane': 0, 'Other': 0}

    def cast_vote(self, candidate_name):
        if candidate_name in self.votes:
            self.votes[candidate_name] += 1

    def get_results(self):
        return self.votes