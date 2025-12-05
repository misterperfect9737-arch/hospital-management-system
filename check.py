# Checksum script for viva validation
import checksumdir
import os

def find_project_folder():
    """Find the project folder automatically"""
    current_dir = os.getcwd()
    
    # Check current directory first
    if os.path.exists("app.py") and os.path.exists("models.py"):
        return "."
    
    return None

def main():
    print("\n" + "="*50)
    print("CHECKSUM VALIDATION FOR VIVA")
    print("="*50)
    
    folder_name = find_project_folder()
    
    if folder_name is None:
        print("\n❌ Project folder not found!")
        folder_name = input("\nEnter folder name manually: ")
        if not folder_name:
            print("No folder name provided. Exiting.")
            return
    
    if not os.path.exists(folder_name):
        print(f"\n❌ Folder '{folder_name}' not found!")
        return
    
    print(f"\n📁 Checking folder: {folder_name}")
    
    try:
        # Calculate checksum
        hash_value = checksumdir.dirhash(folder_name)
        
        print(f"\n✅ Checksum calculated successfully!")
        print(f"📊 Directory Checksum: {hash_value}")
        
        # Check required files
        required_files = ["app.py", "models.py", "routes.py", "requirements.txt"]
        missing_files = []
        
        for file in required_files:
            file_path = os.path.join(folder_name, file)
            if not os.path.exists(file_path):
                missing_files.append(file)
        
        if missing_files:
            print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        else:
            print(f"\n✅ All required files present")
        
        print("\n" + "="*50)
        print("READY FOR VIVA!")
        print("="*50)
        print("\nNext steps:")
        print("1. Show this checksum to proctor")
        print("2. Run: pip install -r requirements.txt")
        print("3. Run: python app.py")
        print("4. Open: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nInstall: pip install checksumdir")

if __name__ == "__main__":
    main()
