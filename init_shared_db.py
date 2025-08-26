import os
import sys
import subprocess

# Add the directory containing this script to the Python path
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Run the prerequisite shell script
prereq_script_path = os.path.join(script_dir, "shared", "scripts", "init_db_prerequisites.sh")
subprocess.run([prereq_script_path], check=True)

# Now import relative to the project root
from shared.database_base.create_tables import create_db_tables

if __name__ == "__main__":
    create_db_tables()