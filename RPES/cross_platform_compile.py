#!/usr/bin/env python3
import os
import platform
import subprocess
import shutil

def compile_multiplet():
    """Compile the multiplet executable for the current platform"""
    
    print(f"Detected platform: {platform.system()}")
    
    # Create src directory if needed
    os.makedirs("src", exist_ok=True)
    
    # Change to the src directory
    os.chdir("src")
    
    # Check which platform we're on
    if platform.system() == "Darwin":  # macOS
        print("Compiling for macOS...")
        # macOS-specific compilation
        subprocess.run("gfortran -c labla.f", shell=True, check=True)
        subprocess.run("gcc -c *.c", shell=True, check=True)
        subprocess.run("gfortran *.o -o multiplet -framework Accelerate", shell=True, check=True)
    
    elif platform.system() == "Linux":
        print("Compiling for Linux...")
        # Linux-specific compilation
        subprocess.run("gfortran -c labla.f", shell=True, check=True)
        subprocess.run("gcc -c *.c", shell=True, check=True)
        subprocess.run("gfortran *.o -o multiplet -lblas -llapack", shell=True, check=True)
    
    elif platform.system() == "Windows":
        print("Compiling for Windows...")
        # Windows-specific compilation (requires MinGW or similar)
        # Note: This is just a placeholder, actual Windows compilation may need more work
        subprocess.run("gfortran -c labla.f", shell=True, check=True)
        subprocess.run("gcc -c *.c", shell=True, check=True)
        subprocess.run("gfortran *.o -o multiplet.exe -lblas -llapack", shell=True, check=True)
    
    else:
        print(f"Unsupported platform: {platform.system()}")
        return False
    
    # Copy the compiled executable to the parent directory
    print("Copying multiplet executable to parent directory...")
    if platform.system() == "Windows":
        shutil.copy("multiplet.exe", "..")
    else:
        shutil.copy("multiplet", "..")
    
    # Go back to the original directory
    os.chdir("..")
    
    return True

if __name__ == "__main__":
    success = compile_multiplet()
    if success:
        print("Compilation successful!")
    else:
        print("Compilation failed.") 