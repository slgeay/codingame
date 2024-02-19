class AI():
    def __init__(self):
        pass

    def iterate(self, input:str):
        inputs = input.splitlines()
        x, y = [int(i) for i in inputs.pop(0).split()]

        human_count = int(inputs.pop(0))
        for i in range(human_count):
            human_id, human_x, human_y = [int(j) for j in inputs.pop(0).split()]
        
        zombie_count = int(inputs.pop(0))
        for i in range(zombie_count):
            zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in inputs.pop(0).split()]

        return "0 0"

    def __repr__(self):
        return f"AI{()})"