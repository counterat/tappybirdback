class GlobalState:
    def __init__(self):
        self._global_variable = set()
    
    @property
    def global_variable(self):
        return self._global_variable
    
    @global_variable.setter
    def global_variable(self, value):
        self._global_variable = value

# Создаем единственный экземпляр глобального состояния
global_state = GlobalState()
def set_global_variable(value):
    global_state.global_variable = value
    print(f"Global variable set to: {global_state.global_variable}")

def get_global_variable():
    return global_state.global_variable

class LeaderboardUsers:
    def __init__(self):
        self._global_variable = set()
    
    @property
    def global_variable(self):
        return self._global_variable
    
    @global_variable.setter
    def global_variable(self, value):
        self._global_variable = value
leaderboard_state = LeaderboardUsers()
def set_leaderboard_state(value):
    leaderboard_state.global_variable = value
    print(f"Global variable set to: {leaderboard_state.global_variable}")

def get_leaderboard_state():
    return leaderboard_state.global_variable



class LeaderboardSquads:
    def __init__(self):
        self._global_variable = set()
    
    @property
    def global_variable(self):
        return self._global_variable
    
    @global_variable.setter
    def global_variable(self, value):
        self._global_variable = value

leaderboard_squads_state = LeaderboardSquads()
def set_leaderboard_squad_state(value):
    leaderboard_squads_state.global_variable = value
    print(f"Global variable set to: {leaderboard_squads_state.global_variable}")

def get_leaderboard_squad_state():
    return leaderboard_squads_state.global_variable