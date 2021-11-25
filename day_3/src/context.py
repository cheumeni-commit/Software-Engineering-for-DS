# src/context.py 
from types import SimpleNamespace

from src.config.directories import directories

context = SimpleNamespace(dirs=directories)

print(context.dirs)

# Now, all the directories are accessible via `context.dirs`