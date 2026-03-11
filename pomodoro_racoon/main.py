import time
import threading
import os
import platform

# Timer settings
work_duration = 25 * 60  # 25 minutes
break_duration = 5 * 60  # 5 minutes break

# Control flag
is_running = False

def play_sound(sound_type="beep"):
    """
    Spielt einen Signalton ab - funktioniert auf Linux und Windows
    sound_type: "beep" für einfachen Piep, "start" für Timer-Start, "end" für Timer-Ende
    """
    try:
        system = platform.system().lower()
        
        if sound_type == "start":
            # Drei kurze Pieptöne für Start
            for _ in range(3):
                print('\a', end='', flush=True)
                time.sleep(0.2)
        elif sound_type == "end":
            # Längerer Signalton für Ende
            for _ in range(5):
                print('\a', end='', flush=True)
                time.sleep(0.3)
        else:
            # Einfacher Piep
            print('\a', end='', flush=True)
            
        # Zusätzliche plattformspezifische Sounds
        if system == "linux":
            try:
                # Versuche pactl (PulseAudio) für einen Signalton
                os.system("pactl upload-sample /usr/share/sounds/alsa/Front_Left.wav bell >/dev/null 2>&1")
                os.system("pactl play-sample bell >/dev/null 2>&1")
            except:
                pass
        elif system == "windows":
            try:
                import winsound
                if sound_type == "start":
                    winsound.MessageBeep(winsound.MB_OK)
                elif sound_type == "end":
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                else:
                    winsound.MessageBeep()
            except ImportError:
                pass
                
    except Exception:
        # Fallback: Einfacher ASCII-Bell
        print('\a', end='', flush=True)

# ASCII frames (Waschbär mit Tomato)
frames = [
    r"""
       🍅
     (\_/)  
     ( •_•)
     / >🍵   Fokus...
    """,
    r"""
       🍅
     (\_/)  
     ( •_•)👉
     / > 🍵  Umblättern...
    """,
    r"""
       🍅
     (\_/)  
     ( •o•)
     / > 🍵  Ups!
    """,
    r"""
       🍅
     (\_/)  
     ( -_-) zzz
     / > 🍵  Nap...
    """,
    r"""
       🍅
     (\_/)  
     ( •_•)☕
     / > 📖  Kaffee!
    """,
    r"""
       🍅
     (\_/)✨
     ( •‿•)
     / >🍰   Geschafft!
    """
]

# Pause frames (Waschbär in der Pause)
break_frames = [
    r"""
       ☕
     (\_/)  
     ( -_-) zzz
     / > 🛋️   Entspannen...
    """,
    r"""
       ☕
     (\_/)  
     ( •‿•)
     / > 🍪   Snack-Zeit!
    """,
    r"""
       ☕
     (\_/)  
     ( ^_^)
     / > 📱   Social Media
    """,
    r"""
       ☕
     (\_/)  
     ( •o•)
     / > 🚶   Kurzer Walk
    """,
    r"""
       ☕
     (\_/)✨
     ( •_•)
     / > 💧   Wasser trinken
    """,
    r"""
       ☕
     (\_/)  
     ( >_<)
     / > ⏰   Gleich weiter!
    """
]

def show_animation(stop_event, total_seconds, is_break=False):
    frame_index = 0
    progress_bar_length = 30
    elapsed = 0
    
    # Wähle richtige Frames basierend auf Timer-Typ
    current_frames = break_frames if is_break else frames

    while not stop_event.is_set() and elapsed <= total_seconds:
        percent = elapsed / total_seconds
        filled = int(progress_bar_length * percent)
        
        # Farbige Progress Bar - für Pause andere Farben
        if is_break:
            # Pause: Entspannende Farben
            if percent <= 0.25:  # 0-25%: Blau (entspannend)
                filled_bar = f"\033[96m{'█' * filled}\033[0m"  # Cyan
            elif percent <= 0.50:  # 25-50%: Grün (erholsam)
                filled_bar = f"\033[92m{'█' * filled}\033[0m"  # Grün
            elif percent <= 0.75:  # 50-75%: Gelb (Warnung)
                filled_bar = f"\033[93m{'█' * filled}\033[0m"  # Gelb
            else:  # 75-100%: Orange (bald zurück zur Arbeit)
                filled_bar = f"\033[91m{'█' * filled}\033[0m"  # Rot
        else:
            # Arbeit: Original Farben
            if percent <= 0.25:  # 0-25%: Rot
                filled_bar = f"\033[91m{'█' * filled}\033[0m"  # Rot
            elif percent <= 0.50:  # 25-50%: Gelb
                filled_bar = f"\033[93m{'█' * filled}\033[0m"  # Gelb
            elif percent <= 0.75:  # 50-75%: Blau
                filled_bar = f"\033[94m{'█' * filled}\033[0m"  # Blau
            else:  # 75-100%: Grün
                filled_bar = f"\033[92m{'█' * filled}\033[0m"  # Grün
            
        bar = filled_bar + "-" * (progress_bar_length - filled)
        percent_display = int(percent * 100)

        # Select motivational message basierend auf Timer-Typ
        if is_break:
            if percent_display <= 25:
                quote = "💬 Zeit zum Entspannen! 😌"
            elif percent_display <= 50:
                quote = "💬 Gönn dir die Pause! 🛋️"
            elif percent_display <= 75:
                quote = "💬 Noch etwas Zeit... 🕐"
            elif percent_display < 100:
                quote = "💬 Gleich geht's weiter! 🔔"
            else:
                quote = "💬 Pause vorbei! Let's go! 🚀"
        else:
            if percent_display <= 25:
                quote = "💬 Fokus, Fokus, Fokus! 🎯"
            elif percent_display <= 50:
                quote = "💬 Weiter so, Champ! 🦝💪"
            elif percent_display <= 75:
                quote = "💬 Gleich geschafft! 🚀"
            elif percent_display < 100:
                quote = "💬 Endspurt! Du rockst das! 🤘"
            else:
                quote = "💬 BOOM! Geschafft! 🎉"

        # Clear screen + print frame
        print("\033c", end="")  # works on most terminals
        print(current_frames[frame_index % len(current_frames)])
        print(f"[{bar}] {percent_display}%")
        print(quote)

        time.sleep(10)  # Geändert von 2 auf 10 Sekunden
        elapsed += 10   # Geändert von 2 auf 10 Sekunden
        frame_index += 1

def start_break_timer():
    global is_running
    is_running = True
    stop_event = threading.Event()
    
    print("🛋️ Pausentimer startet in 3 Sekunden...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1) 
    print("1...")
    time.sleep(1)
    print("☕ PAUSE GESTARTET! ☕")
    play_sound("start")  # Signalton beim Pause-Start

    # Start break animation thread
    anim_thread = threading.Thread(target=show_animation, args=(stop_event, break_duration, True))
    anim_thread.start()

    try:
        for remaining in range(break_duration, 0, -1):
            if not is_running:
                break
            mins, secs = divmod(remaining, 60)
            print(f"Break time left: {mins:02}:{secs:02}", end="\r")
            time.sleep(1)
        if is_running:
            print("\n🔔 Pause ist vorbei! Zurück an die Arbeit! 🔔🍅")
            play_sound("end")  # Signalton beim Pause-Ende
    except KeyboardInterrupt:
        print("\n[!] Pausentimer unterbrochen.")
    finally:
        is_running = False
        stop_event.set()
        anim_thread.join()
        
        # Bildschirm leeren vor Rückkehr zum Hauptmenü
        time.sleep(2)  # Kurze Pause um die Nachricht zu lesen
        print("\033c", end="")  # Clear screen

def start_pomodoro_timer():
    global is_running
    is_running = True
    stop_event = threading.Event()
    
    print("🦝 Timer startet in 3 Sekunden...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1) 
    print("1...")
    time.sleep(1)
    print("🍅 POMODORO GESTARTET! 🍅")
    play_sound("start")  # Signalton beim Start

    # Start animation thread
    anim_thread = threading.Thread(target=show_animation, args=(stop_event, work_duration, False))
    anim_thread.start()

    try:
        for remaining in range(work_duration, 0, -1):
            if not is_running:
                break
            mins, secs = divmod(remaining, 60)
            print(f"Time left: {mins:02}:{secs:02}", end="\r")
            time.sleep(1)
        if is_running:
            print("\n🎉 Arbeitszeit ist um! Nimm dir eine 5-Minuten-Pause! 🎉🍅")
            play_sound("end")  # Signalton beim Ende
            
            # Automatisch Pausentimer starten
            time.sleep(2)  # Kurze Pause zwischen den Timern
            start_break_timer()  # Automatischer Pausentimer
            
    except KeyboardInterrupt:
        print("\n[!] Timer unterbrochen.")
    finally:
        is_running = False
        stop_event.set()
        anim_thread.join()
        # Bildschirm leeren vor Rückkehr zum Hauptmenü  
        print("\033c", end="")  # Clear screen
        print("Zurück zum Hauptmenü...\n")

def main_menu():
    while True:
        print("\nWelcome to the Pomodoro Timer! 🦝🍅")
        print("1. Start Pomodoro Timer")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            start_pomodoro_timer()
        elif choice == '2':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
