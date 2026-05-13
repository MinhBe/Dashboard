import sys
import json
import os
from vsdx import VisioFile

class VisioBuilderPro:
    def __init__(self, template_path):
        self.template_path = template_path
        self.vis = VisioFile(template_path)
        
    def find_shape_pro(self, shape_id):
        for page in self.vis.pages:
            shape = page.find_shape_by_id(shape_id)
            if shape: return shape
        return None

    def build(self, topology, output_path):
        page = self.vis.get_page(0)
        # Clear existing page content or use a new page
        # For simplicity, we'll place shapes in a clean area
        
        device_map = topology.get("device_map", {})
        created_shapes = {}
        
        # ZONE MAPPING
        # Partition A (Left: X=1 to 5)
        # Partition B (Right: X=7 to 11)
        # Layers: ISP(Y=10), FW(Y=8), DNS/F5(Y=6), Servers(Y=4)
        
        zones = {
            "A": {"x_start": 1.0, "width": 4.0},
            "B": {"x_start": 6.5, "width": 4.0}
        }
        
        layers = {
            "isp": 10.0,
            "firewall": 8.0,
            "f5": 6.0,
            "dns": 6.0,
            "server": 4.0,
            "default": 2.0
        }

        devices = topology.get("devices", [])
        for dev in devices:
            name = dev["name"]
            dtype = dev.get("type", "default")
            zone_id = "A" if "Partition A" in name else "B"
            
            # 1. Get Master Shape
            master_id = device_map.get(dtype)
            template_shape = self.find_shape_pro(master_id)
            if not template_shape:
                print(f"Warning: Master {master_id} not found. Fallback to basic.")
                template_shape = page.child_shapes[0]
            
            # 2. Copy to current page
            new_shape = template_shape.copy(page)
            
            # 3. Calculate Position
            x = zones[zone_id]["x_start"] + (zones[zone_id]["width"] / 2)
            y = layers.get(dtype, layers["default"])
            
            # Adjust if multiple devices in same zone/layer
            existing_in_spot = [s for s in created_shapes.values() if abs(s.x - x) < 0.5 and abs(s.y - y) < 0.5]
            if existing_in_spot:
                x += 1.5 * len(existing_in_spot)
            
            # MOVE LOGIC: vsdx move() is relative to current center
            dx = x - new_shape.x
            dy = y - new_shape.y
            new_shape.move(dx, dy)
            
            # 4. Set Text
            new_shape.text = name
            created_shapes[name] = new_shape
            print(f"Placed '{name}' at ({x}, {y})")

        # Connection Logic (Placeholder - actual vsdx connectors are complex)
        # We will add visual markers or simple lines if possible in next iteration
        
        self.vis.save_vsdx(output_path)
        print(f"\n✅ DONE: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            topo = json.load(f)
        builder = VisioBuilderPro(topo["template"])
        builder.build(topo, topo["output"])
