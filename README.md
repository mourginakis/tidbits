# tidbits
cool little code tidbits

## Python

```python
# add current file to the path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```
- `concurrent.py` is a clojure core.async inspired channel implementation.
- `walk.py` is a clojure inspired tree traversal library.


## Evolve (singularity)

- claude's `--dangerously-skip-permissions` should probably be run in docker.
- `yoloclaude` is a wrapper that runs claude in a docker container.
- `evolve` is a recursive self improvement loop. 🫣
- `golem.py` is accessibility for browser automation.
- `chromex` is a script that starts chrome and exposes CDP.
