test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""




"""Both files and folders are FileSystemObjects. For a larger project this would be a superclass
containing only the things common to both, and then files and folders would each subclass this class.
That would be overkill for this exercise."""
class FileSystemObject:

    def __init__(self, ref, name, parent = None, children = [], filesize = 0, is_folder = False):
        self.name = name
        self.parent = parent
        self.children = children
        self.filesize = filesize
        self.is_folder = is_folder
        if self.parent:
            self.path = self.parent.path + '/' + self.name
        else:
            self.path = self.name
        ref[self.path] = self

    def size(self):
        if self.is_folder:
            return sum([c.size() for c in self.children]) if self.children else 0
        else:
            return self.filesize


"""Displays the filesystem, treating folder as its root, using indentation to indicate hierarchy."""
def show_filesystem(folder):
    def show_folder(f, d):
        print(' ' * d, f.name)
        for c in f.children:
            show_folder(c, d+2)
    show_folder(folder, 0)



"""Returns the FSO of the directory we want to change to."""
def cd(current_folder, target):
    if target == '/':
        return ref['/']
    elif target == '..':
        if current_folder.parent:
            return current_folder.parent
        else:
            return current_folder
    else:
        for c in current_folder.children:
            if c.name == target:
                return c
    raise(Exception('dir ' + target + ' not found.'))

"""Uses the list of results to process an ls command."""
def ls(current_folder, results):
    for result in results:
        (size_or_type, name) = result.split()
        if name in [c.name for c in current_folder.children]:
            print('   ', result, 'already present')
            continue
        if size_or_type == 'dir':
            current_folder.children.append(FileSystemObject(ref, name, current_folder, children = [], is_folder = True))
        else:
            try:
                filesize = int(size_or_type)
            except:
                raise(Exception('ls result is an unrecognized format'))
            current_folder.children.append(FileSystemObject(ref, name, current_folder, children = [], filesize = filesize))






"""A global dictionary storing a unique reference to each filesystem object in the hierarchy. This is
only useful for $ cd / commands, but in a real filesystem it's possible to directly change to any directory."""
ref = {}


root = FileSystemObject(ref, '/', is_folder = True)
with open('day7_input.txt', 'r') as f:
    input = f.readlines()

current_folder = root

while input:
    cmd = input.pop(0)
    assert(cmd[:2] == '$ ')     # we should only be parsing commands
    cmd = cmd[2:].split()
    if len(cmd) == 1:
        assert(cmd[0] == 'ls')
        results = []
        while input and input[0][0] != '$':
            results.append(input.pop(0))
        ls(current_folder, results)
    elif len(cmd) == 2:
        assert(cmd[0] == 'cd')
        current_folder = cd(current_folder, cmd[1])
    else:
        raise(Exception('unrecognized command'))


total_size = 70000000
unused_size = total_size - root.size()
target_to_delete = 30000000 - unused_size

best_size = total_size+1
best_path = None
for (path, fso) in ref.items():
    if fso.is_folder:
        s = fso.size()
        new_unused = unused_size + s
        if new_unused >= 30000000 and s < best_size:
                best_size = s
                best_path = fso.path

print(best_path, best_size)










