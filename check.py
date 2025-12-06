# Checksum validation script for viva
import checksumdir
import os

# Get current directory (your project folder)
folder_name = "."

print("\n" + "="*50)
print("CHECKSUM VALIDATION FOR VIVA")
print("="*50)
print(f"\nChecking folder: {os.getcwd()}")

try:
    hash = checksumdir.dirhash(folder_name)
    print(f"\n✅ Checksum calculated successfully!")
    print(f"📊 Directory Checksum: {hash}")
    print("\n" + "="*50)
    print("Show this checksum to proctor!")
    print("="*50)
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure you're in the project folder!")
    print("Run: cd \"C:\\hosipital final\"")
    print("Then: py check.py")
