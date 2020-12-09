import sys
from copy import deepcopy

class Program:
    def __init__(self, program_text):
        self._program = []
        for p in program_text:
            self._program.append([ p[:3], int(p[4:]) ])

        self.reset()

    def reset(self, accumulator_initial_value=0, program_start_line=0):
        self._accumulator = accumulator_initial_value
        self._program_line_idx = program_start_line

    def at_end_of_program(self):
        return self._program_line_idx >= len(self._program)

    def run_norepeat(self):
        executed_line_indices_ = set()
        while True:
            cmd_, val_ = self._program[self._program_line_idx]
            executed_line_indices_.add(self._program_line_idx)

            if cmd_ == 'nop': self._program_line_idx += 1
            elif cmd_ == 'jmp': self._program_line_idx += val_
            elif cmd_ == 'acc':
                self._accumulator += val_
                self._program_line_idx += 1
            else: print(" Got unrecognized cmd " + cmd_)

            if self.at_end_of_program():
                return self._accumulator, True
            elif self._program_line_idx in executed_line_indices_:
                return self._accumulator, False

    def try_swap_nop_jmp_for_norepeat(self):
        last_changed_index_ = -1
        while True:
            program_backup_ = deepcopy(self._program)

            while True:
                last_changed_index_ += 1
                if last_changed_index_ >= len(self._program): return None
                if self._program[last_changed_index_][0] == 'nop':
                    self._program[last_changed_index_][0] = 'jmp'
                    break
                elif self._program[last_changed_index_][0] == 'jmp':
                    self._program[last_changed_index_][0] = 'nop'
                    break

            self.reset()
            accumulator_, norepeat_ = self.run_norepeat()
            if norepeat_: return accumulator_            

            self._program = program_backup_


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data_ = f.read().splitlines()

    program_ = Program(data_)

    if sys.argv[2] == '1':
        out_ = program_.run_norepeat()[0]
    elif sys.argv[2] == '2':
        out_ = program_.try_swap_nop_jmp_for_norepeat()

    print(out_)
    