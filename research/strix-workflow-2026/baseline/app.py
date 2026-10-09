"""Invented vulnerable code for a bounded Strix installation smoke test."""
import subprocess

def greet(name):
    return subprocess.check_output("echo hello " + name, shell=True, text=True)

if __name__ == "__main__":
    print(greet("world"))
