from collections import defaultdict
import heapq
import requests

ID_KEY = "id"
CHILD_NODE_KEY = 'child_node_ids'


def request_node_info(id='089ef556-dfff-4ff2-9733-654645be56fe'):
    return requests.get(f'https://nodes-on-nodes-challenge.herokuapp.com/nodes/{id}')


def is_invalid_node(node_info):
    return ID_KEY not in node_info or CHILD_NODE_KEY not in node_info


def get_children_node_info(children_nodes):
    children_ids = ','.join(children_nodes)

    return request_node_info(id=children_ids).json()


def traverse_nodes(node_info):
    queue = [node_info]
    node_dict = defaultdict(int)

    while queue:
        node = queue.pop(0)
        if is_invalid_node(node):
            print(f"Invalid node with data {node}")
            continue

        node_id = node[ID_KEY]
        node_dict[node_id] += 1

        if node[CHILD_NODE_KEY]:
            child_response = get_children_node_info(node[CHILD_NODE_KEY])

            for child in child_response:
                if is_invalid_node(child):
                    print(f"Invalid child node with data {child}")
                    continue
                child_id = child[ID_KEY]
                if child_id in node_dict:
                    node_dict[child_id] += 1
                    continue
                queue.append(child)
    return node_dict


def find_most_common_node(nodes_dict):
    heap = []

    for key in nodes_dict:
        heapq.heappush(heap, (nodes_dict[key] * -1, key))

    return heap[0]


def main():
    node_response = request_node_info().json()
    if len(node_response) != 1:
        print("Initial node response returned more than one node")
        return
    initial_node_info = node_response[0]
    nodes_dict = traverse_nodes(initial_node_info)
    most_common_node_occurrences, most_common_node_id = find_most_common_node(nodes_dict)

    print(f"Total number of unique nodes is {len(nodes_dict.keys())}")
    print(f"Most common node id is {most_common_node_id} with {most_common_node_occurrences * -1} occurrences")


if __name__ == "__main__":
    main()
