#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def reorganize_structure(root_dir):
    """Reorganizes the repository structure to fix import issues"""
    root = Path(root_dir)
    
    # 1. Create proper Python package structure
    package_dir = root / "phindllama"
    package_dir.mkdir(exist_ok=True)
    
    # 2. Move core components into package
    components = [
        ('app/api', 'phindllama/api'),
        ('app/contracts', 'phindllama/contracts'),
        ('app/economics', 'phindllama/economics'),
        ('app/hooks', 'phindllama/hooks'),
        ('app/infrastructure', 'phindllama/infrastructure'),
        ('app/models', 'phindllama/models'),
        ('app/wallet', 'phindllama/wallet'),
        ('src/agents', 'phindllama/agents'),
        ('src/config', 'phindllama/config'),
        ('src/core', 'phindllama/core'),
        ('src/monitoring', 'phindllama/monitoring'),
        ('src/scripts', 'phindllama/scripts'),
        ('src/utils', 'phindllama/utils')
    ]
    
    for src, dst in components:
        src_path = root / src
        dst_path = root / dst
        if src_path.exists():
            shutil.move(str(src_path), str(dst_path))
    
    # 3. Clean up empty directories
    empty_dirs = [
        'app', 
        'src',
        'phindllama/phindllama'  # Remove duplicate structure
    ]
    
    for dir_path in empty_dirs:
        dir_path = root / dir_path
        try:
            dir_path.rmdir()
        except (OSError, FileNotFoundError):
            pass
    
    # 4. Ensure all Python packages have __init__.py
    for py_dir in root.glob('phindllama/**/'):
        if py_dir.is_dir():
            init_file = py_dir / '__init__.py'
            if not init_file.exists():
                init_file.touch()
    
    # 5. Fix test structure
    test_dir = root / "tests"
    test_dir.mkdir(exist_ok=True)
    shutil.move(str(root / "test"), str(test_dir / "unit"))
    
    # 6. Update critical files
    (package_dir / "__main__.py").write_text("from phindllama.orchestrator import main\n\nif __name__ == '__main__':\n    main()")
    
    print(f"Reorganization complete. New structure:\n")
    os.system(f"tree -L 3 {root_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=".", help="Path to repository root")
    args = parser.parse_args()
    
    reorganize_structure(args.path)
