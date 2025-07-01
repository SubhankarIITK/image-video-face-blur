#!/usr/bin/env python3
"""
Setup script for Face Blur Application
Creates necessary directories and installs dependencies
"""

import os
import subprocess
import sys

def create_directories():
    """Create necessary directories for the application"""
    directories = [
        'static',
        'static/uploads', 
        'static/results',
        'templates',
        'utils'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def install_dependencies():
    """Install required Python packages"""
    try:
        print("📦 Installing dependencies from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def create_init_files():
    """Create __init__.py files for packages"""
    init_files = [
        'utils/__init__.py'
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Package initialization file\n')
            print(f"✅ Created: {init_file}")

def main():
    """Main setup function"""
    print("🚀 Setting up Face Blur Application...")
    print("=" * 50)
    
    # Create directories
    print("📁 Creating directories...")
    create_directories()
    
    # Create init files
    print("\n📄 Creating package files...")
    create_init_files()
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if install_dependencies():
        print("\n✅ Setup completed successfully!")
        print("\n🎯 Next steps:")
        print("   1. Run: python app.py")
        print("   2. Open: http://localhost:5000")
        print("   3. Upload an image or video to test!")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()