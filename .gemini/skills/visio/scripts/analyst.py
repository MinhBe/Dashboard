import sys
import os
from vsdx import VisioFile

def deep_analyze(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found {file_path}")
        return

    with VisioFile(file_path) as vis:
        print(f"--- Báo cáo phân tích hệ thống mạng: {os.path.basename(file_path)} ---\n")
        
        # Toàn bộ thiết bị phát hiện được
        all_devices = []
        
        for page in vis.pages:
            print(f"PHÂN VÙNG: {page.name}")
            
            # Phân loại thiết bị
            inventory = {
                "Firewalls": [],
                "Switches": [],
                "Load Balancers (F5)": [],
                "Servers/Hosts": [],
                "External (ISP/Cloud)": [],
                "Others": []
            }
            
            # Truy vết kết nối
            connections = []
            
            shapes = page.all_shapes
            for shape in shapes:
                text = shape.text.strip() if shape.text else ""
                clean_text = text.lower()
                
                device_info = {
                    "ID": shape.ID,
                    "Name": text if text else f"Unknown-{shape.ID}",
                    "Type": shape.shape_type,
                    "MasterID": shape.master_shape_ID
                }
                
                # Logic nhận diện dựa trên keyword
                if any(k in clean_text for k in ["firewall", "fw", "forti", "sophos", "ngfw"]):
                    inventory["Firewalls"].append(device_info)
                elif any(k in clean_text for k in ["switch", "sw", "ex3400", "ex4300", "core"]):
                    inventory["Switches"].append(device_info)
                elif "f5" in clean_text or "big-ip" in clean_text or "waf" in clean_text:
                    inventory["Load Balancers (F5)"].append(device_info)
                elif any(k in clean_text for k in ["server", "db", "app", "esxi", "poweredge"]):
                    inventory["Servers/Hosts"].append(device_info)
                elif any(k in clean_text for k in ["isp", "internet", "wan", "cmc", "vnpt", "cloud"]):
                    inventory["External (ISP/Cloud)"].append(device_info)
                elif text:
                    inventory["Others"].append(device_info)

            # Xuất kết quả phân loại
            for category, items in inventory.items():
                if items:
                    print(f"  [{category}]")
                    for item in items:
                        print(f"    - {item['Name']} (ID: {item['ID']})")
            
            # Ghi chú về kết nối
            print(f"  [Connectivity]: Phát hiện {len(page.connects)} điểm nối kết.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        deep_analyze(sys.argv[1])
    else:
        print("Usage: python analyst.py <path_to_vsdx>")
