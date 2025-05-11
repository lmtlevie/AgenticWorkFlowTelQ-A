#!/bin/bash

# Script to run the example conversation

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Function to install requirements with pip
install_with_pip() {
    echo "Installing with pip..."
    # Pre-install tokenizers to avoid Rust compilation issues
    pip install tokenizers --no-build-isolation
    # Now install camel-ai and other requirements
    pip install -r requirements.txt
    touch venv/.requirements_installed
}

# Function to install from GitHub source
install_from_source() {
    echo "Installing camel-ai from source..."
    # Clone the repository
    git clone https://github.com/camel-ai/camel.git camel-repo
    cd camel-repo
    # Install the package in development mode
    pip install -e .
    cd ..
    # Install other dependencies
    pip install accelerate einops
    touch venv/.requirements_installed
}

# Function to install with conda (if available)
install_with_conda() {
    if command -v conda >/dev/null 2>&1; then
        echo "Installing with conda..."
        conda install -c conda-forge tokenizers
        pip install -r requirements.txt
        touch venv/.requirements_installed
    else
        echo "Conda not found, skipping this method."
        return 1
    fi
}

# Install requirements if needed
if [ ! -f "venv/.requirements_installed" ]; then
    echo "Installing requirements..."
    echo "Attempting installation method 1: Using pip with pre-installed tokenizers"
    install_with_pip && echo "Installation successful!" || {
        echo "Method 1 failed. Trying method 2: Installing from source"
        install_from_source && echo "Installation successful!" || {
            echo "Method 2 failed. Trying method 3: Using conda (if available)"
            install_with_conda && echo "Installation successful!" || {
                echo "All installation methods failed. Please try manually:"
                echo "1. Install Rust toolchain: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
                echo "2. Install camel-ai via: pip install camel-ai --no-build-isolation"
                exit 1
            }
        }
    }
fi

# Run the example script
echo "Running example script..."
python example_mock.py

echo "Done! Check the outputs directory for the generated conversation." 