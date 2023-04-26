import os
import pickle


class Container:
    folder = 'dataFiles'
    objects = []
    ptr_container = None

    def __init__(self, filename=None):
        if filename is not None:
            self.filename = os.path.join(os.path.dirname(__file__), self.folder, filename)
            self.objects = []
            self.load()
        else:
            self.filename = os.path.join(os.path.dirname(__file__), self.folder, 'testFile.txt')

    @staticmethod
    def get_instance(filename):
        if Container.ptr_container is None:
            Container.ptr_container = Container(filename)
        else:
            Container.ptr_container.set_filename(filename)

        return Container.ptr_container

    def set_filename(self, filename):
        self.filename = os.path.join(os.path.dirname(__file__), self.folder, filename)

    def add_object(self, obj):
        self.objects.append(obj)

    def edit_object(self, index, obj):
        self.objects[index - 1] = obj

    def delete_object(self, index):
        # TODO
        pass

    def get_objects(self):
        self.load()
        return self.objects

    def load(self):
        if os.path.isfile(self.filename):
            with open(self.filename, 'rb') as f:
                data = f.read()

            if data != b'':
                container = pickle.loads(data)
                self.objects = container.objects
        else:
            self.objects = []

    def persist(self):
        for i in range(len(self.objects)):
            self.objects[i].set_index(i + 1)

        with open(self.filename, 'wb') as f:
            pickle.dump(self, f)

    def __getstate__(self):
        return {
            "filename": self.filename,
            "objects": self.objects
        }

    def __setstate__(self, state):
        self.filename = state["filename"]
        self.objects = state["objects"]
