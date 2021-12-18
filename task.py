import sys


class ToDo():
    def __init__(self):  # Main Logic
        # List that will contain their corresponging tasks, will make the code more streamlined.
        self.pending = []
        self.completed = []

        self.helptext = """Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics"""

        args = sys.argv  # List of arguments passed

        # Figuring out which command was actually run
        if len(args) == 1:
            sys.stdout.buffer.write(self.helptext.encode('utf-8'))  # If there is only 1 argument it means that no argument was passed.

        elif args[1] == 'help':
            sys.stdout.buffer.write(self.helptext.encode('utf-8'))

        elif args[1] == 'add':
            if len(args) < 4:  # Checking to see if the right amount of arguments was passed
                sys.stdout.buffer.write('Error: Missing tasks string. Nothing added!'.encode('utf-8'))
            else:
                self.add(args[2], args[3])
                sys.stdout.buffer.write(f'Added task: "{args[2]}" with priority {args[3]}'.encode('utf-8'))

        elif args[1] == 'ls':
            self.ls()

        elif args[1] == 'del':
            if len(args) < 3:
                sys.stdout.buffer.write('Error: Missing NUMBER for deleting tasks.'.encode('utf-8'))
            else:
                x = self.delete(args[2])
                if x:
                    sys.stdout.buffer.write(f'Deleted task #{args[2]}'.encode('utf-8'))  # Since I am reusing the delete function in done I will send output here.

        elif args[1] == 'done':
            if len(args) < 3:
                sys.stdout.buffer.write('Error: Missing NUMBER for marking tasks as done.'.encode('utf-8'))
            else:
                x = self.done(args[2])
                if x:
                    sys.stdout.buffer.write('Marked item as done.'.encode('utf-8'))

        elif args[1] == 'report':
            self.report()

    def ls(self):
        self.update_pending()
        list = self.pending

        if len(list) == 0:
            sys.stdout.buffer.write(f'There are no pending tasks!'.encode('utf-8'))

        count = 1
        for i in list:
            i = i.split(' ', 1)
            sys.stdout.buffer.write(f'{(count)}. {i[1]} [{i[0]}]\n'.encode('utf-8'))
            count += 1

    def add(self, priority, task):
        try:
            priority = int(priority)
            if int(priority) < 0:
                sys.stdout.buffer.write('Priority has to be a positive integer or 0.'.encode('utf-8'))
                return

        except ValueError as error:
            sys.stdout.buffer.write('Priority has to be a positive integer or 0.'.encode('utf-8'))
            return

        self.update_pending()
        lines = self.pending

        f = open('task.txt', 'w+')
        added = False

        for line in lines:
            if int((line.split(' ', 1))[0]) <= priority:
                continue
            else:

                lines.insert(int(lines.index(f'{line}')), f'{priority} {task}')
                lines = "\n".join(lines)
                f.write(lines)
                added = True
                break

        if not added:
            lines.append(f'{priority} {task}')
            lines = "\n".join(lines)
            f.write(lines)
            added = True

        f.close()
        self.update_pending()
        sys.stdout.buffer.write(f'Added task: "{task}" with priority {priority}'.encode('utf-8'))

    def delete(self, index):
        self.update_pending()
        lines = self.pending

        f = open("task.txt", "w")

        try:
            if int(index) < 1:
                sys.stdout.buffer.write(f'Error: task with index #{index} does not exist. Nothing deleted.'.encode('utf-8'))
                return False

            del lines[int(index) - 1]

        except IndexError as error:
            sys.stdout.buffer.write(f'Error: task with index #{index} does not exist. Nothing deleted.'.encode('utf-8'))
            return False

        except ValueError as error:
            sys.stdout.buffer.write('The index has to be a valid positive integer'.encode('utf-8'))
            return False

        lines = '\n'.join(lines)
        f.write(lines)
        f.close()
        self.update_pending()

        return True

    def done(self, index):
        try:
            index = int(index)
            if int(index) < 0:
                sys.stdout.buffer.write('Invalid index provided.'.encode('utf-8'))
                return

        except ValueError as error:
            sys.stdout.buffer.write('Invalid index provided.'.encode('utf-8'))
            return

        self.update_pending()

        try:
            if index < 1:
                sys.stdout.buffer.write(f'Error: no incomplete item with index #{index} exists.'.encode('utf-8'))
                return False
            task = self.pending[index - 1]
        except IndexError as error:
            sys.stdout.buffer.write(f'Error: no incomplete item with index #{index} exists.'.encode('utf-8'))
            return False

        self.delete(index)

        self.update_completed()
        lines = self.completed
        f = open('completed.txt', 'w')

        lines.append(task.split(' ', 1)[1])
        lines = '\n'.join(lines)
        f.write(lines)
        f.close()

        return True

    def report(self):
        self.update_completed()
        self.update_pending()

        pending = self.pending
        completed = self.completed

        sys.stdout.buffer.write(f'Pending : {len(pending)}\n'.encode('utf-8'))
        count = 1
        for task in pending:
            task = task.split(' ', 1)
            sys.stdout.buffer.write(f'{(count)}. {task[1]} [{task[0]}]\n'.encode('utf-8'))
            count += 1

        sys.stdout.buffer.write(f'\nCompleted : {len(completed)}\n'.encode('utf-8'))
        count = 1
        for task in completed:
            sys.stdout.buffer.write(f'{count}. {task}\n'.encode('utf-8'))
            count += 1

    def update_pending(self):  # Function that updates the pending tasks list made above
        try:
            f = open('task.txt', 'r')
        except FileNotFoundError as error:
            f = open('task.txt', 'x')
            f.close()
            f = open('task.txt', 'r')
        lis = []

        for line in f.readlines():
            line = line.strip('\n')
            lis.append(line)

        self.pending = lis
        f.close()

    def update_completed(self):  # Function that updates the completed tasks list made above
        try:
            f = open('completed.txt', 'r')
        except FileNotFoundError as error:
            f = open('completed.txt', 'x')
            f.close()
            f = open('completed.txt', 'r')
        lis = []

        for line in f.readlines():
            line = line.strip('\n')
            lis.append(line)

        self.completed = lis
        f.close()


if __name__ == "__main__":
    ToDo()
