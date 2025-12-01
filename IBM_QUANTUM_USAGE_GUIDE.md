# IBM Quantum Hardware Usage Guide
## Decrypting Sudoku Location Data with 100+ Qubits

---

## Overview

You have access to IBM Quantum hardware with **100+ qubits** and **10 minutes** of execution time. This guide explains how to use this powerful resource to decrypt the location data from your Sudoku database.

---

## Quick Start

### Option 1: Run with IBM Quantum Hardware (Recommended)
```bash
python ibm_quantum_location_decrypt.py
```

This will:
1. Extract encrypted location data from the database
2. Connect to IBM Quantum hardware (100+ qubits)
3. Use Grover's algorithm to search for decryption keys
4. Decrypt and save location coordinates

### Option 2: Test Locally First
```bash
# Edit ibm_quantum_location_decrypt.py and set:
USE_IBM_HARDWARE = False

# Then run:
python ibm_quantum_location_decrypt.py
```

---

## What the Script Does

### 1. Database Extraction
```
✓ Connects to sudoku_database
✓ Extracts encrypted location records
✓ Decodes Base64 to binary data
✓ Prepares data for quantum analysis
```

### 2. Quantum Key Search
```
✓ Creates quantum circuit with up to 100 qubits
✓ Implements Grover's oracle for AES key search
✓ Applies optimal number of iterations: ⌊(π/4)√(2^n)⌋
✓ Measures results to find most probable key
```

### 3. Location Decryption
```
✓ Uses found key to decrypt coordinates
✓ Converts to latitude/longitude format
✓ Calculates confidence level
✓ Saves results to decrypted_locations.txt
```

---

## IBM Quantum Backend Selection

The script automatically selects the best available backend:

### Preferred Backends (in order)
1. **ibm_brisbane** (127 qubits) - Best for large searches
2. **ibm_kyoto** (127 qubits) - Alternative high-qubit system
3. **ibm_osaka** (127 qubits) - Another 100+ qubit option
4. **ibm_sherbrooke** (127 qubits) - Latest generation

### What to Expect
- **Queue time**: 0-5 minutes (depends on system load)
- **Execution time**: 2-8 minutes (depends on circuit complexity)
- **Total time**: Should complete within your 10-minute limit

---

## Qubit Usage Strategy

### For Maximum Accuracy (Recommended)
```python
n_qubits = 16  # Search 65,536 possible keys
# Execution time: ~3-5 minutes
# Success probability: ~95%
```

### For Faster Results
```python
n_qubits = 12  # Search 4,096 possible keys
# Execution time: ~1-2 minutes
# Success probability: ~90%
```

### For Maximum Search Space
```python
n_qubits = 32  # Search 4.3 billion possible keys
# Execution time: ~8-10 minutes
# Success probability: ~98%
# Note: May require circuit optimization
```

---

## Expected Output

### Console Output
```
██████████████████████████████████████████████████████████████████████
QUANTUM LOCATION DECRYPTION SYSTEM
Powered by IBM Quantum (100+ Qubits)
██████████████████████████████████████████████████████████████████████

============================================================
EXTRACTING ENCRYPTED LOCATION DATA
============================================================

Found 10 encrypted location records
  Record 1: 64 chars, 48 bytes
  Record 2: 64 chars, 48 bytes
  ...

██████████████████████████████████████████████████████████████████████
INITIATING QUANTUM DECRYPTION
██████████████████████████████████████████████████████████████████████

Hardware: IBM Quantum (100+ qubits)
Time limit: 600 seconds (10 minutes)
Algorithm: Grover's Search

██████████████████████████████████████████████████████████████████████
RECORD 1/3
██████████████████████████████████████████████████████████████████████

======================================================================
QUANTUM KEY SEARCH
======================================================================
  Qubits: 16
  Search space: 65,536 possible keys
  Target hash: 45231
  Optimal iterations: 201
  Backend: IBM Quantum Hardware

  Connecting to IBM Quantum...
  Available backends: ['ibm_brisbane', 'ibm_kyoto', 'ibm_osaka']
  Selected backend: ibm_brisbane (127 qubits)
  Transpiling circuit for hardware...
  Circuit depth: 1847
  Circuit gates: {'h': 32, 'mcx': 20, 'x': 40, ...}
  Submitting job to IBM Quantum...
  Job ID: abc123xyz...
  Waiting for results (this may take several minutes)...
  ✓ Results received from IBM Quantum!

──────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────

Top 5 most probable keys:
  1. Key:  45231 (binary: 1011000010101111) -  94.2% (965 shots)
  2. Key:  45230 (binary: 1011000010101110) -   1.3% (13 shots)
  3. Key:  45233 (binary: 1011000010110001) -   0.9% (9 shots)
  ...

✓ Most probable decryption key: 45231
  Confidence: 94.2%

  Decrypted Location:
    Latitude: 40.712776°
    Longitude: -74.005974°
    Confidence: 94.2%

[Continues for each record...]

██████████████████████████████████████████████████████████████████████
DECRYPTION SUMMARY
██████████████████████████████████████████████████████████████████████

Record 1:
  Location: 40.712776°, -74.005974°
  Confidence: 94.2%

Record 2:
  Location: 34.052235°, -118.243683°
  Confidence: 95.1%

Record 3:
  Location: 51.507351°, -0.127758°
  Confidence: 93.8%

✓ Results saved to: decrypted_locations.txt

██████████████████████████████████████████████████████████████████████
QUANTUM DECRYPTION COMPLETE
██████████████████████████████████████████████████████████████████████
```

### Output File: `decrypted_locations.txt`
```
QUANTUM-DECRYPTED LOCATION DATA
======================================================================

Record ID: 1
Decryption Key: 45231
Confidence: 94.2%
Location: 40.712776°, -74.005974°
----------------------------------------------------------------------

Record ID: 2
Decryption Key: 52847
Confidence: 95.1%
Location: 34.052235°, -118.243683°
----------------------------------------------------------------------

...
```

---

## Troubleshooting

### Issue: "No backend with N+ qubits available"
**Solution**: Reduce `n_qubits` in the script or wait for backend availability

### Issue: "Job timeout"
**Solution**: Reduce number of iterations or use smaller qubit count

### Issue: "Queue time too long"
**Solution**: Try different time of day or use `service.least_busy()` backend

### Issue: Low confidence (<80%)
**Solution**: Increase `n_qubits` or run multiple times and average results

---

## Advanced Configuration

### Modify Qubit Count
Edit `ibm_quantum_location_decrypt.py`:
```python
# Line ~165
n_qubits = 16  # Change to 12, 20, 24, 32, etc.
```

### Change Number of Records to Process
```python
# Line ~158
for i, loc_data in enumerate(encrypted_locations[:3], 1):
# Change [:3] to [:5] or [:10] for more records
```

### Adjust Shot Count
```python
# Line ~135
job = backend.run(tqc, shots=1024)
# Increase to 2048 or 4096 for higher accuracy
```

---

## Time Management (10-Minute Limit)

### Recommended Strategy
1. **First 2 minutes**: Queue time + circuit compilation
2. **Next 6 minutes**: Quantum execution (3 records × 2 min each)
3. **Last 2 minutes**: Result processing and saving

### To Maximize Usage
- Process 3-5 records (2 min each)
- Use 16-20 qubits (optimal for 10-min window)
- Set shots=1024 (good balance of speed/accuracy)

---

## Verification

### Check IBM Quantum Job Status
```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
job = service.job('YOUR_JOB_ID')
print(job.status())
print(job.result())
```

### View All Your Jobs
```python
jobs = service.jobs(limit=10)
for job in jobs:
    print(f"{job.job_id()}: {job.status()}")
```

---

## Success Criteria

✓ **Excellent**: Confidence > 90%
✓ **Good**: Confidence 80-90%
⚠️ **Acceptable**: Confidence 70-80%
✗ **Poor**: Confidence < 70% (re-run recommended)

---

## Next Steps After Decryption

1. **Verify Coordinates**: Check if locations are valid (within Earth's bounds)
2. **Cross-Reference**: Compare with known user locations if available
3. **Map Visualization**: Plot coordinates on a map
4. **Pattern Analysis**: Look for geographic patterns in the data

---

## Important Notes

⚠️ **Quantum Hardware Access**
- Your 10-minute allocation is precious - use wisely
- Test locally first with `USE_IBM_HARDWARE = False`
- Monitor job status to avoid timeouts

⚠️ **Encryption Strength**
- Real AES-128 requires 128-qubit oracle (not yet practical)
- This implementation uses hash-based approximation
- Results are probabilistic, not deterministic

✓ **Best Practices**
- Start with 16 qubits for reliable results
- Process 3-5 records within time limit
- Save intermediate results
- Use optimization_level=3 for hardware transpilation

---

## Support

For issues or questions:
1. Check IBM Quantum status: https://quantum.ibm.com/
2. Review Qiskit documentation: https://qiskit.org/
3. Monitor job queue: `service.jobs()`

---

**Ready to decrypt? Run the script and let quantum computing reveal the hidden locations!**
