import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec
import os

categories = [
    ("Characters", [(i, f"n{i}") for i in range(1, 10)]),
    ("Circles", [(i+10, f"c{i}") for i in range(1, 10)]),
    ("Bamboo", [(i+20, f"b{i}") for i in range(1, 10)]),
    ("Winds", [(31, "w1", "North"), (32, "w2", "East"), 
               (33, "w3", "South"), (34, "w4", "West")]),
    ("Dragons", [(41, "d1", "White"), (42, "d2", "Green"), 
                (43, "d3", "Red")]),
    ("Flowers", [(i+50, f"f{j}") for j, i in enumerate(range(1, 5), 1)]),
    ("Seasons", [(i+60, f"s{j}") for j, i in enumerate(range(1, 5), 1)])
]

fig = plt.figure(figsize=(20, 3*len(categories)))
gs = GridSpec(len(categories), 11)

for row, (category_name, tiles) in enumerate(categories):
    # Add rotated category label in the first column
    ax_label = plt.subplot(gs[row, 0])
    ax_label.text(0.5, 0.5, category_name, 
                 rotation=90, 
                 fontsize=16, 
                 fontweight='bold',
                 ha='center',
                 va='center')
    ax_label.axis('off')
    
    # Add tiles
    for idx, tile_info in enumerate(tiles):
        tile_id = tile_info[0]
        shorthand = tile_info[1]
        
        # Create subplot for this tile, starting from second column
        ax = plt.subplot(gs[row, idx + 1])
        
        # Load and display tile image
        img = mpimg.imread(os.path.join('tiles', f"{shorthand}.png"))
        plt.imshow(img)
        
        # Add tile information as text below
        plt.text(0.5, -0.2, f"ID: {tile_id}\nSHORT: {shorthand}", 
                ha='center', transform=ax.transAxes)
            
        plt.axis('off')

plt.tight_layout()
plt.savefig('tile_reference.png', bbox_inches='tight', dpi=300)