import random

class Game(object):
    OBJECTS = [ 0, 1, 2, 3, 4 ]

    def __init__(self, width, height):
        self._arena = [ [ 0 for i in range(width) ] for j in range(height) ]
        self._width = width
        self._height = height

    def initialize(self):
        for y in range(self._height):
            for x in range(self._width):
                ob = random.choice(Game.OBJECTS)
                self._arena[y][x] = ob
        self._print_arena()
        num_events = self._run()
        print("Number of kabooms: %s" % num_events)

    def _run(self):
        """
            Check matrix for sets that will modify the matrix and execute them.
        """
        
        event = True
        num_events = 0
        while event:
            event = self._run_one()
            num_events = num_events + 1 if event else num_events

        return num_events

    def _run_one(self):
        """
            Scan matrix to find a set that will modify the matrix and execute it.
        """

        #
        # check horizontally
        #

        last_ob = None
        last_len = 0
        found_set = False
        set_y = None
        set_x = None

        for y in range(self._height):
            last_len = 0
            last_ob = None

            for x in range(self._width):
                ob = self._arena[y][x]
                if last_ob == None:
                    last_ob = ob
                    last_len = 1
                elif last_ob != ob:
                    if last_len >= 3:
                        # just terminated a matching set
                        found_set = True
                        set_y = y
                        set_x = x - last_len
                        break
                    else:
                        last_ob = ob
                        last_len = 1
                else:
                    last_len += 1

            if not found_set:
                if last_len >= 3:
                    # last line actually completed a set at the end of the line
                    found_set = True
                    set_y = y
                    set_x = self._width - last_len

            if found_set:
                break
        
        if found_set:
            set_length = last_len
            set_ob = last_ob
            self._process_set(set_y, set_x, set_length, horizontal=True)
            return True

        #
        # check vertically
        #
        last_ob = None
        last_len = 0

        for x in range(self._width):
            last_len = 0
            last_ob = None

            for y in range(self._height):
                ob = self._arena[y][x]
                if last_ob == None:
                    last_ob = ob
                    last_len = 1
                elif last_ob != ob:
                    if last_len >= 3:
                        # just terminated a matching set
                        found_set = True
                        set_x = x
                        set_y = y - last_len
                        break
                    else:
                        last_ob = ob
                        last_len = 1
                else:
                    last_len += 1

            if not found_set:
                if last_len >= 3:
                    # last column actually completed a set at the end
                    found_set = True
                    set_x = x
                    set_y = self._height - last_len

            if found_set:
                break
                
        if found_set:
            set_length = last_len
            set_ob = last_ob
            self._process_set(set_y, set_x, set_length, horizontal=False)
            return True

        return False

        
    def _print_arena(self):
        for y in range(self._height):
            print(''.join([ repr(self._arena[y][x]) for x in range(self._width) ]))
                
                
    def _process_set(self, y, x, length, horizontal):
        print("Kaboom @ (%02d, %02d), length %d, %s" % ( \
                y + 1, x + 1, length, 
                "horizontal" if horizontal else "vertical"
            )
        )
        # for now, just replace them with new random values:
        
        if horizontal:
            for x_offset in range(length):
                self._arena[y][x + x_offset] = random.choice(Game.OBJECTS)
        else:
            for y_offset in range(length):
                self._arena[y + y_offset][x] = random.choice(game.OBJECTS)

        self._print_arena()

if __name__ == "__main__":
    game = Game(10, 10)
    game.initialize()
