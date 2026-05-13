import sys
import json
import os
from vsdx import VisioFile

class VisioGenerator:
    def __init__(self, template_path):
        self.template_path = template_path
        self.vis = VisioFile(template_path)
        
    def generate(self, topology, output_path):
        # Create a new page or use the first one
        page = self.vis.get_page(0)
        
        # Mapping of device types to "example" shape IDs from the template
        # We can detect these dynamically or have them pre-defined
        device_map = topology.get("device_map", {})
        
        created_shapes = {}
        
        # Default layout: Grid
        spacing_x = 2.0
        spacing_y = 2.0
        cols = topology.get("layout", {}).get("cols", 4)
        
        for i, device in enumerate(topology.get("devices", [])):
            name = device["name"]
            dtype = device.get("type", "default")
            
            # Find a template shape for this type
            template_shape_id = device_map.get(dtype)
            if not template_shape_id:
                # Fallback to the first shape on the page if no map provided
                template_shape = page.child_shapes[0]
            else:
                template_shape = page.find_shape_by_id(template_shape_id)
            
            # Copy shape
            new_shape = template_shape.copy(page)
            
            # Calculate position
            row = i // cols
            col = i % cols
            x = col * spacing_x + 1.0
            y = page.height - (row * spacing_y + 1.0)
            
            new_shape.move(x - new_shape.x, y - new_shape.y)
            new_shape.text = name
            
            created_shapes[name] = new_shape
            
        # Add connections
        for conn in topology.get("connections", []):
            src_name = conn["from"]
            dst_name = conn["to"]
            if src_name in created_shapes and dst_name in created_shapes:
                # vsdx library Page.add_connect is for existing connectors
                # This part is tricky in vsdx 0.6.1, might need a template connector
                pass
                
        self.vis.save_vsdx(output_path)
        print(f"Successfully generated Visio file: {output_path}")

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        if sys.argv[1] == "--analyze" and len(sys.argv) > 2:
            file_path = sys.argv[2]
            with VisioFile(file_path) as vis:
                for page in vis.pages:
                    print(f"\nPage: {page.name}")
                    for shape in page.child_shapes:
                        text = shape.text.strip() if shape.text else "No text"
                        print(f"  Shape ID={shape.ID} (Text: {text})")
        else:
            with open(sys.argv[1], 'r') as f:
                topo = json.load(f)
            gen = VisioGenerator(topo["template"])
            gen.generate(topo, topo["output"])
