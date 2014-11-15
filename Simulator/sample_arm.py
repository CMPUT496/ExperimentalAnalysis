class SampleArm():

    # as of right now I am assuming an arm is represented by a numpy array
    def __init__(self, arm):
        self.arm = arm
        self.num_pulls = 0.0
        self.total_reward = 0.0
        self.average = 0.0

    def get_arm(self):
        return self.arm

    def set_arm(self, arm):
        self.arm = arm

    def get_num_pulls(self):
        return self.num_pulls

    def set_num_pulls(self, num_pulls):
        self.num_pulls = num_pulls

    def get_total_reward(self):
        return self.total_reward

    def set_total_reward(self, total_reward):
        self.total_reward = total_reward

    def get_average(self):
        return self.average

    def set_average(self, average):
        self.average = average
