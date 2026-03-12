import time
import threading
import platform
import argparse
import subprocess
import sys
import select

DEFAULT_WORK_MINUTES = 25
DEFAULT_SHORT_BREAK_MINUTES = 5
DEFAULT_LONG_BREAK_MINUTES = 25
SESSIONS_BEFORE_LONG_BREAK = 4


def play_sound(sound_type="beep"):
    try:
        system = platform.system().lower()
        if system == "linux":
            try:
                subprocess.run(
                    ["aplay", "-q", "/usr/share/sounds/alsa/Front_Left.wav"],
                    capture_output=True, timeout=2,
                )
            except Exception:
                pass
            beeps = {"start": 2, "end": 4}.get(sound_type, 1)
            for _ in range(beeps):
                print('\a', end='', flush=True)
                time.sleep(0.2)
        elif system == "windows":
            try:
                import winsound
                winsound.MessageBeep(
                    winsound.MB_ICONEXCLAMATION if sound_type == "end" else winsound.MB_OK
                )
            except ImportError:
                print('\a', end='', flush=True)
        else:
            print('\a', end='', flush=True)
    except Exception:
        print('\a', end='', flush=True)


def send_notification(title, message):
    try:
        system = platform.system().lower()
        if system == "linux":
            subprocess.run(["notify-send", "-t", "5000", title, message],
                           capture_output=True, timeout=3)
        elif system == "darwin":
            subprocess.run(
                ["osascript", "-e",
                 f'display notification "{message}" with title "{title}"'],
                capture_output=True, timeout=3,
            )
    except Exception:
        pass


work_frames = [
    r"""
       🍅
     (\_/)
     ( •_•)
     / >🍵   Focusing...
    """,
    r"""
       🍅
     (\_/)
     ( •_•)👉
     / > 🍵  Deep work...
    """,
    r"""
       🍅
     (\_/)
     ( •o•)
     / > 🍵  Oops!
    """,
    r"""
       🍅
     (\_/)
     ( -_-) zzz
     / > 🍵  Napping...
    """,
    r"""
       🍅
     (\_/)
     ( •_•)☕
     / > 📖  Coffee!
    """,
    r"""
       🍅
     (\_/)✨
     ( •‿•)
     / >🍰   Almost done!
    """,
]

break_frames = [
    r"""
       ☕
     (\_/)
     ( -_-) zzz
     / > 🛋️   Resting...
    """,
    r"""
       ☕
     (\_/)
     ( •‿•)
     / > 🍪   Snack time!
    """,
    r"""
       ☕
     (\_/)
     ( ^_^)
     / > 📱   Scroll away
    """,
    r"""
       ☕
     (\_/)
     ( •o•)
     / > 🚶   Short walk
    """,
    r"""
       ☕
     (\_/)✨
     ( •_•)
     / > 💧   Stay hydrated
    """,
    r"""
       ☕
     (\_/)
     ( >_<)
     / > ⏰   Almost back!
    """,
]


def get_color(percent, is_break):
    if is_break:
        if percent <= 0.25: return "\033[96m"
        elif percent <= 0.50: return "\033[92m"
        elif percent <= 0.75: return "\033[93m"
        else: return "\033[91m"
    else:
        if percent <= 0.25: return "\033[91m"
        elif percent <= 0.50: return "\033[93m"
        elif percent <= 0.75: return "\033[94m"
        else: return "\033[92m"


def get_quote(percent_display, is_break):
    if is_break:
        if percent_display <= 25: return "💬 Time to relax! 😌"
        elif percent_display <= 50: return "💬 Enjoy your break! 🛋️"
        elif percent_display <= 75: return "💬 Almost done resting... 🕐"
        else: return "💬 Back to work soon! 🔔"
    else:
        if percent_display <= 25: return "💬 Focus, focus, focus! 🎯"
        elif percent_display <= 50: return "💬 Keep it up, champ! 🦝💪"
        elif percent_display <= 75: return "💬 Almost there! 🚀"
        else: return "💬 Final stretch! You've got this! 🤘"


def show_animation(stop_event, total_seconds, session_num, is_break=False):
    frame_index = 0
    tick = 0
    bar_length = 30
    start_time = time.time()
    current_frames = break_frames if is_break else work_frames

    while not stop_event.is_set():
        elapsed = time.time() - start_time
        remaining = max(0.0, total_seconds - elapsed)
        percent = min(elapsed / total_seconds, 1.0)
        filled = int(bar_length * percent)
        percent_display = int(percent * 100)

        color = get_color(percent, is_break)
        bar = f"{color}{'█' * filled}\033[0m" + "-" * (bar_length - filled)
        quote = get_quote(percent_display, is_break)
        mins, secs = divmod(int(remaining), 60)
        label = "Break" if is_break else f"Session {session_num}"

        print("\033c", end="")
        print(current_frames[frame_index % len(current_frames)])
        print(f"  {label}")
        print(f"  [{bar}] {percent_display}%")
        print(f"  ⏱  {mins:02}:{secs:02} remaining")
        print(f"  {quote}")
        hint = "skip break" if is_break else "end session early"
        print(f"\n  [Press Enter to {hint}]")

        time.sleep(1)
        tick += 1
        if tick % 5 == 0:
            frame_index += 1


def check_for_enter(timeout):
    """Return True if Enter is pressed before timeout, False otherwise."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        ready, _, _ = select.select([sys.stdin], [], [], 0.5)
        if ready:
            sys.stdin.readline()
            return True
    return False


def run_timer(duration, session_num=1, is_break=False):
    stop_event = threading.Event()
    anim_thread = threading.Thread(
        target=show_animation,
        args=(stop_event, duration, session_num, is_break),
        daemon=True,
    )
    anim_thread.start()
    try:
        check_for_enter(duration)
    except KeyboardInterrupt:
        raise
    finally:
        stop_event.set()
        anim_thread.join()


def main_menu(work_mins, short_break_mins, long_break_mins):
    session_count = 0

    while True:
        in_cycle = session_count % SESSIONS_BEFORE_LONG_BREAK
        dots = "🍅" * in_cycle + "○" * (SESSIONS_BEFORE_LONG_BREAK - in_cycle)

        print("\033c", end="")
        print(f"  🦝 Pomodoro Raccoon 🍅\n")
        print(f"  Progress: {dots}  ({session_count} completed)")
        print(f"\n  1. Start Pomodoro    ({work_mins} min)")
        print(f"  2. Short break       ({short_break_mins} min)")
        print(f"  3. Long break        ({long_break_mins} min)")
        print(f"  4. Exit")

        choice = input("\n  Choice: ").strip()

        if choice == '1':
            try:
                print("\n  🦝 Starting in...")
                for n in range(3, 0, -1):
                    print(f"  {n}...")
                    time.sleep(1)
                play_sound("start")

                run_timer(work_mins * 60, session_num=session_count + 1)
                session_count += 1

                play_sound("end")
                send_notification("🍅 Pomodoro Complete!",
                                  f"Session {session_count} done. Time for a break!")

                is_long = session_count % SESSIONS_BEFORE_LONG_BREAK == 0
                break_label = "long" if is_long else "short"
                break_dur = long_break_mins if is_long else short_break_mins

                print("\033c", end="")
                print(f"\n  🎉 Session {session_count} complete!")
                if is_long:
                    print(f"  You've earned a long break ({break_dur} min)! 🎊")
                else:
                    print(f"  Time for a short break ({break_dur} min).")

                ans = input(f"\n  Start {break_label} break? [Y/n]: ").strip().lower()
                if ans != 'n':
                    play_sound("start")
                    run_timer(break_dur * 60, session_num=session_count, is_break=True)
                    play_sound("end")
                    send_notification("⏰ Break Over!", "Time to get back to work! 🦝")

            except KeyboardInterrupt:
                print("\n\n  [Session interrupted]")
                time.sleep(1)

        elif choice == '2':
            try:
                play_sound("start")
                run_timer(short_break_mins * 60, is_break=True)
                play_sound("end")
            except KeyboardInterrupt:
                print("\n\n  [Break interrupted]")
                time.sleep(1)

        elif choice == '3':
            try:
                play_sound("start")
                run_timer(long_break_mins * 60, is_break=True)
                play_sound("end")
            except KeyboardInterrupt:
                print("\n\n  [Break interrupted]")
                time.sleep(1)

        elif choice == '4':
            print(f"\n  Goodbye! 👋  ({session_count} sessions completed)\n")
            break


def main():
    parser = argparse.ArgumentParser(description="Pomodoro Raccoon - CLI Pomodoro timer 🦝")
    parser.add_argument("--work", type=int, default=DEFAULT_WORK_MINUTES,
                        metavar="MIN", help=f"Work duration in minutes (default: {DEFAULT_WORK_MINUTES})")
    parser.add_argument("--short-break", type=int, default=DEFAULT_SHORT_BREAK_MINUTES,
                        metavar="MIN", help=f"Short break in minutes (default: {DEFAULT_SHORT_BREAK_MINUTES})")
    parser.add_argument("--long-break", type=int, default=DEFAULT_LONG_BREAK_MINUTES,
                        metavar="MIN", help=f"Long break in minutes (default: {DEFAULT_LONG_BREAK_MINUTES})")
    args = parser.parse_args()
    main_menu(args.work, args.short_break, args.long_break)


if __name__ == "__main__":
    main()
