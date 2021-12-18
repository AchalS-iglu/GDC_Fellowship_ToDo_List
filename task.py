#print("Hello, World!")

import sys

class ToDo():
    def __init__(self):

        self.pending = []
        self.completed = []

        self.helptext="""Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics"""

        try:
            args = sys.argv

            if len(args) == 1:
                sys.stdout.buffer.write(self.helptext.encode('utf-8'))
            
            elif args[1] == 'help':
                sys.stdout.buffer.write(self.helptext.encode('utf-8'))

            elif args[1] == 'add':
                if len(args) < 4:
                    sys.stdout.buffer.write('Error: Missing tasks string. Nothing added!'.encode('utf-8'))
                else:                  
                    self.add(args[2], args[3])
                    sys.stdout.buffer.write(f'Added task: "{args[2]}" with priority {args[3]}'.encode('utf-8'))
                                        
            elif args[1] == 'ls':
                self.ls()
            
            elif args[1] == 'del':
                self.delete(args[2])
                sys.stdout.buffer.write(f'Deleted item with index {args[2]}'.encode('utf-8'))
            
            elif args[1] == 'done':
                self.done(args[2])
                sys.stdout.buffer.write('Marked item as done.'.encode('utf-8'))
            
            elif args[1] == 'report':
                self.report()
            

        #except IndexError as error:
        #    sys.stdout.buffer.write(self.helptext.encode('utf-8'))

        except Exception as error:
            raise error
 
    def ls(self):
        try:
            self.update_pending()

            count = 1
            for i in self.pending:
                i = i.split(' ', 1)
                #print(i)
                sys.stdout.buffer.write(f'{(count)}. {i[1]} [{i[0]}]\n'.encode('utf-8'))
                count += 1

        except FileNotFoundError as error:
            sys.stdout.buffer.write('The tasks file not found, kindly begin by adding new tasks!'.encode('utf-8'))
            
        except Exception as error:
            raise error

    def add(self, priority, task):
        try:
            try:
                priority = int(priority)
                if int(priority) < 0:
                    sys.stdout.buffer.write('Prority has to be a positive integer or 0.'.encode('utf-8'))
                    return
 
            except ValueError as error:
                sys.stdout.buffer.write('Prority has to be a positive integer or 0.'.encode('utf-8'))
                return

            self.update_pending()
            lines = self.pending

            f = open('task.txt', 'w+')
            added = False

            for l in lines:
                if int(( l.split(' ', 1) )[0]) <= priority:
                    continue
                else:

                    lines.insert(int(lines.index(f'{l}')), f'{priority} {task}')
                    lines = "\n".join(lines)
                    f.write(lines)
                    added = True
                    break
            
            if added == False:
                lines.append(f'{priority} {task}')
                lines = "\n".join(lines)
                f.write(lines)
                added = True
            
            f.close()
            self.update_pending()
            sys.stdout.buffer.write(f'Added task: "{task}" with priority {priority}'.encode('utf-8'))
            
        except Exception as error:
            raise error

    def delete(self, index):
        self.update_pending()
        lines = self.pending
        
        f = open("task.txt", "w")

        try:
            del lines[int(index) - 1]
        except IndexError as error:
            sys.stdout.buffer.write(f'Error: item with index {index} does not exist. Nothing deleted.'.encode('utf-8'))
        except ValueError as error:
            sys.stdout.buffer.write('The index has to be a valid positive integer'.encode('utf-8'))
        
        lines = '\n'.join(lines)
        f.write(lines)
        f.close()
        self.update_pending()

    def done(self, index):
        try:
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
                task = self.pending[index - 1]     
            except IndexError as error:
                sys.stdout.buffer.write(f'Error: no incomplete item with index {index} exists.'.encode('utf-8'))
                return

            self.delete(index)

            self.update_completed()
            lines = self.completed
            f = open('completed.txt', 'w')

            lines.append(task.split(' ', 1)[1])
            lines = '\n'.join(lines)
            f.write(lines)
            f.close()

        except Exception as error:
            raise error

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

        sys.stdout.buffer.write(f'Completed : {len(completed)}\n'.encode('utf-8'))
        count = 1
        for task in completed:
            sys.stdout.buffer.write(f'{count}. {task}\n'.encode('utf-8'))

    def update_pending(self):
        try:
            f = open('task.txt', 'a+')
            lis = []

            for l in f.readlines():
                l = l.strip('\n')
                lis.append(l)

            self.pending = lis
            f.close()

        except Exception as error:
            raise error
    
    def update_completed(self):
        try:
            f = open('completed.txt', 'a+')
            lis = []

            for l in f.readlines():
                l = l.strip('\n')
                lis.append(l)

            self.completed = lis
            f.close()

        except Exception as error:
            raise error
    

if __name__ == "__main__":
    ToDo()
    #args = parser.parse_args()
    #print(args.test)