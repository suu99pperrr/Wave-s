import discord
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import aiohttp
import io
import math
import random
import colorsys

# Bot configuration
intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)

# Welcome channel name
WELCOME_CHANNEL = 'wlc'

@bot.event
async def on_ready():
    print(f'{bot.user} is ready! 🌊')

@bot.event
async def on_member_join(member):
    """Welcome new members with an ultra custom image"""
    
    welcome_channel = discord.utils.get(member.guild.channels, name=WELCOME_CHANNEL)
    
    if not welcome_channel:
        print(f"Welcome channel '{WELCOME_CHANNEL}' not found!")
        return
    
    try:
        # Create ultra custom welcome image
        welcome_image = await create_epic_welcome_image(member)
        
        # Epic welcome messages (random)
        welcome_messages = [
            f"🌊 **TSUNAMI ALERT!** {member.mention} just crashed into our server! Welcome aboard! 🏄‍♂️",
            f"⚡ **WAVE RIDER DETECTED!** {member.mention} has surfed into our community! Cowabunga! 🌊",
            f"🔥 **SPLASH!** {member.mention} just made the biggest wave! Welcome to paradise! 🏝️",
            f"💎 **LEGENDARY SURFER!** {member.mention} has joined the crew! Ride the waves! 🌊✨",
            f"🚀 **TIDAL WAVE INCOMING!** {member.mention} just dropped in! Welcome to the zone! 🌊"
        ]
        
        message = random.choice(welcome_messages)
        
        if welcome_image:
            file = discord.File(welcome_image, filename="epic_welcome.png")
            await welcome_channel.send(message, file=file)
        else:
            await welcome_channel.send(message)
            
    except Exception as e:
        print(f"Error: {e}")
        await welcome_channel.send(f"🌊 Welcome {member.mention}! 🌊")

async def create_epic_welcome_image(member):
    """Create an absolutely EPIC welcome image"""
    try:
        width, height = 1000, 500
        
        # Create base image with dynamic gradient
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Epic animated-style gradient background
        for y in range(height):
            # Multi-color gradient with wave influence
            wave_influence = math.sin(y * 0.02) * 20
            
            # Calculate color based on position
            hue = (240 + wave_influence) / 360  # Blue to purple range
            saturation = 0.8 + (y / height) * 0.2
            lightness = 0.3 + (y / height) * 0.4
            
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            color = tuple(int(c * 255) for c in rgb)
            
            draw.rectangle([(0, y), (width, y + 1)], fill=color)
        
        # Add particle effects
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 8)
            alpha = random.randint(100, 255)
            
            # Create star-like particles
            particle_color = (255, 255, 255, alpha)
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            particle_draw = ImageDraw.Draw(overlay)
            particle_draw.ellipse([x - size, y - size, x + size, y + size], fill=particle_color)
            
            # Convert overlay to RGB and blend
            particle_rgb = Image.new('RGB', (width, height), (255, 255, 255))
            particle_rgb.paste(overlay, (0, 0), overlay)
            img = Image.blend(img, particle_rgb, alpha / 255 * 0.3)
        
        # Draw EPIC cartoon waves with multiple layers
        wave_layers = [
            {'y_base': height - 60, 'amplitude': 40, 'frequency': 0.015, 'color': (0, 191, 255, 200)},
            {'y_base': height - 100, 'amplitude': 30, 'frequency': 0.02, 'color': (30, 144, 255, 150)},
            {'y_base': height - 140, 'amplitude': 25, 'frequency': 0.025, 'color': (65, 105, 225, 100)},
        ]
        
        for wave in wave_layers:
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            wave_draw = ImageDraw.Draw(overlay)
            
            points = []
            for x in range(0, width + 20, 3):
                y = wave['y_base'] + int(wave['amplitude'] * math.sin(x * wave['frequency']))
                points.append((x, y))
            
            # Close the wave shape
            points.extend([(width, height), (0, height)])
            wave_draw.polygon(points, fill=wave['color'])
            
            # Convert to RGB and paste
            wave_rgb = Image.new('RGB', (width, height))
            wave_rgb.paste(img, (0, 0))
            wave_rgb.paste(overlay, (0, 0), overlay)
            img = wave_rgb
        
        # Add foam/splash effects
        foam_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        foam_draw = ImageDraw.Draw(foam_overlay)
        
        for i in range(20):
            x = random.randint(50, width - 50)
            y = random.randint(height - 150, height - 50)
            size = random.randint(5, 20)
            foam_draw.ellipse([x - size, y - size, x + size, y + size], 
                            fill=(255, 255, 255, random.randint(80, 150)))
        
        img.paste(foam_overlay, (0, 0), foam_overlay)
        
        # Get and process user avatar
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.url)) as resp:
                if resp.status == 200:
                    avatar_data = await resp.read()
                    avatar = Image.open(io.BytesIO(avatar_data))
                    
                    # Epic avatar processing
                    avatar_size = 150
                    avatar = avatar.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
                    
                    # Create epic circular mask with glow effect
                    mask_size = avatar_size + 20
                    mask = Image.new('L', (mask_size, mask_size), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    
                    # Multiple circles for glow effect
                    for i in range(10, 0, -1):
                        alpha = int(255 * (1 - i / 10) * 0.3)
                        circle_size = avatar_size + i * 2
                        x_offset = (mask_size - circle_size) // 2
                        mask_draw.ellipse([x_offset, x_offset, 
                                         x_offset + circle_size, x_offset + circle_size], 
                                        fill=alpha)
                    
                    # Main avatar circle
                    center = mask_size // 2
                    mask_draw.ellipse([center - avatar_size//2, center - avatar_size//2,
                                     center + avatar_size//2, center + avatar_size//2], 
                                    fill=255)
                    
                    # Create glowing avatar
                    glow_avatar = Image.new('RGBA', (mask_size, mask_size), (0, 0, 0, 0))
                    
                    # Add rainbow glow border
                    glow_draw = ImageDraw.Draw(glow_avatar)
                    for i in range(8):
                        hue = i / 8
                        rgb = colorsys.hls_to_rgb(hue, 0.5, 1.0)
                        color = tuple(int(c * 255) for c in rgb) + (100,)
                        
                        border_thickness = 8 - i
                        glow_draw.ellipse([center - avatar_size//2 - border_thickness, 
                                         center - avatar_size//2 - border_thickness,
                                         center + avatar_size//2 + border_thickness, 
                                         center + avatar_size//2 + border_thickness], 
                                        outline=color, width=2)
                    
                    # Paste resized avatar
                    avatar_resized = Image.new('RGBA', (mask_size, mask_size), (0, 0, 0, 0))
                    avatar_x = (mask_size - avatar_size) // 2
                    avatar_resized.paste(avatar, (avatar_x, avatar_x))
                    avatar_resized.putalpha(mask)
                    
                    # Combine glow and avatar
                    final_avatar = Image.alpha_composite(glow_avatar, avatar_resized)
                    
                    # Paste on main image
                    avatar_pos_x = (width - mask_size) // 2
                    avatar_pos_y = 30
                    img.paste(final_avatar, (avatar_pos_x, avatar_pos_y), final_avatar)
        
        # EPIC text with multiple effects
        try:
            font_title = ImageFont.truetype("arial.ttf", 60)
            font_subtitle = ImageFont.truetype("arial.ttf", 32)
            font_small = ImageFont.truetype("arial.ttf", 20)
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Main welcome text with rainbow effect
        welcome_text = f"WELCOME {member.display_name.upper()}!"
        text_x = width // 2
        text_y = 280
        
        # Rainbow text effect
        if font_title:
            text_width = draw.textlength(welcome_text, font=font_title)
            start_x = text_x - text_width // 2
            
            char_x = start_x
            for i, char in enumerate(welcome_text):
                hue = (i * 30) % 360
                rgb = colorsys.hls_to_rgb(hue / 360, 0.7, 1.0)
                color = tuple(int(c * 255) for c in rgb)
                
                # Text shadow
                for offset in [(-3, -3), (-3, 3), (3, -3), (3, 3)]:
                    draw.text((char_x + offset[0], text_y + offset[1]), char, 
                             font=font_title, fill=(0, 0, 0))
                
                # Rainbow character
                draw.text((char_x, text_y), char, font=font_title, fill=color)
                char_x += draw.textlength(char, font=font_title)
        
        # Subtitle with glow
        if font_subtitle:
            subtitle = "🌊 DIVE INTO THE ADVENTURE! 🌊"
            
            # Glow effect
            for radius in range(5, 0, -1):
                alpha = int(100 * (6 - radius) / 5)
                glow_color = (0, 255, 255, alpha)
                
                for angle in range(0, 360, 30):
                    offset_x = int(radius * math.cos(math.radians(angle)))
                    offset_y = int(radius * math.sin(math.radians(angle)))
                    
                    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    overlay_draw = ImageDraw.Draw(overlay)
                    overlay_draw.text((text_x + offset_x, text_y + 80 + offset_y), 
                                    subtitle, font=font_subtitle, fill=glow_color, anchor="mm")
                    
                    img_rgba = img.convert('RGBA')
                    img_rgba = Image.alpha_composite(img_rgba, overlay)
                    img = img_rgba.convert('RGB')
            
            # Main subtitle text
            draw = ImageDraw.Draw(img)
            draw.text((text_x, text_y + 80), subtitle, font=font_subtitle, 
                     fill=(255, 255, 255), anchor="mm")
        
        # Add member count with epic styling
        if font_small:
            member_count = f"MEMBER #{len(member.guild.members)} HAS ARRIVED!"
            
            # Metallic effect
            for offset_y in range(3):
                shade = 150 + offset_y * 35
                draw.text((text_x, text_y + 140 + offset_y), member_count, 
                         font=font_small, fill=(shade, shade, 0), anchor="mm")
            
            draw.text((text_x, text_y + 140), member_count, 
                     font=font_small, fill=(255, 255, 100), anchor="mm")
        
        # Add decorative elements
        # Lightning bolts
        lightning_points = [
            [(100, 100), (120, 150), (110, 150), (130, 200)],
            [(870, 120), (850, 170), (860, 170), (840, 220)],
        ]
        
        for lightning in lightning_points:
            # Glow effect
            for thickness in range(8, 0, -1):
                alpha = int(50 * (9 - thickness) / 8)
                overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.polygon(lightning, outline=(255, 255, 0, alpha), width=thickness)
                
                img_rgba = img.convert('RGBA')
                img_rgba = Image.alpha_composite(img_rgba, overlay)
                img = img_rgba.convert('RGB')
            
            # Main lightning
            draw = ImageDraw.Draw(img)
            draw.polygon(lightning, outline=(255, 255, 255), width=3)
            draw.polygon(lightning, fill=(255, 255, 0))
        
        # Animated-style sparkles
        sparkle_positions = [
            (150, 80), (200, 60), (800, 90), (750, 70),
            (120, 300), (880, 320), (50, 250), (950, 280)
        ]
        
        for x, y in sparkle_positions:
            # Draw sparkle
            sparkle_size = random.randint(8, 15)
            sparkle_color = (255, 255, 255)
            
            # Four-pointed star
            points = [
                (x, y - sparkle_size),  # top
                (x + 3, y - 3),
                (x + sparkle_size, y),  # right
                (x + 3, y + 3),
                (x, y + sparkle_size),  # bottom
                (x - 3, y + 3),
                (x - sparkle_size, y),  # left
                (x - 3, y - 3)
            ]
            
            # Glow
            for glow_size in range(5, 0, -1):
                glow_alpha = int(80 * (6 - glow_size) / 5)
                overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                
                glow_points = [(px + random.randint(-glow_size, glow_size), 
                               py + random.randint(-glow_size, glow_size)) for px, py in points]
                overlay_draw.polygon(glow_points, fill=(255, 255, 255, glow_alpha))
                
                img_rgba = img.convert('RGBA')
                img_rgba = Image.alpha_composite(img_rgba, overlay)
                img = img_rgba.convert('RGB')
            
            # Main sparkle
            draw = ImageDraw.Draw(img)
            draw.polygon(points, fill=sparkle_color)
        
        # Epic wave patterns with transparency
        for wave_layer in range(3):
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            wave_draw = ImageDraw.Draw(overlay)
            
            wave_y = height - 80 - (wave_layer * 40)
            wave_amplitude = 50 - (wave_layer * 10)
            wave_frequency = 0.01 + (wave_layer * 0.005)
            wave_phase = wave_layer * 100
            
            # Create wave path
            points = []
            for x in range(0, width + 30, 2):
                y = wave_y + int(wave_amplitude * math.sin((x + wave_phase) * wave_frequency))
                points.append((x, y))
            
            # Add foam caps on waves
            foam_points = []
            for i in range(0, len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                # Add foam where wave peaks
                if i > 0 and i < len(points) - 1:
                    prev_y = points[i - 1][1]
                    next_y = points[i + 1][1]
                    
                    if y1 < prev_y and y1 < next_y:  # Wave peak
                        foam_points.extend([
                            (x1 - 10, y1 - 5),
                            (x1 + 10, y1 - 5),
                            (x1 + 15, y1 + 5),
                            (x1 - 15, y1 + 5)
                        ])
            
            # Close wave shape
            points.extend([(width, height), (0, height)])
            
            # Wave colors with transparency
            wave_colors = [
                (0, 255, 255, 120),    # Cyan
                (30, 144, 255, 100),   # Dodger blue  
                (65, 105, 225, 80)     # Royal blue
            ]
            
            wave_draw.polygon(points, fill=wave_colors[wave_layer])
            
            # Add foam
            if foam_points:
                for i in range(0, len(foam_points), 4):
                    if i + 3 < len(foam_points):
                        foam_quad = foam_points[i:i+4]
                        wave_draw.polygon(foam_quad, fill=(255, 255, 255, 200))
            
            # Blend wave layer
            img_rgba = img.convert('RGBA')
            img = Image.alpha_composite(img_rgba, overlay).convert('RGB')
        
        # Get user avatar with EPIC processing
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.url)) as resp:
                if resp.status == 200:
                    avatar_data = await resp.read()
                    avatar = Image.open(io.BytesIO(avatar_data))
                    
                    # Epic avatar size
                    avatar_size = 180
                    avatar = avatar.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
                    
                    # Create epic border with multiple rings
                    border_size = avatar_size + 40
                    border_img = Image.new('RGBA', (border_size, border_size), (0, 0, 0, 0))
                    border_draw = ImageDraw.Draw(border_img)
                    
                    # Multiple colorful rings
                    ring_colors = [
                        (255, 0, 255, 200),   # Magenta
                        (0, 255, 255, 180),   # Cyan
                        (255, 255, 0, 160),   # Yellow
                        (255, 255, 255, 220)  # White
                    ]
                    
                    for i, color in enumerate(ring_colors):
                        ring_thickness = 3
                        ring_radius = avatar_size // 2 + 10 + (i * 5)
                        center = border_size // 2
                        
                        border_draw.ellipse([center - ring_radius, center - ring_radius,
                                           center + ring_radius, center + ring_radius], 
                                          outline=color, width=ring_thickness)
                    
                    # Create circular avatar
                    mask = Image.new('L', (avatar_size, avatar_size), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
                    
                    circular_avatar = Image.new('RGBA', (avatar_size, avatar_size), (0, 0, 0, 0))
                    circular_avatar.paste(avatar, (0, 0))
                    circular_avatar.putalpha(mask)
                    
                    # Position avatar in border
                    avatar_offset = (border_size - avatar_size) // 2
                    border_img.paste(circular_avatar, (avatar_offset, avatar_offset), circular_avatar)
                    
                    # Paste final avatar on main image
                    final_x = (width - border_size) // 2
                    final_y = 40
                    
                    img_rgba = img.convert('RGBA')
                    img_rgba.paste(border_img, (final_x, final_y), border_img)
                    img = img_rgba.convert('RGB')
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG', quality=95)
        img_bytes.seek(0)
        
        return img_bytes
        
    except Exception as e:
        print(f"Error creating epic welcome image: {e}")
        return None

# Run the bot
# ... rest of your bot code above ...

# Run the bot
if __name__ == "__main__":
    import os
    bot.run(os.getenv('TOKEN'))
