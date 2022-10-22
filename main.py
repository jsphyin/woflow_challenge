import requests

response = requests.get('https://nodes-on-nodes-challenge.herokuapp.com/nodes/089ef556-dfff-4ff2-9733-654645be56fe')

ID_KEY = "id"
CHILD_NODE_KEY = 'child_node_ids'


def request_node_info(id='089ef556-dfff-4ff2-9733-654645be56fe'):
    return requests.get(f'https://nodes-on-nodes-challenge.herokuapp.com/nodes/{id}')


def is_invalid_node(node_info):
    return ID_KEY not in node_info or CHILD_NODE_KEY not in node_info


def traverse_nodes(node_info):
    queue = [node_info]
    seen = set()

    while queue:
        node = queue.pop(0)
        if is_invalid_node(node):
            print(f"Invalid node with data {node}")
            continue
        if node[ID_KEY] in seen:
            continue

        seen.add(node[ID_KEY])

        if node[CHILD_NODE_KEY]:
            children_ids = ','.join(node[CHILD_NODE_KEY])

            child_response = request_node_info(id=children_ids).json()

            for child in child_response:
                queue.append(child)
    return seen


def main():
    node_response = request_node_info().json()
    if len(node_response) != 1:
        print("Initial node response returned more than one node")
    initial_node_info = node_response[0]
    print(traverse_nodes(initial_node_info))


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
