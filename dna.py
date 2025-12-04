import os
import sys
import time
import math
import random
import platform
import hashlib
from datetime import datetime

class DNAAnimator:
    def __init__(self):
        self.os_type = platform.system()
        self.setup_hardware_seed()
        self.cycle_count = 0
        self.clear_interval = 50
        self.char, self.distro_name = self.get_os_info()
        
    def setup_hardware_seed(self):
        """(1) Auto-Randomizer Seed Based on Hardware"""
        hardware_id = f"{platform.processor()}{platform.machine()}{os.uname().nodename}"
        seed_value = int(hashlib.md5(hardware_id.encode()).hexdigest(), 16)
        random.seed(seed_value % (2**32))
        
    def get_brightness(self):
        """(2) Auto-Brightness Control based on time"""
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 12:  # Morning
            brightness = 0.8
        elif 12 <= current_hour < 18:  # Afternoon (brightest)
            brightness = 1.0
        elif 18 <= current_hour < 22:  # Evening
            brightness = 0.6
        else:  # Night
            brightness = 0.3
        
        return brightness
    
    def adjust_intensity(self, brightness):
        """Adjust character intensity based on brightness"""
        if brightness >= 0.9:
            return self.char
        elif brightness >= 0.6:
            return '○'
        else:
            return '·'
    
    def get_os_info(self):
        """(4) OS-Adaptive Animation Character - Linux Distributors"""
        distro_name = "Linux"
        char = '●'
        
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
                
                if 'ubuntu' in os_info:
                    distro_name = "Ubuntu"
                    char = '◉'
                elif 'fedora' in os_info:
                    distro_name = "Fedora"
                    char = '◆'
                elif 'debian' in os_info:
                    distro_name = "Debian"
                    char = '◎'
                elif 'arch' in os_info:
                    distro_name = "Arch"
                    char = '⬢'
                elif 'centos' in os_info:
                    distro_name = "CentOS"
                    char = '⬟'
                elif 'opensuse' in os_info:
                    distro_name = "openSUSE"
                    char = '◈'
                elif 'alpine' in os_info:
                    distro_name = "Alpine"
                    char = '△'
                elif 'manjaro' in os_info:
                    distro_name = "Manjaro"
                    char = '⬡'
        except:
            pass
        
        return char, distro_name
    
    def clear_terminal(self):
        """(3) Auto-clear terminal every X cycles"""
        self.cycle_count += 1
        if self.cycle_count % self.clear_interval == 0:
            os.system('cls' if self.os_type == "Windows" else 'clear')
            sys.stdout.write('\033[H\033[J')
            sys.stdout.flush()
    
    def generate_dna_frame(self, frame_num):
        """Generate a single frame of DNA animation"""
        width = 60
        height = 15
        brightness = self.get_brightness()
        char = self.adjust_intensity(brightness)
        
        frame = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Single DNA helix - vertical animation
        center_y = height // 2
        
        for i in range(width):
            # Left strand
            y1 = center_y + math.sin((i + frame_num) * 0.2) * 4
            
            # Right strand (opposite phase)
            y2 = center_y + math.cos((i + frame_num) * 0.2) * 4
            
            # Draw left strand
            if 0 <= int(y1) < height and 0 <= i < width:
                frame[int(y1)][i] = char
            
            # Draw right strand
            if 0 <= int(y2) < height and 0 <= i < width:
                frame[int(y2)][i] = char
            
            # Draw connecting bonds
            if int(y1) != int(y2):
                min_y = min(int(y1), int(y2))
                max_y = max(int(y1), int(y2))
                for y in range(min_y + 1, max_y):
                    if 0 <= y < height:
                        frame[y][i] = '-'
        
        return [''.join(row) for row in frame]
    
    def run(self):
        """Main animation loop"""
        frame_num = 0
        os.system('cls' if self.os_type == "Windows" else 'clear')
        try:
            while True:
                frame = self.generate_dna_frame(frame_num)
                
                # Display frame with info
                brightness = self.get_brightness()
                
                # Use cursor positioning to update in place
                sys.stdout.write('\033[H')  # Move cursor to top
                print(f"Brightness: {brightness:.0%} | Frame: {frame_num:4d} | OS: {self.distro_name}\n")
                
                for line in frame:
                    print(line)
                
                print(f"\nPress Ctrl+C to stop")
                sys.stdout.flush()
                
                time.sleep(0.1)
                frame_num += 1
                
        except KeyboardInterrupt:
            os.system('cls' if self.os_type == "Windows" else 'clear')
            print("\nDNA Animation stopped. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    animator = DNAAnimator()
    animator.run()