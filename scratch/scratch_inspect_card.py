import json

with open("blinkit_sample_state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

# Let's inspect objects in state that have 'Amul Taaza Toned Milk'
def find_nodes_with_text(obj, target="Amul Taaza Toned Milk"):
    nodes = []
    if isinstance(obj, dict):
        txt = json.dumps(obj)
        if target in txt:
            # check if it's the specific product card object
            if 'identity' in obj and 'name' in obj:
                nodes.append(obj)
            else:
                for k, v in obj.items():
                    nodes.extend(find_nodes_with_text(v, target))
    elif isinstance(obj, list):
        for item in obj:
            nodes.extend(find_nodes_with_text(item, target))
    return nodes

nodes = find_nodes_with_text(state)
print("Nodes found:", len(nodes))
if nodes:
    print(json.dumps(nodes[0], indent=2))
