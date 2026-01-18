# Convex Hull Implementation

This is an implementation for two algorithms generating 2D Convex Hulls - **Graham Scan** and **Divide & Conquer**.

## How to run

There are 3 ways to run the implementation.

### 1. Interactive Drawing in Web UI
```bash
python -m http.server 8080
```
Then open <http://0.0.0.0:8080/> in a web browser or the **Ports** tab if you are using VSCode

- **Click on the canvas** to add points manually (this helps us testing tricky edge cases easily), or just click **Random** button to generate random points
- **Compute Hull** shows convex hulls computed by both algorithms (green=Graham, orange=Divide-and-Conquer)
- **Export/Import** to save/load points as JSON

### 2. Test from File
```bash
# Save points from web UI, then:
echo '[[100,200],[150,300],[200,150]]' > test.json
python test_runner.py test.json
```
### 3. Batch Tests
```bash
python test_runner.py           # Run benchmark with various testcase sizes
python test_runner.py --verify  # Verify correctness (by comparing results of 2 algorithms)
```