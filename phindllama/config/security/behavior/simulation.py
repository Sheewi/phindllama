# human_simulator.py
class HumanSimulator:
    def __init__(self):
        self.profiles = {
            'trader': load_profile('trader.json'),
            'investor': load_profile('investor.json')
        }
    
    def simulate(self, profile_type):
        profile = self.profiles[profile_type]
        return BehavioralSequence(
            mouse_movements=profile['mouse'],
            keystroke_dynamics=profile['keystrokes'],
            attention_pattern=profile['attention']
        )