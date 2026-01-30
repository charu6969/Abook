"""
Settings Panels for ABook
WiFi, Battery, Time configuration panels
All grayscale theme
"""

import pygame
from config import *
import datetime


class SettingsPanel:
    """Base class for settings panels"""
    
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        self.panel_rect = None
        self.close_btn = None
        
    def draw_panel_background(self, screen, title, width=400, height=500):
        """Draw standard panel background"""
        # Center on screen
        x = (600 - width) // 2
        y = (1024 - height) // 2
        
        self.panel_rect = pygame.Rect(x, y, width, height)
        
        # Background with shadow effect
        shadow = pygame.Rect(x + 5, y + 5, width, height)
        pygame.draw.rect(screen, (100, 100, 100), shadow, border_radius=10)
        pygame.draw.rect(screen, (240, 240, 240), self.panel_rect, border_radius=10)
        pygame.draw.rect(screen, (150, 150, 150), self.panel_rect, 2, border_radius=10)
        
        # Title bar
        title_rect = pygame.Rect(x, y, width, 50)
        pygame.draw.rect(screen, (200, 200, 200), title_rect, border_radius=10)
        pygame.draw.line(screen, (150, 150, 150), 
                        (x, y + 50), (x + width, y + 50), 2)
        
        # Title text
        title_text = self.font_l.render(title, True, COLOR_BLACK)
        screen.blit(title_text, (x + 15, y + 12))
        
        # Close button (X)
        self.close_btn = pygame.Rect(x + width - 40, y + 10, 30, 30)
        pygame.draw.rect(screen, (220, 220, 220), self.close_btn, border_radius=5)
        pygame.draw.line(screen, COLOR_BLACK,
                        (self.close_btn.left + 8, self.close_btn.top + 8),
                        (self.close_btn.right - 8, self.close_btn.bottom - 8), 2)
        pygame.draw.line(screen, COLOR_BLACK,
                        (self.close_btn.right - 8, self.close_btn.top + 8),
                        (self.close_btn.left + 8, self.close_btn.bottom - 8), 2)
        
        return x, y


class WiFiPanel(SettingsPanel):
    """WiFi settings panel"""
    
    def __init__(self, fonts):
        super().__init__(fonts)
        self.wifi_enabled = True
        self.networks = [
            {"name": "Home WiFi", "strength": 4, "secured": True, "connected": True},
            {"name": "JSS University", "strength": 3, "secured": True, "connected": False},
            {"name": "Public WiFi", "strength": 2, "secured": False, "connected": False},
        ]
        self.network_btns = []
        self.toggle_btn = None
        
    def draw(self, screen):
        """Draw WiFi settings panel"""
        x, y = self.draw_panel_background(screen, "WiFi Settings")
        
        content_y = y + 70
        
        # WiFi toggle
        toggle_y = content_y
        toggle_label = self.font_m.render("WiFi", True, COLOR_BLACK)
        screen.blit(toggle_label, (x + 20, toggle_y))
        
        # Toggle switch (grayscale)
        self.toggle_btn = pygame.Rect(x + 320, toggle_y, 60, 30)
        if self.wifi_enabled:
            pygame.draw.rect(screen, (80, 80, 80), self.toggle_btn, border_radius=15)
            # Switch knob (ON - right side)
            knob_x = self.toggle_btn.right - 32
            pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.toggle_btn.centery), 12)
        else:
            pygame.draw.rect(screen, (180, 180, 180), self.toggle_btn, border_radius=15)
            # Switch knob (OFF - left side)
            knob_x = self.toggle_btn.left + 17
            pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.toggle_btn.centery), 12)
        
        # Available networks (if enabled)
        if self.wifi_enabled:
            networks_y = content_y + 60
            networks_label = self.font_m.render("Available Networks", True, COLOR_BLACK)
            screen.blit(networks_label, (x + 20, networks_y))
            
            self.network_btns = []
            btn_y = networks_y + 40
            
            for network in self.networks:
                # Network button
                btn = pygame.Rect(x + 20, btn_y, 360, 50)
                
                # Highlight if connected
                if network['connected']:
                    pygame.draw.rect(screen, (200, 200, 200), btn, border_radius=8)
                    pygame.draw.rect(screen, (100, 100, 100), btn, 2, border_radius=8)
                else:
                    pygame.draw.rect(screen, (230, 230, 230), btn, border_radius=8)
                    pygame.draw.rect(screen, (180, 180, 180), btn, 1, border_radius=8)
                
                # Network name
                name_text = self.font_m.render(network['name'], True, COLOR_BLACK)
                screen.blit(name_text, (btn.x + 45, btn.y + 10))
                
                # Signal strength bars (grayscale)
                bar_x = btn.x + 10
                bar_y = btn.centery
                for i in range(4):
                    bar_height = 5 + (i * 4)
                    bar_color = (50, 50, 50) if i < network['strength'] else (200, 200, 200)
                    pygame.draw.rect(screen, bar_color,
                                   (bar_x + i * 6, bar_y - bar_height, 4, bar_height))
                
                # Lock icon if secured
                if network['secured']:
                    lock_x = btn.right - 30
                    lock_y = btn.centery - 8
                    pygame.draw.rect(screen, (100, 100, 100),
                                   (lock_x, lock_y + 5, 12, 10), 1)
                    pygame.draw.arc(screen, (100, 100, 100),
                                  (lock_x - 2, lock_y, 16, 12), 0, 3.14, 2)
                
                # Connected indicator
                if network['connected']:
                    conn_text = self.font_s.render("Connected", True, (80, 80, 80))
                    screen.blit(conn_text, (btn.x + 45, btn.y + 30))
                
                self.network_btns.append((btn, network))
                btn_y += 60
        else:
            # WiFi disabled message
            disabled_text = self.font_m.render("WiFi is disabled", True, (150, 150, 150))
            screen.blit(disabled_text, (x + 20, content_y + 60))
    
    def handle_click(self, pos):
        """Handle clicks in WiFi panel"""
        if self.close_btn and self.close_btn.collidepoint(pos):
            return ('close_wifi', None)
        
        if self.toggle_btn and self.toggle_btn.collidepoint(pos):
            self.wifi_enabled = not self.wifi_enabled
            return ('toggle_wifi', self.wifi_enabled)
        
        if self.wifi_enabled and self.network_btns:
            for btn, network in self.network_btns:
                if btn.collidepoint(pos):
                    return ('connect_network', network['name'])
        
        return (None, None)


class BatteryPanel(SettingsPanel):
    """Battery/Power settings panel"""
    
    def __init__(self, fonts):
        super().__init__(fonts)
        self.battery_level = 85
        self.charging = False
        self.power_save_mode = False
        self.power_save_btn = None
        
    def draw(self, screen):
        """Draw battery settings panel"""
        x, y = self.draw_panel_background(screen, "Battery & Power", width=400, height=400)
        
        content_y = y + 70
        
        # Battery visualization (large)
        battery_x = x + 150
        battery_y = content_y + 20
        
        # Battery body
        body_rect = pygame.Rect(battery_x, battery_y, 100, 50)
        pygame.draw.rect(screen, (200, 200, 200), body_rect, border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100), body_rect, 2, border_radius=5)
        
        # Battery terminal
        terminal_rect = pygame.Rect(battery_x + 100, battery_y + 15, 8, 20)
        pygame.draw.rect(screen, (100, 100, 100), terminal_rect)
        
        # Battery level fill
        fill_width = int(95 * (self.battery_level / 100))
        fill_rect = pygame.Rect(battery_x + 3, battery_y + 3, fill_width, 44)
        
        # Color based on level
        if self.battery_level > 50:
            fill_color = (100, 100, 100)
        elif self.battery_level > 20:
            fill_color = (120, 120, 120)
        else:
            fill_color = (150, 150, 150)
        
        pygame.draw.rect(screen, fill_color, fill_rect, border_radius=3)
        
        # Percentage text
        percent_text = self.font_l.render(f"{self.battery_level}%", True, COLOR_BLACK)
        screen.blit(percent_text, (battery_x + 25, battery_y + 70))
        
        # Charging status
        if self.charging:
            status_text = self.font_m.render("Charging", True, (80, 80, 80))
        else:
            status_text = self.font_m.render("Not Charging", True, (150, 150, 150))
        screen.blit(status_text, (battery_x - 10, battery_y + 105))
        
        # Power save mode toggle
        toggle_y = content_y + 170
        label = self.font_m.render("Power Save Mode", True, COLOR_BLACK)
        screen.blit(label, (x + 20, toggle_y))
        
        # Toggle switch
        self.power_save_btn = pygame.Rect(x + 280, toggle_y, 60, 30)
        if self.power_save_mode:
            pygame.draw.rect(screen, (80, 80, 80), self.power_save_btn, border_radius=15)
            knob_x = self.power_save_btn.right - 32
            pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.power_save_btn.centery), 12)
        else:
            pygame.draw.rect(screen, (180, 180, 180), self.power_save_btn, border_radius=15)
            knob_x = self.power_save_btn.left + 17
            pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.power_save_btn.centery), 12)
        
        # Battery info
        info_y = toggle_y + 60
        info_texts = [
            f"Time remaining: ~{int(self.battery_level / 10)} hours",
            f"Last charged: 2 hours ago",
            f"Battery health: Good"
        ]
        
        for i, text in enumerate(info_texts):
            info = self.font_s.render(text, True, (100, 100, 100))
            screen.blit(info, (x + 20, info_y + i * 25))
    
    def handle_click(self, pos):
        """Handle clicks in battery panel"""
        if self.close_btn and self.close_btn.collidepoint(pos):
            return ('close_battery', None)
        
        if self.power_save_btn and self.power_save_btn.collidepoint(pos):
            self.power_save_mode = not self.power_save_mode
            return ('toggle_power_save', self.power_save_mode)
        
        return (None, None)


class TimePanel(SettingsPanel):
    """Time & Date settings panel"""
    
    def __init__(self, fonts):
        super().__init__(fonts)
        self.format_24h = True
        self.format_btn = None
        
    def draw(self, screen):
        """Draw time settings panel"""
        x, y = self.draw_panel_background(screen, "Time & Date", width=400, height=450)
        
        content_y = y + 70
        
        # Current time (large)
        now = datetime.datetime.now()
        if self.format_24h:
            time_str = now.strftime("%H:%M:%S")
        else:
            time_str = now.strftime("%I:%M:%S %p")
        
        time_text = self.font_l.render(time_str, True, COLOR_BLACK)
        time_x = x + (400 - time_text.get_width()) // 2
        screen.blit(time_text, (time_x, content_y))
        
        # Current date
        date_str = now.strftime("%A, %B %d, %Y")
        date_text = self.font_m.render(date_str, True, (100, 100, 100))
        date_x = x + (400 - date_text.get_width()) // 2
        screen.blit(date_text, (date_x, content_y + 45))
        
        # Time format toggle
        toggle_y = content_y + 110
        label = self.font_m.render("24-Hour Format", True, COLOR_BLACK)
        screen.blit(label, (x + 20, toggle_y))
        
        # Toggle switch
        self.format_btn = pygame.Rect(x + 280, toggle_y, 60, 30)
        if self.format_24h:
            pygame.draw.rect(screen, (80, 80, 80), self.format_btn, border_radius=15)
            knob_x = self.format_btn.right - 32
            pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.format_btn.centery), 12)
        else:
            pygame.draw.rect(screen, (180, 180, 180), self.format_btn, border_radius=15)
            knob_x = self.format_btn.left + 17
            pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.format_btn.centery), 12)
        
        # Timezone info
        info_y = toggle_y + 60
        timezone_label = self.font_m.render("Timezone", True, COLOR_BLACK)
        screen.blit(timezone_label, (x + 20, info_y))
        
        timezone_value = self.font_m.render("Asia/Kolkata (IST)", True, (100, 100, 100))
        screen.blit(timezone_value, (x + 20, info_y + 30))
        
        # Auto sync
        sync_y = info_y + 80
        sync_label = self.font_s.render("Automatically sync time from internet", True, (100, 100, 100))
        screen.blit(sync_label, (x + 20, sync_y))
        
        # Alarm info (placeholder)
        alarm_y = sync_y + 50
        alarm_text = self.font_m.render("Alarms & Reminders", True, COLOR_BLACK)
        screen.blit(alarm_text, (x + 20, alarm_y))
        
        no_alarms = self.font_s.render("No alarms set", True, (150, 150, 150))
        screen.blit(no_alarms, (x + 20, alarm_y + 30))
    
    def handle_click(self, pos):
        """Handle clicks in time panel"""
        if self.close_btn and self.close_btn.collidepoint(pos):
            return ('close_time', None)
        
        if self.format_btn and self.format_btn.collidepoint(pos):
            self.format_24h = not self.format_24h
            return ('toggle_time_format', self.format_24h)
        
        return (None, None)