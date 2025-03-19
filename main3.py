import pygame
import random
import time
import heapq

# Initialize display settings
display_size = 600
node_size = 20
edge_width = 3
color = (0, 255, 0)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode([display_size, display_size])
pygame.display.set_caption('Network Graph')

nodes = []
edges = []
node_cap = 20

def generate_nodes():
    for _ in range(node_cap):
        x, y = random.randint(0, display_size - node_size), random.randint(0, display_size - node_size)
        nodes.append((x + node_size // 2, y + node_size // 2))

def generate_edges():
    for i in range(node_cap):
        for j in range(i + 1, node_cap):
            weight = random.randint(1, 20)  # Assign a random weight
            edges.append((weight, nodes[i], nodes[j]))

def draw_graph():
    screen.fill(black)
    for _, node_a, node_b in edges:
        pygame.draw.line(screen, color, node_a, node_b, edge_width)
    for node in nodes:
        pygame.draw.rect(screen, color, (*node, node_size, node_size))
    pygame.display.update()

def kruskal():
    edges_sorted = sorted(edges, key=lambda x: x[0])  # Sort by weight
    parent = {node: node for node in nodes}
    
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]
    
    def union(node1, node2):
        root1, root2 = find(node1), find(node2)
        if root1 != root2:
            parent[root2] = root1
    
    mst = []
    for weight, node_a, node_b in edges_sorted:
        if find(node_a) != find(node_b):
            union(node_a, node_b)
            mst.append((weight, node_a, node_b))
    return mst

def prim():
    start = nodes[0]
    visited = set([start])
    min_heap = [(weight, start, neighbor) for weight, start, neighbor in edges if start == nodes[0] or neighbor == nodes[0]]
    heapq.heapify(min_heap)
    
    mst = []
    while min_heap and len(visited) < node_cap:
        weight, node_a, node_b = heapq.heappop(min_heap)
        if node_b not in visited:
            visited.add(node_b)
            mst.append((weight, node_a, node_b))
            for edge in edges:
                if edge[1] == node_b and edge[2] not in visited:
                    heapq.heappush(min_heap, edge)
    return mst

# Generate graph
generate_nodes()
generate_edges()
draw_graph()

# Measure algorithm performance
start_time = time.time()
kruskal_mst = kruskal()
kruskal_time = time.time() - start_time

start_time = time.time()
prim_mst = prim()
prim_time = time.time() - start_time

print(f"Kruskal's Algorithm Time: {kruskal_time:.6f} seconds")
print(f"Prim's Algorithm Time: {prim_time:.6f} seconds")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()