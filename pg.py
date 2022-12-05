class a:
    id = 2
    def __str__(self):
        return str(self.id * 2)

    def __repr__(self):
        return str(self.id)

ds = a()
ds.id = 4
print([ds])