class VotingLogic:
    def __init__(self):
        self.votes = {'John': 0, 'Jane': 0, 'Other': 0}
        self.voted_ids = set()

    def cast_vote(self, candidate_name, voter_id):
        if voter_id in self.voted_ids:
            return False 
        if candidate_name in self.votes:
            self.votes[candidate_name] += 1
            self.voted_ids.add(voter_id)
            return True
        return False
    def get_results(self):
        return self.votes