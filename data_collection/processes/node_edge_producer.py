from data_collection.processes.author_to_commit import get_author_to_commits_map
from data_visualization.structures import Node, Edge, NodeType
from data_collection.helpers import FileHierarchy, sort_dict_per_value
edges = []
nodes = []

MINIMUM_FILES_IN_MODULE = 20

author_to_commits = get_author_to_commits_map()


def get_all_file_paths():
    all_file_paths = []
    for commits in author_to_commits.values():
        for commit in commits:
            file_paths = list(map(lambda file: file['filepath'], commit['files']))
            for file_path in file_paths:
                if file_path not in all_file_paths:
                    all_file_paths.append(file_path)
    return all_file_paths


def get_author_to_file_paths():
    author_to_file_paths = {}
    for author in author_to_commits.keys():
        author_commits = author_to_commits[author]
        for commit in author_commits:
            file_paths = list(map(lambda file: file['filepath'], commit['files']))
            author_to_file_paths[author] = file_paths
    return author_to_file_paths


def get_all_module_nodes():
    file_paths = get_all_file_paths()
    fh = FileHierarchy(file_paths)
    mapping = sort_dict_per_value(fh.get_components_to_num_files_map())
    # module: folders with more than MINIMUM_FILES_IN_MODULE files and not repeated (pairwise intersection = 0)
    mapping_refined = {}

    def result_includes_path(path):
        for key in mapping_refined.keys():
            if path in key:
                return True
        return False
    for path in mapping:
        if mapping[path] > MINIMUM_FILES_IN_MODULE and not result_includes_path(path):
            mapping_refined[path] = mapping[path]

    module_nodes = []
    for path in mapping_refined:
        module_nodes.append(Node(NodeType.MODULE, path))
    return module_nodes


def get_all_contributor_nodes():
    return list(map(lambda name: Node(NodeType.CONTRIBUTOR, name), author_to_commits.keys()))


def get_all_nodes():
    return get_all_module_nodes() + get_all_contributor_nodes()


def get_all_edges(author_to_file_paths, module_nodes, contributor_nodes):
    # TODO: add num files changed in a module
    edges = []
    def num_files_changed_in_this_module(changed_file_paths, module_name):
        counter = 0
        for file_path in changed_file_paths:
            if module_name in file_path:
                counter = counter + 1
        return counter
    for module_node in module_nodes:
        for author in author_to_file_paths:
            changed_file_paths_by_this_author = author_to_file_paths[author]
            num = num_files_changed_in_this_module(changed_file_paths_by_this_author, module_node.name)
            if num > 0:
                src = Node.get_node_by_name(contributor_nodes, author)
                edges.append(Edge(src, module_node, num))
    return edges


atfp = get_author_to_file_paths()
module_nodes = get_all_module_nodes()
contributor_nodes = get_all_contributor_nodes()

### TODO: Nader: Below you can find all nodes and edges needed for visualization

# Edges
all_edges = get_all_edges(atfp, module_nodes, contributor_nodes)

# Nodes
all_nodes = get_all_nodes()
contributor_nodes = get_all_contributor_nodes()
module_nodes = get_all_module_nodes()
