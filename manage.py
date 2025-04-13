import os
import sys
import subprocess
import socket


def is_redis_running(host="127.0.0.1", port=6379):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def start_redis():
    redis_path = r"C:\Users\kamil\Downloads\Redis-x64-3.2.100"
    exe_path = os.path.join(redis_path, "redis-server.exe")

    if not is_redis_running():
        try:
            subprocess.Popen([exe_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Redis server spuštěn.")
        except FileNotFoundError:
            print("redis-server.exe nebyl nalezen na zadané cestě.")
    else:
        print("Redis už běží.")


def start_celery_beat():
    try:
        subprocess.Popen(["celery", "-A", "kamiladmin", "beat", "--loglevel=info"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Celery Beat spuštěn.")
    except FileNotFoundError:
        print("Celery (beat) není dostupné v PATH. Zkontroluj virtuální prostředí.")


def start_celery_worker():
    try:
        subprocess.Popen(["celery", "-A", "kamiladmin", "worker", "--pool=solo", "--loglevel=info"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Celery Worker spuštěn.")
    except FileNotFoundError:
        print("Celery (worker) není dostupné v PATH. Zkontroluj virtuální prostředí.")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kamiladmin.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # start_redis()
    # start_celery_beat()
    # start_celery_worker()

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
