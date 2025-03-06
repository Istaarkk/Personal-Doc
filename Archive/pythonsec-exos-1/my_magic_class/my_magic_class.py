class Dummy:
    def __init__(self, *args, **kwargs):
        self._args = list(args)
        self._desc = "instance magic"  

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    def __getitem__(self, index):
        return self._args[index]

    def __len__(self):
        return len(self._args)

