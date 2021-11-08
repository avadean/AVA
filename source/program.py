

class Program:
    def __init__(self, systemPrefix: str = None):
        self.name = systemPrefix
        self.stack = []

        # Get input and error files...

    def abort(self, msg: str = '', code: int = 1):
        # Write error msg and stack to error file...

        # Once we're done writing then zero stack to prevent recursion.
        self.stack = []

        self.stop(code=code)

    def stop(self, code: int = 0):
        if len(self.stack) != 0:
            self.abort('Trace stack not empty on stop', code=2)

        # Close any open files...

        # And finally exit.
        exit(code)

    def entry(self, item: str = None):
        self.stack.append(item)

    def exit(self, item: str = None):
        lastItem = self.stack.pop()

        if lastItem != item:
            self.abort(f'Trace stack error: tried to remove {item} but found {lastItem}')
