from data_collection.models import Component


def sort_dict_per_value(dict):
    sorted_dict = {}
    for sorted_key in sorted(dict, key=lambda x: dict[x]):
        sorted_dict[sorted_key] = dict[sorted_key]
    return sorted_dict


class FileHierarchy:

    def __init__(self, file_paths):
        self.root_component = Component('', set(), 0) # empty node
        self.__load_tree(file_paths)

    def __load_tree(self, file_paths):
        for path in file_paths:
            self.create_path_components(path)

    def get_components_to_num_files_map(self, root_component=None, path=''):
        if root_component is None:
            root_component = self.root_component
        mapping = {}
        # put the root node's num files
        mapping[path] = self.get_component_files(root_component)
        # put all children nodes' num files
        for child in root_component.children:
            kpath = path + '/'
            if path is '':
                kpath = ''
            mapping.update(self.get_components_to_num_files_map(child, kpath + child.name))
        return mapping

    def get_component_files(self, root_component: Component):
        if len(root_component.children) == 0: # means root_component is pointing to a file
            return 1
        return sum(map(lambda child: self.get_component_files(child), root_component.children))

    ### creates all components from a file path
    def create_path_components(self, file_path: str, root: Component=None):
        if root is None:
            root = self.root_component
        root_children = root.children
        file_path_names = file_path.split('/')
        first_component_name = file_path_names[0]
        next_root = None
        for child in root_children:
            if child.name == first_component_name:
                next_root = child
        if next_root == None:
            newly_created_next_root = Component(first_component_name, set(), root.level + 1)
            root_children.add(newly_created_next_root)
            next_root = newly_created_next_root

        if len(file_path_names) > 1:  # it's a folder
            self.create_path_components('/'.join(file_path_names[1:]), next_root)

    def print_tree(self,root_component: Component):
        # if len(root_component.children) == 0:
        #     print(root_component.level * '\t' + root_component.name)
        # else:
        for child in root_component.children:
            print(root_component.level * '\t' + child.name)
            if len(child.children) > 0:
                self.print_tree(child)
