import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        # sets self.env = env, state = None, next_waypoint = None, and a default color
        super(LearningAgent, self).__init__(env)
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.next_waypoint = None
        self.total_reward = 0
        self.state = None

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        sensed_inputs = self.env.sense(self)
        print sensed_inputs

        default_state = 'ok to PROCEED or '
        # At an intersection with a red light
        if sensed_inputs['light'] == 'red' and sensed_inputs['left'] == None:
            self.state = "ok to RIGHT on RED"
        elif sensed_inputs['light'] == 'red':
            self.state = "STOP RED light"

        # At an intersection with a green light
        if sensed_inputs['light'] == 'green' and sensed_inputs['oncoming'] == None and sensed_inputs['left'] == None:
            self.state = default_state + "LEFT on GREEN" + " or RIGHT on GREEN"
        elif sensed_inputs['light'] == 'green' and sensed_inputs['left'] == None:
            self.state = default_state + "RIGHT on GREEN"
        elif sensed_inputs['light'] == 'green':
            self.state = "ok to PROCEED"







        # TODO: Select action according to your policy
        action = random.choice([None, 'forward', 'left', 'right']) #None, 'forward', 'left', 'right'

        # Execute action and get reward
        reward = self.env.act(self, action)


        # TODO: Learn policy based on state, action, reward

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=1.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False



    sim.run(n_trials=10)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
